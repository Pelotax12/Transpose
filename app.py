import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- 1. LÓGICA DE TRANSPOSIÇÃO (Baseada nos seus PDFs) ---
# Mapeamento de Pitch Concertante (Violão/Teclado) para Saxofone Alto
# Regra: Transpor uma 3ª menor abaixo (ou 6ª Maior acima)
CONCERT_TO_ALTO = {
    'C': 'A', 'C#': 'A#', 'Db': 'Bb',
    'D': 'B', 'D#': 'C', 'Eb': 'C',
    'E': 'C#', 'F': 'D', 'F#': 'D#', 'Gb': 'Eb',
    'G': 'E', 'G#': 'F', 'Ab': 'F',
    'A': 'F#', 'A#': 'G', 'Bb': 'G',
    'B': 'G#', 'Cb': 'Ab'
}

def transpose_chord(chord_str):
    """Transpõe um acorde individual preservando a qualidade e o baixo (slash)"""
    if not chord_str:
        return ""
    
    # Regex para capturar: Raiz, Qualidade (m, 7, maj, etc), e Baixo (ex: /E)
    match = re.match(r'^([A-G][#b]?)(.*?)(?:/([A-G][#b]?))?$', chord_str.strip())
    if not match:
        return chord_str
    
    root = match.group(1)
    quality = match.group(2)
    bass = match.group(3)
    
    # Transpõe a raiz
    new_root = CONCERT_TO_ALTO.get(root, root)
    
    # Transpõe o baixo, se existir
    new_bass = CONCERT_TO_ALTO.get(bass, bass) if bass else ""
    
    if new_bass:
        return f"{new_root}{quality}/{new_bass}"
    return f"{new_root}{quality}"

# --- 2. LÓGICA DE EXTRAÇÃO (Web Scraping) ---
def scrape_cifra(url):
    """Busca a página e extrai os acordes do Cifra Club"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return None, f"Erro ao acessar o link: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # O Cifra Club coloca os acordes em tags <b> dentro de um <pre> ou div específica
    # Vamos tentar encontrar o bloco da cifra
    cifra_block = soup.find('pre', id='cifra') or soup.find('div', class_='cifra') or soup.find('pre')
    
    if not cifra_block:
        return None, "Não foi possível encontrar o bloco de cifras na página. Use a opção de colar o texto manualmente."

    # Clona o bloco para não alterar o original
    transposed_block = BeautifulSoup(str(cifra_block), 'html.parser')
    
    # Encontra todas as tags <b> (que são os acordes no Cifra Club) e transpõe
    for b_tag in transposed_block.find_all('b'):
        original_chord = b_tag.text.strip()
        if original_chord:
            b_tag.string = transpose_chord(original_chord)
            
    return transposed_block.get_text(), None

# --- 3. PROCESSAMENTO DE TEXTO (Fallback Manual) ---
def process_raw_text(text):
    """Se o scraping falhar, transpõe acordes encontrados no texto cru"""
    lines = text.split('\n')
    transposed_lines = []
    
    # Regex para identificar linhas que parecem ser apenas acordes
    chord_pattern = re.compile(r'^\s*([A-G][#b]?(?:m|maj|min|dim|aug|sus|add|[0-9]|/[A-G][#b]?)*\s*)+$')
    
    for line in lines:
        if chord_pattern.match(line):
            # Se a linha é só acordes, transpõe cada palavra
            words = line.split()
            transposed_words = [transpose_chord(w) for w in words]
            transposed_lines.append(" ".join(transposed_words))
        else:
            transposed_lines.append(line)
            
    return "\n".join(transposed_lines)

# --- 4. INTERFACE DO APLICATIVO (STREAMLIT) ---
st.set_page_config(page_title="Transpositor para Sax Alto", page_icon="🎷", layout="wide")

st.title("🎷 Transpositor de Cifras para Saxofone Alto")
st.markdown("Transponha cifras de violão, guitarra e teclado (Concert Pitch) diretamente para a leitura do **Saxofone Alto** (Eb).")
st.markdown("---")

tab1, tab2 = st.tabs(["🔗 Extrair de Link", "📝 Colar Texto Manualmente"])

with tab1:
    st.subheader("Extrair do Cifra Club (ou similar)")
    url_input = st.text_input("Cole o link da música aqui:", placeholder="https://www.cifraclub.com.br/...")
    
    if st.button("Transpor Cifra"):
        if url_input:
            with st.spinner("Buscando e transpondo..."):
                result, error = scrape_cifra(url_input)
                if error:
                    st.error(error)
                else:
                    st.success("Cifra transposta com sucesso!")
                    st.code(result, language="text")
        else:
            st.warning("Por favor, insira um link válido.")

with tab2:
    st.subheader("Colar a Cifra Diretamente")
    st.info("Use esta opção se o site bloquear o acesso automático ou se a cifra estiver em outro formato.")
    text_input = st.text_area("Cole a letra e os acordes aqui:", height=300)
    
    if st.button("Transpor Texto"):
        if text_input:
            result = process_raw_text(text_input)
            st.success("Texto transcrito e transposto!")
            st.code(result, language="text")
        else:
            st.warning("Por favor, cole algum texto.")

st.markdown("---")
st.caption("Desenvolvido com base nas tabelas oficiais de transposição. Regra aplicada: Concert Pitch -> Alto Sax (3ª menor abaixo / 6ª maior acima). Ex: C -> A, G -> E.")

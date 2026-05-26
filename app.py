import streamlit as st
from music21 import note, stream, converter
import re

# Configurar página
st.set_page_config(page_title="Transpositor de Guitarra para Sax Alto", layout="wide")
st.title("🎸 Transpositor de Guitarra para 🎷 Sax Alto")

st.markdown("""
Este aplicativo transpõe notas de guitarra para notação de sax alto.
- **Guitarra**: Instrumento em altura de concerto
- **Sax Alto**: Instrumento em Mib (soa uma sexta maior mais baixo)
""")

# Notas musicais
NOTAS = ['Dó', 'Dó#', 'Ré', 'Ré#', 'Mi', 'Fá', 'Fá#', 'Sol', 'Sol#', 'Lá', 'Lá#', 'Si']
NOTAS_INGLES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SEMITONS_TRANSPOSICAO = 9  # Uma sexta maior = 9 semitons para cima

def transpor_nota(nome_nota, semitons):
    """
    Transpõe uma nota individual por um número de semitons.
    
    Args:
        nome_nota (str): Nome da nota (ex: 'C4', 'D#5')
        semitons (int): Número de semitons para transpor
    
    Returns:
        str: Nota transposta
    """
    try:
        # Usar music21 para transposição
        n = note.Note(nome_nota)
        transposta = n.transpose(semitons)
        return str(transposta.pitch)
    except:
        return None

def converter_nota_portuguesa(nome_nota_ingles):
    """
    Converte notação inglesa (C, D, E...) para portuguesa (Dó, Ré, Mi...)
    """
    mapa = {
        'C': 'Dó', 'D': 'Ré', 'E': 'Mi', 'F': 'Fá',
        'G': 'Sol', 'A': 'Lá', 'B': 'Si'
    }
    
    resultado = ""
    i = 0
    while i < len(nome_nota_ingles):
        if nome_nota_ingles[i] in mapa:
            resultado += mapa[nome_nota_ingles[i]]
        else:
            resultado += nome_nota_ingles[i]
        i += 1
    
    return resultado

def analisar_notacao_guitarra(texto_entrada):
    """
    Analisa notação de guitarra e retorna lista de notas.
    Aceita formatos como: C4 D4 E4 ou C4, D4, E4
    """
    # Remover espaços extras e dividir
    texto_entrada = texto_entrada.strip()
    
    # Dividir por espaço ou vírgula
    lista_notas = re.split(r'[,\s]+', texto_entrada)
    lista_notas = [n.strip() for n in lista_notas if n.strip()]
    
    return lista_notas

def validar_notas(lista_notas):
    """
    Valida se as notas são válidas.
    """
    notas_validas = []
    notas_invalidas = []
    
    for n in lista_notas:
        try:
            note.Note(n)
            notas_validas.append(n)
        except:
            notas_invalidas.append(n)
    
    return notas_validas, notas_invalidas

# Interface do Streamlit
st.header("📝 Opções de Entrada")

col1, col2 = st.columns(2)

with col1:
    metodo_entrada = st.radio(
        "Escolha o método de entrada:",
        ["Múltiplas Notas", "Uma Nota"],
        horizontal=True
    )

if metodo_entrada == "Múltiplas Notas":
    entrada_guitarra = st.text_area(
        "Digite as notas da guitarra (separadas por espaços ou vírgulas):",
        placeholder="Exemplo: C4 D4 E4 F#4 G4",
        height=100
    )
    
    if entrada_guitarra:
        lista_notas = analisar_notacao_guitarra(entrada_guitarra)
        notas_validas, notas_invalidas = validar_notas(lista_notas)
        
        if notas_invalidas:
            st.warning(f"⚠️ Notas inválidas detectadas: {', '.join(notas_invalidas)}")
        
        if notas_validas:
            st.success(f"✅ {len(notas_validas)} nota(s) válida(s) encontrada(s)")
        
else:  # Uma Nota
    col_nota, col_oitava = st.columns(2)
    
    with col_nota:
        nome_nota_guitarra = st.selectbox(
            "Nota:",
            NOTAS_INGLES,
            index=0
        )
    
    with col_oitava:
        oitava_guitarra = st.number_input(
            "Oitava:",
            min_value=0,
            max_value=8,
            value=4
        )
    
    entrada_guitarra = f"{nome_nota_guitarra}{oitava_guitarra}"
    lista_notas = [entrada_guitarra]
    notas_validas = lista_notas

# Transposição
if notas_validas:
    st.header("📊 Resultados da Transposição")
    
    notas_transpostas = []
    
    for nota_guitarra in notas_validas:
        transposta = transpor_nota(nota_guitarra, SEMITONS_TRANSPOSICAO)
        if transposta:
            notas_transpostas.append(transposta)
    
    # Exibir resultados em tabela
    if notas_transpostas:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎸 Notas da Guitarra (Altura de Concerto)")
            st.write(", ".join(notas_validas))
        
        with col2:
            st.subheader("🎷 Notas do Sax Alto")
            st.write(", ".join(notas_transpostas))
        
        # Tabela detalhada
        st.subheader("📋 Transposição Detalhada")
        
        dados_tabela = []
        for guitarra, sax in zip(notas_validas, notas_transpostas):
            guitarra_pt = converter_nota_portuguesa(guitarra)
            sax_pt = converter_nota_portuguesa(sax)
            dados_tabela.append({
                "Nota Guitarra": guitarra_pt,
                "Nota Sax Alto": sax_pt,
            })
        
        st.table(dados_tabela)
        
        # Exportar resultados
        st.subheader("📥 Exportar Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            saida_csv = "Nota Guitarra,Nota Sax Alto\n"
            saida_csv += "\n".join([f"{g},{s}" for g, s in zip(notas_validas, notas_transpostas)])
            st.download_button(
                label="Baixar em CSV",
                data=saida_csv,
                file_name="transposicao.csv",
                mime="text/csv"
            )
        
        with col2:
            saida_texto = "TRANSPOSIÇÃO DE GUITARRA PARA SAX ALTO\n"
            saida_texto += "="*50 + "\n\n"
            saida_texto += "Notas da Guitarra (Altura de Concerto):\n"
            saida_texto += ", ".join(notas_validas) + "\n\n"
            saida_texto += "Notas do Sax Alto:\n"
            saida_texto += ", ".join(notas_transpostas) + "\n"
            
            st.download_button(
                label="Baixar em TXT",
                data=saida_texto,
                file_name="transposicao.txt",
                mime="text/plain"
            )

# Informações úteis
st.markdown("---")
st.subheader("ℹ️ Informações")

with st.expander("Como funciona a transposição?"):
    st.markdown("""
    **Transposição para Sax Alto:**
    - O sax alto é um instrumento em Mib
    - Quando um músico de sax alto toca uma nota, ela soa uma sexta maior mais baixa
    - Isso significa: para transpor notas de guitarra para sax alto, adicionamos 9 semitons
    
    **Exemplos:**
    - Guitarra Dó4 → Sax Alto Lá4 (soa como Dó4)
    - Guitarra Ré4 → Sax Alto Si4 (soa como Ré4)
    - Guitarra Mi4 → Sax Alto Dó#5 (soa como Mi4)
    """)

with st.expander("Convenção de Nomeação de Notas"):
    st.markdown("""
    **Formato: Nome da Nota + Oitava**
    - Nomes das notas: Dó, Dó#, Ré, Ré#, Mi, Fá, Fá#, Sol, Sol#, Lá, Lá#, Si
    - Oitavas: 0-8 (intervalo comum para guitarra: 2-6)
    - Exemplos: Dó4, Ré#5, Fá#3, Sol2
    
    **Afinação Padrão da Guitarra:**
    - Corda Mi baixo: Mi2
    - Corda Lá: Lá2
    - Corda Ré: Ré3
    - Corda Sol: Sol3
    - Corda Si: Si3
    - Corda Mi agudo: Mi4
    """)

st.markdown("---")
st.caption("Feito com ❤️ usando Streamlit e music21")

import streamlit as st
from music21 import note, stream, converter
import re

# Configurar página
st.set_page_config(page_title="Transpositor de Violão para Sax Alto", layout="wide")
st.title("🎸 Transpositor de Violão para 🎷 Sax Alto")

st.markdown("""
Este aplicativo transpõe notas de violão para notação de sax alto e gera escalas para acompanhamento musical.
- **Violão**: Instrumento em altura de concerto
- **Sax Alto**: Instrumento em Mib (soa uma sexta maior mais baixo)
""")

# Notas musicais
NOTAS_INGLES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_PT = ['Dó', 'Dó#', 'Ré', 'Ré#', 'Mi', 'Fá', 'Fá#', 'Sol', 'Sol#', 'Lá', 'Lá#', 'Si']
SEMITONS_TRANSPOSICAO = 9  # Uma sexta maior = 9 semitons para cima

# Intervalos para escalas (em semitons a partir da tônica)
ESCALA_MAIOR = [0, 2, 4, 5, 7, 9, 11, 12]  # 8 notas
ESCALA_PENTATONICA_MENOR = [0, 3, 5, 7, 10, 12]  # 6 notas (incluindo oitava)

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

def gerar_escala_maior(nota_tonica, oitava_inicial=4):
    """
    Gera uma escala maior a partir de uma tônica.
    
    Args:
        nota_tonica (str): Nota em inglês (ex: 'C')
        oitava_inicial (int): Oitava inicial
    
    Returns:
        list: Lista de notas da escala
    """
    try:
        nota_base = note.Note(f"{nota_tonica}{oitava_inicial}")
        escala = []
        for intervalo in ESCALA_MAIOR:
            nota_escala = nota_base.transpose(intervalo)
            escala.append(str(nota_escala.pitch))
        return escala
    except:
        return []

def gerar_escala_pentatonica(nota_tonica, oitava_inicial=4):
    """
    Gera uma escala pentatônica menor a partir de uma tônica.
    
    Args:
        nota_tonica (str): Nota em inglês (ex: 'C')
        oitava_inicial (int): Oitava inicial
    
    Returns:
        list: Lista de notas da escala pentatônica
    """
    try:
        nota_base = note.Note(f"{nota_tonica}{oitava_inicial}")
        escala = []
        for intervalo in ESCALA_PENTATONICA_MENOR:
            nota_escala = nota_base.transpose(intervalo)
            escala.append(str(nota_escala.pitch))
        return escala
    except:
        return []

def analisar_notacao_violao(texto_entrada):
    """
    Analisa notação de violão e retorna lista de notas.
    """
    texto_entrada = texto_entrada.strip()
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

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================

# Abas para diferentes funcionalidades
aba1, aba2 = st.tabs(["🎵 Transposição de Notas", "🎼 Acompanhamento Musical"])

# ============================================================================
# ABA 1: TRANSPOSIÇÃO DE NOTAS
# ============================================================================
with aba1:
    st.header("📝 Opções de Entrada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metodo_entrada = st.radio(
            "Escolha o método de entrada:",
            ["Múltiplas Notas", "Uma Nota"],
            horizontal=True
        )
    
    if metodo_entrada == "Múltiplas Notas":
        entrada_violao = st.text_area(
            "Digite as notas do violão (separadas por espaços ou vírgulas):",
            placeholder="Exemplo: C4 D4 E4 F#4 G4",
            height=100
        )
        
        if entrada_violao:
            lista_notas = analisar_notacao_violao(entrada_violao)
            notas_validas, notas_invalidas = validar_notas(lista_notas)
            
            if notas_invalidas:
                st.warning(f"⚠️ Notas inválidas detectadas: {', '.join(notas_invalidas)}")
            
            if notas_validas:
                st.success(f"✅ {len(notas_validas)} nota(s) válida(s) encontrada(s)")
            
    else:  # Uma Nota
        col_nota, col_oitava = st.columns(2)
        
        with col_nota:
            nome_nota_violao = st.selectbox(
                "Nota:",
                NOTAS_INGLES,
                index=0
            )
        
        with col_oitava:
            oitava_violao = st.number_input(
                "Oitava:",
                min_value=0,
                max_value=8,
                value=4
            )
        
        entrada_violao = f"{nome_nota_violao}{oitava_violao}"
        lista_notas = [entrada_violao]
        notas_validas = lista_notas
    
    # Transposição
    if notas_validas:
        st.header("📊 Resultados da Transposição")
        
        notas_transpostas = []
        
        for nota_violao in notas_validas:
            transposta = transpor_nota(nota_violao, SEMITONS_TRANSPOSICAO)
            if transposta:
                notas_transpostas.append(transposta)
        
        # Exibir resultados em tabela
        if notas_transpostas:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎸 Notas do Violão (Altura de Concerto)")
                st.write(", ".join(notas_validas))
            
            with col2:
                st.subheader("🎷 Notas do Sax Alto")
                st.write(", ".join(notas_transpostas))
            
            # Tabela detalhada
            st.subheader("📋 Transposição Detalhada")
            
            dados_tabela = []
            for violao, sax in zip(notas_validas, notas_transpostas):
                violao_pt = converter_nota_portuguesa(violao)
                sax_pt = converter_nota_portuguesa(sax)
                dados_tabela.append({
                    "Nota Violão": violao_pt,
                    "Nota Sax Alto": sax_pt,
                })
            
            st.table(dados_tabela)
            
            # Exportar resultados
            st.subheader("📥 Exportar Resultados")
            col1, col2 = st.columns(2)
            
            with col1:
                saida_csv = "Nota Violão,Nota Sax Alto\n"
                saida_csv += "\n".join([f"{v},{s}" for v, s in zip(notas_validas, notas_transpostas)])
                st.download_button(
                    label="Baixar em CSV",
                    data=saida_csv,
                    file_name="transposicao.csv",
                    mime="text/csv"
                )
            
            with col2:
                saida_texto = "TRANSPOSIÇÃO DE VIOLÃO PARA SAX ALTO\n"
                saida_texto += "="*50 + "\n\n"
                saida_texto += "Notas do Violão (Altura de Concerto):\n"
                saida_texto += ", ".join(notas_validas) + "\n\n"
                saida_texto += "Notas do Sax Alto:\n"
                saida_texto += ", ".join(notas_transpostas) + "\n"
                
                st.download_button(
                    label="Baixar em TXT",
                    data=saida_texto,
                    file_name="transposicao.txt",
                    mime="text/plain"
                )

# ============================================================================
# ABA 2: ACOMPANHAMENTO MUSICAL
# ============================================================================
with aba2:
    st.header("🎼 Modo Acompanhamento Musical")
    
    st.markdown("""
    Use este modo para preparar o acompanhamento musical da sua banda!
    
    **Como funciona:**
    1. Escolha o **tom da música** (a nota tônica em que a banda está tocando)
    2. O app gera as **escalas** que você pode usar para improvisar
    3. Veja as notas **transpostas para sax alto**
    4. Use as escalas para acompanhar harmonicamente
    """)
    
    # Seleção do tom
    st.markdown("### 🎵 Selecione o Tom da Música")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tom_indice = st.selectbox(
            "Escolha a nota tônica:",
            range(len(NOTAS_INGLES)),
            format_func=lambda x: NOTAS_INGLES[x],
            key="tom_nota"
        )
        tom_nota_ingles = NOTAS_INGLES[tom_indice]
        tom_nota_pt = NOTAS_PT[tom_indice]
    
    with col2:
        tom_oitava = st.number_input(
            "Oitava da tônica:",
            min_value=2,
            max_value=6,
            value=4,
            key="tom_oitava"
        )
    
    if tom_nota_ingles:
        # Gerar escalas
        escala_maior = gerar_escala_maior(tom_nota_ingles, tom_oitava)
        escala_pentatonica = gerar_escala_pentatonica(tom_nota_ingles, tom_oitava)
        
        # Transpor escalas para sax alto
        escala_maior_sax = [transpor_nota(n, SEMITONS_TRANSPOSICAO) for n in escala_maior]
        escala_pentatonica_sax = [transpor_nota(n, SEMITONS_TRANSPOSICAO) for n in escala_pentatonica]
        
        # ====================================================================
        # SEÇÃO 1: ESCALA MAIOR
        # ====================================================================
        st.markdown("---")
        st.markdown(f"### 1️⃣ ESCALA MAIOR DE {tom_nota_pt.upper()}")
        st.markdown("""
        A escala maior é a base para improviso e acompanhamento. Use-a para tocar melodias que combinam com o tom.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎸 Violão (Tom Original)")
            escala_maior_pt = [converter_nota_portuguesa(n) for n in escala_maior]
            st.info(f"**{tom_nota_pt}** → " + " → ".join(escala_maior_pt))
            
            with st.expander("Ver detalhes da escala:"):
                df_escala = []
                for i, (nota, nota_pt) in enumerate(zip(escala_maior, escala_maior_pt)):
                    df_escala.append({
                        "Posição": i + 1,
                        "Nota (Inglês)": nota,
                        "Nota (Português)": nota_pt
                    })
                st.dataframe(df_escala, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎷 Sax Alto (Transposição)")
            escala_maior_sax_pt = [converter_nota_portuguesa(n) for n in escala_maior_sax]
            st.success(f"**{converter_nota_portuguesa(escala_maior_sax[0])}** → " + " → ".join(escala_maior_sax_pt))
            
            with st.expander("Ver detalhes da transposição:"):
                df_escala_sax = []
                for i, (nota, nota_pt) in enumerate(zip(escala_maior_sax, escala_maior_sax_pt)):
                    df_escala_sax.append({
                        "Posição": i + 1,
                        "Nota (Inglês)": nota,
                        "Nota (Português)": nota_pt
                    })
                st.dataframe(df_escala_sax, use_container_width=True)
        
        # ====================================================================
        # SEÇÃO 2: ESCALA PENTATÔNICA
        # ====================================================================
        st.markdown("---")
        st.markdown(f"### 2️⃣ ESCALA PENTATÔNICA MENOR DE {tom_nota_pt.upper()}")
        st.markdown("""
        A escala pentatônica é mais prática para improviso rápido. Com apenas 5 notas principais, é mais fácil criar linhas melódicas que soam bem!
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎸 Violão (Tom Original)")
            # Remove a última nota (oitava) para mostrar apenas 5 notas principais
            escala_penta_pt = [converter_nota_portuguesa(n) for n in escala_pentatonica[:-1]]
            escala_penta_display = " → ".join(escala_penta_pt)
            st.info(f"**{tom_nota_pt}** → {escala_penta_display}")
            
            with st.expander("Dicas de uso:"):
                st.markdown("""
                - Use essas 5 notas para criar riffs e solos
                - A pentatônica soa bem em qualquer ordem
                - Perfeita para improviso sem "errar"
                - Muito usada em blues e rock
                """)
        
        with col2:
            st.markdown("#### 🎷 Sax Alto (Transposição)")
            escala_penta_sax_pt = [converter_nota_portuguesa(n) for n in escala_pentatonica_sax[:-1]]
            escala_penta_sax_display = " → ".join(escala_penta_sax_pt)
            st.success(f"**{converter_nota_portuguesa(escala_pentatonica_sax[0])}** → {escala_penta_sax_display}")
            
            with st.expander("Como usar no seu acompanhamento:"):
                st.markdown("""
                - Toque essas notas para acompanhar a banda
                - Crie frases musicais com essa sequência
                - Combine com ritmo para melhor fluidez
                """)
        
        # ====================================================================
        # SEÇÃO 3: RESUMO PARA ACOMPANHAMENTO
        # ====================================================================
        st.markdown("---")
        st.markdown("### 📋 Resumo Rápido para Acompanhamento")
        
        resumo_data = {
            "Tom": [tom_nota_pt.upper()],
            "Escala Maior (Sax)": [" - ".join(escala_maior_sax_pt)],
            "Pentatônica (Sax)": [" - ".join(escala_penta_sax_pt)],
        }
        
        st.dataframe(resumo_data, use_container_width=True)
        
        # ====================================================================
        # SEÇÃO 4: EXPORTAR
        # ====================================================================
        st.markdown("---")
        st.markdown("### 📥 Exportar para Referência")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar em TXT
            saida_txt = f"ACOMPANHAMENTO MUSICAL - TOM: {tom_nota_pt.upper()}\n"
            saida_txt += "="*60 + "\n\n"
            saida_txt += "ESCALA MAIOR (Sax Alto):\n"
            saida_txt += " → ".join(escala_maior_sax_pt) + "\n\n"
            saida_txt += "ESCALA PENTATÔNICA MENOR (Sax Alto):\n"
            saida_txt += " → ".join(escala_penta_sax_pt) + "\n\n"
            saida_txt += "NOTAS (Notação Inglesa)\n"
            saida_txt += "Escala Maior: " + " → ".join(escala_maior_sax) + "\n"
            saida_txt += "Pentatônica: " + " → ".join(escala_pentatonica_sax[:-1]) + "\n"
            
            st.download_button(
                label="📄 Baixar Resumo (TXT)",
                data=saida_txt,
                file_name=f"acompanhamento_{tom_nota_pt.lower()}.txt",
                mime="text/plain"
            )
        
        with col2:
            # Exportar em CSV
            saida_csv = "Tipo,Notas (Sax Alto)\n"
            saida_csv += f"Escala Maior,{' | '.join(escala_maior_sax_pt)}\n"
            saida_csv += f"Pentatônica,{' | '.join(escala_penta_sax_pt)}\n"
            
            st.download_button(
                label="📊 Baixar Dados (CSV)",
                data=saida_csv,
                file_name=f"acompanhamento_{tom_nota_pt.lower()}.csv",
                mime="text/csv"
            )

# ============================================================================
# INFORMAÇÕES GERAIS
# ============================================================================
st.markdown("---")
st.subheader("ℹ️ Informações Úteis")

with st.expander("Como funciona a transposição?"):
    st.markdown("""
    **Transposição para Sax Alto:**
    - O sax alto é um instrumento em Mib
    - Quando um músico de sax alto toca uma nota, ela soa uma sexta maior mais baixa
    - Isso significa: para transpor notas de violão para sax alto, adicionamos 9 semitons
    
    **Exemplos:**
    - Violão Dó4 → Sax Alto Lá4 (soa como Dó4)
    - Violão Ré4 → Sax Alto Si4 (soa como Ré4)
    - Violão Mi4 → Sax Alto Dó#5 (soa como Mi4)
    """)

with st.expander("Diferença entre Escala Maior e Pentatônica"):
    st.markdown("""
    **Escala Maior (8 notas):**
    - Completa e estruturada
    - Toca bem em qualquer ordem
    - Ideal para melodias precisas
    - Exemplo em Dó: Dó, Ré, Mi, Fá, Sol, Lá, Si, Dó
    
    **Escala Pentatônica Menor (5 notas):**
    - Simplificada (poucas notas)
    - Fácil de memorizar
    - Ótima para improviso rápido
    - Soa bem em qualquer ordem
    - Exemplo em Dó: Dó, Mib, Fá, Sol, Sib
    """)

with st.expander("Convenção de Nomeação de Notas"):
    st.markdown("""
    **Formato: Nome da Nota + Oitava**
    - Nomes das notas: Dó, Dó#, Ré, Ré#, Mi, Fá, Fá#, Sol, Sol#, Lá, Lá#, Si
    - Oitavas: 0-8 (intervalo comum para violão: 2-6)
    - Exemplos: Dó4, Ré#5, Fá#3, Sol2
    
    **Afinação Padrão do Violão:**
    - Corda Mi baixo: Mi2
    - Corda Lá: Lá2
    - Corda Ré: Ré3
    - Corda Sol: Sol3
    - Corda Si: Si3
    - Corda Mi agudo: Mi4
    """)

st.markdown("---")
st.caption("Feito com ❤️ usando Streamlit e music21")

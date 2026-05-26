import streamlit as st
from music21 import note, stream, converter
import re

# Configurar página
st.set_page_config(page_title="Guitar to Alto Sax Transposer", layout="wide")
st.title("🎸 Guitar to 🎷 Alto Saxophone Transposer")

st.markdown("""
This app transposes guitar notes to alto saxophone notation.
- **Guitar**: Concert pitch instrument
- **Alto Saxophone**: Eb instrument (sounds a major 6th lower)
""")

# Notas musicais
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
TRANSPOSITION_SEMITONES = 9  # Uma 6ª maior = 9 semitons para cima

def transpose_note(note_name, semitones):
    """
    Transpõe uma nota individual por um número de semitons.
    
    Args:
        note_name (str): Nome da nota (ex: 'C4', 'D#5')
        semitones (int): Número de semitons para transpor
    
    Returns:
        str: Nota transposta
    """
    try:
        # Usar music21 para transposição
        n = note.Note(note_name)
        transposed = n.transpose(semitones)
        return str(transposed.pitch)
    except:
        return None

def parse_guitar_notation(input_text):
    """
    Analisa notação de guitarra e retorna lista de notas.
    Aceita formatos como: C4 D4 E4 ou C4, D4, E4
    """
    # Remover espaços extras e dividir
    input_text = input_text.strip()
    
    # Dividir por espaço ou vírgula
    notes_list = re.split(r'[,\s]+', input_text)
    notes_list = [n.strip() for n in notes_list if n.strip()]
    
    return notes_list

def validate_notes(notes_list):
    """
    Valida se as notas são válidas.
    """
    valid_notes = []
    invalid_notes = []
    
    for n in notes_list:
        try:
            note.Note(n)
            valid_notes.append(n)
        except:
            invalid_notes.append(n)
    
    return valid_notes, invalid_notes

# Interface do Streamlit
st.header("Input Options")

col1, col2 = st.columns(2)

with col1:
    input_method = st.radio(
        "Choose input method:",
        ["Text Input", "Single Note"],
        horizontal=True
    )

if input_method == "Text Input":
    guitar_input = st.text_area(
        "Enter guitar notes (separated by spaces or commas):",
        placeholder="Example: C4 D4 E4 F#4 G4",
        height=100
    )
    
    if guitar_input:
        notes_list = parse_guitar_notation(guitar_input)
        valid_notes, invalid_notes = validate_notes(notes_list)
        
        if invalid_notes:
            st.warning(f"⚠️ Invalid notes detected: {', '.join(invalid_notes)}")
        
        if valid_notes:
            st.success(f"✅ Found {len(valid_notes)} valid notes")
        
else:  # Single Note
    col_note, col_octave = st.columns(2)
    
    with col_note:
        guitar_note_name = st.selectbox(
            "Note:",
            NOTES,
            index=0
        )
    
    with col_octave:
        guitar_octave = st.number_input(
            "Octave:",
            min_value=0,
            max_value=8,
            value=4
        )
    
    guitar_input = f"{guitar_note_name}{guitar_octave}"
    notes_list = [guitar_input]
    valid_notes = notes_list

# Transposição
if valid_notes:
    st.header("Transposition Results")
    
    transposed_notes = []
    
    for guitar_note in valid_notes:
        transposed = transpose_note(guitar_note, TRANSPOSITION_SEMITONES)
        if transposed:
            transposed_notes.append(transposed)
    
    # Exibir resultados em tabela
    if transposed_notes:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎸 Guitar Notes (Concert Pitch)")
            st.write(", ".join(valid_notes))
        
        with col2:
            st.subheader("🎷 Alto Saxophone Notes")
            st.write(", ".join(transposed_notes))
        
        # Tabela detalhada
        st.subheader("Detailed Transposition")
        
        table_data = []
        for guitar, sax in zip(valid_notes, transposed_notes):
            table_data.append({
                "Guitar Note": guitar,
                "Alto Sax Note": sax,
            })
        
        st.table(table_data)
        
        # Exportar resultados
        st.subheader("Export")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_output = "Guitar Note,Alto Sax Note\n"
            csv_output += "\n".join([f"{g},{s}" for g, s in zip(valid_notes, transposed_notes)])
            st.download_button(
                label="Download as CSV",
                data=csv_output,
                file_name="transposition.csv",
                mime="text/csv"
            )
        
        with col2:
            text_output = "GUITAR TO ALTO SAXOPHONE TRANSPOSITION\n"
            text_output += "="*40 + "\n\n"
            text_output += "Guitar Notes (Concert Pitch):\n"
            text_output += ", ".join(valid_notes) + "\n\n"
            text_output += "Alto Saxophone Notes:\n"
            text_output += ", ".join(transposed_notes) + "\n"
            
            st.download_button(
                label="Download as TXT",
                data=text_output,
                file_name="transposition.txt",
                mime="text/plain"
            )

# Informações úteis
st.markdown("---")
st.subheader("ℹ️ Information")

with st.expander("How the transposition works"):
    st.markdown("""
    **Alto Saxophone Transposition:**
    - Alto sax is an Eb instrument
    - When an alto sax player reads a note, it sounds a major 6th lower
    - This means: to transpose guitar notes to alto sax, we add 9 semitones
    
    **Example:**
    - Guitar C4 → Alto Sax A4 (sounds as C4)
    - Guitar D4 → Alto Sax B4 (sounds as D4)
    - Guitar E4 → Alto Sax C#5 (sounds as E4)
    """)

with st.expander("Note naming convention"):
    st.markdown("""
    **Format: NoteName + Octave**
    - Note names: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
    - Octaves: 0-8 (common range for guitar: 2-6)
    - Examples: C4, D#5, F#3, G2
    
    **Guitar Standard Tuning:**
    - Low E string: E2
    - A string: A2
    - D string: D3
    - G string: G3
    - B string: B3
    - High E string: E4
    """)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit and music21")

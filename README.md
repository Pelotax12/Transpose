# 🎸 Transpositor de Violão para 🎷 Sax Alto

Um aplicativo web interativo para transpor notas de violão para notação de sax alto, construído com **Streamlit** e **music21**.

## 📋 O que é Transposição?

Transposição é o processo de mudar a altura de uma composição musical. O sax alto é um instrumento transpositor em **Mib**, o que significa que soa uma sexta maior mais baixa do que está escrito. Este aplicativo automatiza o processo de transposição para você!

### Conceitos Musicais

- **Violão**: Instrumento em altura de concerto (soa como está escrito)
- **Sax Alto**: Instrumento em Mib (transpõe 9 semitons acima na escrita)

**Exemplo de Transposição:**
- Violão: Dó4 → Sax Alto: Lá4 (soa como Dó4)
- Violão: Ré4 → Sax Alto: Si4 (soa como Ré4)
- Violão: Mi4 → Sax Alto: Dó#5 (soa como Mi4)

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/Pelotax12/Transpose.git
cd Transpose
```

### Passo 2: Criar um Ambiente Virtual (Opcional, mas Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Executar o Aplicativo

```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no seu navegador em `http://localhost:8501`

### Opções de Entrada

#### 1️⃣ Múltiplas Notas
Digite várias notas de violão separadas por **espaços ou vírgulas**:
```
C4 D4 E4 F#4 G4
```
ou
```
C4, D4, E4, F#4, G4
```

#### 2️⃣ Uma Nota
Use o seletor para escolher:
- A nota (Dó, Ré, Mi, Fá, Sol, Lá, Si)
- A oitava (0-8)

## 📊 Funcionalidades

✅ **Transposição automática** de notas de violão para sax alto  
✅ **Validação de notas** com mensagens de erro informativas  
✅ **Visualização em tempo real** dos resultados  
✅ **Exportação de dados** em CSV e TXT  
✅ **Interface intuitiva** e responsiva  
✅ **Informações educativas** sobre transposição musical  

## 🎼 Referência de Notas

### Notas Musicais
- **Notas Naturais**: Dó, Ré, Mi, Fá, Sol, Lá, Si
- **Notas Acidentadas**: 
  - `#` (sustenido) = nota elevada em meio tom
  - `b` (bemol) = nota abaixada em meio tom

### Oitavas
- Intervalo: 0-8
- **Violão comum**: oitavas 2-6
- **Exemplo**: C4 (Dó na 4ª oitava)

### Afinação Padrão do Violão
| Corda | Nota |
|-------|------|
| Mi (baixo) | E2 |
| Lá | A2 |
| Ré | D3 |
| Sol | G3 |
| Si | B3 |
| Mi (agudo) | E4 |

## 📁 Estrutura do Projeto

```
Transpose/
├── app.py              # Aplicativo principal em Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 🔧 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework para criar aplicações web interativas
- **[music21](https://music21.readthedocs.io/)** - Biblioteca Python para análise e manipulação de música
- **Python 3** - Linguagem de programação

## 📦 Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| streamlit | 1.40.1 | Framework web interativo |
| music21 | 9.1.0 | Processamento de notação musical |

## 🤝 Como Contribuir

Contribuições são bem-vindas! Aqui está como você pode ajudar:

1. **Fork** o repositório
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

## 💡 Ideias para Futuras Versões

- [ ] Suporte para outros instrumentos transpostores (clarinete, trompete, etc.)
- [ ] Importar arquivos MusicXML
- [ ] Reprodução de áudio das notas
- [ ] Interface para acordes completos
- [ ] Exportação em formato de notação musical (PDF, PNG)
- [ ] Histórico de transposições
- [ ] Modo escuro/claro

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**João Gabriel (Pelotax12)**
- GitHub: [@Pelotax12](https://github.com/Pelotax12)

## 🆘 Suporte

Se você encontrar algum problema ou tiver uma sugestão, por favor:

1. Verifique as [Issues](https://github.com/Pelotax12/Transpose/issues) existentes
2. [Crie uma nova Issue](https://github.com/Pelotax12/Transpose/issues/new) se o problema não foi reportado

## 📚 Recursos Adicionais

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Documentação do music21](https://music21.readthedocs.io/)
- [Teoria Musical - Transposição](https://en.wikipedia.org/wiki/Transposition_(music))
- [Sax Alto - Wikipedia](https://pt.wikipedia.org/wiki/Saxofone)

---

**Feito com ❤️ usando Streamlit e music21**

import streamlit as st
import fitz
from groq import Groq
import os

# Caminho da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Extrair texto dos PDFs
def extract_text_from_pdfs(uploaded_pdfs):
    text = ""
    for pdf in uploaded_pdfs:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

# Consulta à Groq
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content

# Interface Streamlit
def main():
    st.set_page_config(page_title="Chat Inteligente", layout="centered")

    # Estilo visual com fundo azul
    st.markdown("""
        <style>
            body {
                background-color: #e6f0ff;
            }
            .stApp {
                background-color: #e6f0ff;
            }
            [data-testid="stSidebar"] {
                background-color: #cce0ff;
            }
            .title {
                text-align: center; 
                font-size: 2rem; 
                color: #2a4d8f;
            }
            .subtext {
                color: #4d6fa3; 
                text-align: center;
            }
            .stButton>button {
                background-color: #1f77d0;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 0.5rem 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar com logo e upload
    with st.sidebar:
        st.image(LOGO_PATH, width=180)
        st.header("📁 Upload de PDF")
        uploaded_pdfs = st.file_uploader("Selecione seus arquivos PDF", type="pdf", accept_multiple_files=True)

    st.markdown('<div class="title">📖 Assistente inteligente de biblioteca 📖</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtext">Faça upload de um ou mais PDFs e tire dúvidas sobre o conteúdo!</p>', unsafe_allow_html=True)

    if "document_text" not in st.session_state:
        st.session_state["document_text"] = ""

    if uploaded_pdfs:
        with st.spinner("🔍 Extraindo as Informações dos PDFs..."):
            st.session_state["document_text"] = extract_text_from_pdfs(uploaded_pdfs)
        st.success("✅ PDFs processados com sucesso!")

    user_input = st.text_area("💬 Digite sua pergunta aqui:", height=120)

    if st.button("Enviar") and user_input.strip() != "" and st.session_state["document_text"]:
        with st.spinner("🧠 Pensando..."):
            response = chat_with_groq(user_input, st.session_state["document_text"])
        st.markdown("### 📌 Resposta:")
        st.markdown(response)

if __name__ == "__main__":
    main()

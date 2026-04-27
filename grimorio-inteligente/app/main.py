import os
import sys
import base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from app.rag_pipeline import RAGPipeline


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "assets", "background.jpg")


def image_to_base64(image_path):
    if not os.path.exists(image_path):
        return None

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    return encoded


def load_custom_css():
    background_base64 = image_to_base64(BACKGROUND_IMAGE)

    if background_base64:
        background_css = f"""
        .stApp {{
            background-image:
                linear-gradient(rgba(15, 7, 7, 0.88), rgba(15, 7, 7, 0.92)),
                url("data:image/jpg;base64,{background_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    else:
        background_css = """
        .stApp {
            background:
                radial-gradient(circle at top, #4a0f12 0%, #160708 45%, #070303 100%);
        }
        """

    st.markdown(
        f"""
        <style>
        {background_css}

        html, body, [class*="css"] {{
            font-family: Georgia, 'Times New Roman', serif;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #180707 0%, #2a0b0d 50%, #120505 100%);
            border-right: 2px solid #8a6428;
        }}

        section[data-testid="stSidebar"] * {{
            color: #f2dfb3;
        }}

        .main-title {{
            text-align: center;
            padding: 28px 20px 10px 20px;
            color: #f6d98b;
            font-size: 52px;
            font-weight: 800;
            letter-spacing: 1px;
            text-shadow: 0 0 12px rgba(128, 0, 0, 0.9), 0 0 24px rgba(0, 0, 0, 0.9);
        }}

        .subtitle {{
            text-align: center;
            color: #d8b76a;
            font-size: 20px;
            margin-bottom: 32px;
        }}

        .hero-card {{
            background: rgba(28, 10, 10, 0.88);
            border: 1px solid #9a7432;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 0 28px rgba(0, 0, 0, 0.55);
            margin-bottom: 24px;
        }}

        .hero-card p {{
            color: #f3e4c2;
            font-size: 17px;
            line-height: 1.6;
            text-align: center;
        }}

        .section-card {{
            background: rgba(20, 8, 8, 0.92);
            border: 1px solid rgba(194, 146, 58, 0.75);
            border-radius: 16px;
            padding: 22px;
            margin-top: 18px;
            margin-bottom: 18px;
            box-shadow: 0 0 22px rgba(0, 0, 0, 0.45);
        }}

        .answer-card {{
            background: linear-gradient(135deg, rgba(58, 13, 16, 0.94), rgba(19, 7, 7, 0.96));
            border-left: 6px solid #c59a3d;
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 0 24px rgba(0, 0, 0, 0.55);
        }}

        .answer-card h2 {{
            color: #f6d98b;
            margin-top: 0;
        }}

        .answer-card p, .answer-card li {{
            color: #f8edd2;
            font-size: 17px;
            line-height: 1.6;
        }}

        .source-box {{
            background: rgba(11, 5, 5, 0.88);
            border: 1px solid rgba(154, 116, 50, 0.75);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 14px;
        }}

        .source-title {{
            color: #f6d98b;
            font-weight: bold;
            font-size: 17px;
            margin-bottom: 8px;
        }}

        .source-meta {{
            color: #cdb27a;
            font-size: 14px;
            margin-bottom: 10px;
        }}

        .source-content {{
            color: #efe1bf;
            font-size: 15px;
            line-height: 1.5;
        }}

        div[data-testid="stTextInput"] input {{
            background-color: rgba(18, 7, 7, 0.95);
            color: #f8edd2;
            border: 1px solid #a8792b;
            border-radius: 12px;
            padding: 14px;
            font-size: 16px;
        }}

        div[data-testid="stTextInput"] input:focus {{
            border-color: #f4c76b;
            box-shadow: 0 0 8px rgba(244, 199, 107, 0.5);
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: rgba(18, 7, 7, 0.95);
            border: 1px solid #a8792b;
            color: #f8edd2;
            border-radius: 12px;
        }}

        .stSlider label, .stTextInput label, .stSelectbox label {{
            color: #f6d98b !important;
            font-weight: bold;
        }}

        div.stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, #7b1118 0%, #4a080d 100%);
            color: #f6d98b;
            border: 1px solid #c59a3d;
            border-radius: 14px;
            padding: 14px 20px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 0 18px rgba(0, 0, 0, 0.55);
            transition: all 0.2s ease-in-out;
        }}

        div.stButton > button:hover {{
            background: linear-gradient(135deg, #9d1721 0%, #5c0b10 100%);
            color: #fff3c4;
            border-color: #f4c76b;
            transform: translateY(-1px);
            box-shadow: 0 0 22px rgba(197, 154, 61, 0.35);
        }}

        div[data-testid="stExpander"] {{
            background: rgba(18, 7, 7, 0.88);
            border: 1px solid rgba(154, 116, 50, 0.55);
            border-radius: 14px;
            color: #f8edd2;
        }}

        div[data-testid="stExpander"] summary {{
            color: #f6d98b;
            font-weight: bold;
        }}

        .stMarkdown, .stWrite, p, label {{
            color: #f8edd2;
        }}

        h1, h2, h3 {{
            color: #f6d98b;
        }}

        .footer {{
            text-align: center;
            margin-top: 36px;
            padding: 18px;
            color: #cdb27a;
            font-size: 14px;
            border-top: 1px solid rgba(154, 116, 50, 0.45);
        }}

        .badge-row {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 24px;
        }}

        .badge {{
            background: rgba(74, 8, 13, 0.9);
            border: 1px solid #9a7432;
            color: #f6d98b;
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


@st.cache_resource
def load_pipeline():
    return RAGPipeline()


st.set_page_config(
    page_title="Grimório Inteligente",
    page_icon="📖",
    layout="wide"
)

load_custom_css()

st.markdown("<h1 class='main-title'>📖 Grimório Inteligente</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Assistente RAG para mestres e jogadores de RPG de mesa</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="badge-row">
        <span class="badge">RAG</span>
        <span class="badge">Dungeons & Dragons</span>
        <span class="badge">Busca Semântica</span>
        <span class="badge">LLM Local</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-card">
        <p>
            Consulte regras, magias, equipamentos, condições e tabelas da sua base de conhecimento.
            O Grimório recupera trechos relevantes dos documentos e gera uma resposta com fontes.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("## ⚙️ Configurações")

    category = st.selectbox(
        "Filtrar por categoria",
        [
            "todos",
            "magia",
            "equipamento",
            "condicao",
            "combate",
            "monstro",
            "regra_geral"
        ]
    )

    top_k = st.slider(
        "Quantidade de trechos recuperados",
        min_value=1,
        max_value=10,
        value=5
    )

    st.markdown("---")
    st.markdown("### 🧠 Modelos")
    st.markdown("**LLM:** `llama3.1:8b`")
    st.markdown("**Embeddings:** `BAAI/bge-m3`")
    st.markdown("**Banco vetorial:** `ChromaDB`")

    st.markdown("---")
    st.markdown("### 📌 Dica")
    st.markdown(
        "Pergunte de forma objetiva. Exemplo: "
        "`Qual o dano da magia Fireball?`"
    )


st.markdown("<div class='section-card'>", unsafe_allow_html=True)

question = st.text_input(
    "Faça sua pergunta ao Grimório:",
    placeholder="Exemplo: Qual o dano da magia Fireball?"
)

consult_button = st.button("Consultar o Grimório")

st.markdown("</div>", unsafe_allow_html=True)


if "history" not in st.session_state:
    st.session_state.history = []


if consult_button:
    if not question.strip():
        st.warning("Digite uma pergunta antes de consultar.")
    else:
        with st.spinner("O Grimório está consultando os antigos tomos..."):
            pipeline = load_pipeline()
            result = pipeline.ask(
                question=question,
                category=category,
                top_k=top_k
            )

        st.session_state.history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })


if st.session_state.history:
    last = st.session_state.history[-1]

    st.markdown(
        f"""
        <div class="answer-card">
            <h2>🕯️ Resposta do Grimório</h2>
            <p>{last["answer"].replace(chr(10), "<br>")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 📚 Fontes recuperadas")

    for index, source in enumerate(last["sources"], start=1):
        metadata = source["metadata"]

        source_name = metadata.get("source", "Fonte desconhecida")
        page = metadata.get("page", "N/A")
        category_name = metadata.get("category", "N/A")
        content_type = metadata.get("content_type", "N/A")

        with st.expander(f"Fonte {index} - {source_name} - Página {page}"):
            st.markdown(
                f"""
                <div class="source-box">
                    <div class="source-title">Fonte {index}: {source_name}</div>
                    <div class="source-meta">
                        Página: {page} |
                        Categoria: {category_name} |
                        Tipo: {content_type}
                    </div>
                    <div class="source-content">
                        {source["content"].replace(chr(10), "<br>")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


if len(st.session_state.history) > 1:
    st.markdown("## 🧾 Histórico da sessão")

    for item in reversed(st.session_state.history[:-1]):
        with st.expander(item["question"]):
            st.write(item["answer"])


st.markdown(
    """
    <div class="footer">
        Grimório Inteligente — Micro SaaS com RAG para consulta de regras de RPG de mesa
    </div>
    """,
    unsafe_allow_html=True
)
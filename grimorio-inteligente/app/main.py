import streamlit as st
from app.rag_pipeline import RAGPipeline
from app.config import LLM_MODEL_NAME
import time

st.set_page_config(
    page_title="Grimório Inteligente",
    page_icon="📖",
    layout="wide"
)

# ⭐ Cache CORRETO - só carrega uma vez
@st.cache_resource(show_spinner="Carregando modelos... Isso pode levar alguns segundos na primeira vez.")
def load_pipeline():
    start = time.time()
    pipeline = RAGPipeline()
    end = time.time()
    st.sidebar.success(f"✅ Modelos carregados em {end - start:.1f}s")
    return pipeline

# ⭐ Força o carregamento ANTES do usuário interagir
pipeline = load_pipeline()

st.title("📖 Grimório Inteligente")
st.subheader("Assistente RAG para mestres e jogadores de RPG de mesa")

st.markdown(
    """
    Faça perguntas sobre regras, magias, equipamentos, condições e tabelas da base carregada.
    O sistema responde usando recuperação semântica e mostra os trechos usados como fonte.
    """
)

with st.sidebar:
    st.header("Configurações")

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
    st.markdown("Modelo LLM: `" + LLM_MODEL_NAME +"`")
    st.markdown("Embeddings: `BAAI/bge-m3`")
    st.markdown("Banco vetorial: `ChromaDB`")

question = st.text_input(
    "Digite sua pergunta:",
    placeholder="Exemplo: Qual o dano da magia Fireball?"
)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Consultar"):
    if not question.strip():
        st.warning("Digite uma pergunta antes de consultar.")
    else:
        with st.spinner("Consultando o Grimório..."):
            # ⭐ Não chama load_pipeline() aqui - já está carregado!
            start = time.time()
            result = pipeline.ask(
                question=question,
                category=category,
                top_k=top_k
            )
            end = time.time()
            
            st.sidebar.info(f"⏱️ Consulta respondida em {end - start:.1f}s")

        st.session_state.history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })

if st.session_state.history:
    last = st.session_state.history[-1]

    st.markdown("## Resposta")
    st.write(last["answer"])

    st.markdown("## Fontes recuperadas")

    for index, source in enumerate(last["sources"], start=1):
        metadata = source["metadata"]

        with st.expander(f"Fonte {index} - {metadata.get('source')} - Página {metadata.get('page')}"):
            st.markdown(f"**Categoria:** {metadata.get('category')}")
            st.markdown(f"**Tipo:** {metadata.get('content_type')}")
            st.markdown("**Trecho recuperado:**")
            st.write(source["content"])

st.markdown("---")
st.markdown("### Histórico da sessão")

for item in reversed(st.session_state.history[:-1]):
    with st.expander(item["question"]):
        st.write(item["answer"])
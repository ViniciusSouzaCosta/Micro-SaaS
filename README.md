# Grimório Inteligente

O Grimório Inteligente é um Micro SaaS com RAG voltado para mestres e jogadores de RPG de mesa. O sistema permite consultar regras, magias, equipamentos, condições e tabelas a partir de documentos de referência, retornando respostas com fontes.

## Problema

Durante sessões de RPG, consultar regras em livros extensos pode atrasar o jogo. A aplicação resolve esse problema oferecendo uma busca semântica com geração de respostas baseada em documentos.

## Domínio

O domínio escolhido foi RPG de mesa, inicialmente com foco em D&D 5e por meio do System Reference Document.

## Base de conhecimento

A base utiliza documentos SRD disponibilizados sob licença Creative Commons Attribution 4.0 International.

## Arquitetura

Usuário → Streamlit → Pipeline RAG → ChromaDB → LLM via Ollama → Resposta com fontes

## Tecnologias

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- BAAI/bge-m3
- Ollama
- Llama 3.1 8B
- PyMuPDF
- pdfplumber

## Como instalar

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1:8b
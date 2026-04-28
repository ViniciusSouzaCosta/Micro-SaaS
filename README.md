# 📖 Grimório Inteligente  
### Micro SaaS com RAG para Consulta de Regras de RPG de Mesa

O **Grimório Inteligente** é uma aplicação web baseada em **RAG (Retrieval-Augmented Generation)** desenvolvida para auxiliar **mestres e jogadores de RPG de mesa** durante sessões.

A aplicação permite consultar rapidamente:

- magias
- regras
- condições
- equipamentos
- combate
- tabelas
- criaturas
- mecânicas do sistema

Tudo isso utilizando **busca semântica + modelo de linguagem open-source**, retornando respostas com **fonte e página do documento**.

---

# 🎯 Problema

Durante sessões de RPG, consultar livros extensos como o **SRD / Livro do Jogador** pode interromper o fluxo do jogo.

Exemplo de problemas reais:

- “Qual o dano da magia Fireball?”
- “Como funciona vantagem?”
- “Quanto custa uma longsword?”
- “O que acontece com uma criatura paralisada?”

Buscar manualmente em PDFs de centenas de páginas quebra a imersão da sessão.

O Grimório Inteligente resolve isso através de um **pipeline RAG**, permitindo consultas rápidas em linguagem natural.

---

# 🎮 Domínio Escolhido

O domínio escolhido foi **RPG de mesa**, inicialmente com foco em:

- **D&D 5e**
- **SRD 5.1 / SRD 5.2**

A escolha foi feita por ser um problema real e comum entre mestres e jogadores.

---

# 🧠 Arquitetura da Solução

```text
Usuário
   ↓
Interface Streamlit
   ↓
Pipeline RAG
   ↓
Retriever Semântico
   ↓
ChromaDB
   ↓
LLM via Ollama
   ↓
Resposta com fonte
```

---

# ⚙️ Tecnologias Utilizadas

## Backend

- Python 3.10+
- Streamlit
- ChromaDB
- Sentence Transformers
- Ollama
- PyMuPDF
- pdfplumber

## Embeddings

Modelo open-source utilizado:

```text
BAAI/bge-m3
```

## Modelo de linguagem

LLM open-source utilizado:

```text
Llama 3.1 8B
```

Executado localmente via **Ollama**.

## Banco vetorial

```text
ChromaDB
```

---

# 📚 Base de Conhecimento

A base de conhecimento é composta por:

- documentos PDF
- regras oficiais
- magias
- tabelas
- equipamentos
- condições
- regras de combate

Exemplo:

```text
data/raw/srd_5_1.pdf
```

---

# 🧩 Pipeline RAG

O sistema implementa um pipeline RAG completo.

## Etapas

### 1. Ingestão

Leitura de arquivos:

- PDF
- TXT (extensível)
- HTML (extensível)

---

### 2. Pré-processamento

Extração de:

- texto
- tabelas
- páginas
- metadados

---

### 3. Chunking

Estratégia utilizada:

```text
1800 caracteres
overlap = 250
```

### Justificativa

Essa estratégia preserva contexto suficiente para regras maiores e evita perda de semântica entre páginas.

Tabelas são convertidas para **Markdown** antes da indexação.

Exemplo:

```markdown
| Weapon | Cost | Damage |
|---|---|---|
| Longsword | 15 gp | 1d8 |
```

---

### 4. Embeddings

Modelo:

```text
BAAI/bge-m3
```

Motivo da escolha:

- open-source
- multilíngue
- excelente para busca semântica
- ótimo para perguntas em português com base em documentos em inglês

---

### 5. Banco Vetorial

Banco utilizado:

```text
ChromaDB
```

---

### 6. Recuperação Semântica

A busca é feita por similaridade vetorial.

Exemplo:

```text
top_k = 5
```

---

### 7. Geração

LLM:

```text
llama3.1:8b
```

Executado localmente com:

```text
Ollama
```

---

# 🗂 Estrutura do Projeto

```text
grimorio-inteligente/
│
├── app/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── generator.py
│   ├── prompts.py
│   └── config.py
│
├── ingestion/
│   ├── extract_text.py
│   ├── extract_tables.py
│   ├── chunking.py
│   └── build_index.py
│
├── evaluation/
│   ├── questions.json
│   └── evaluate_retrieval.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── chunks/
│
├── vectorstore/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Como Rodar o Projeto

---

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/grimorio-inteligente.git
cd grimorio-inteligente
```

---

## 2. Criar ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Instalar Ollama

Instale o Ollama no sistema.

Depois execute:

```bash
ollama pull llama3.1:8b
```

---

## 5. Adicionar documentos

Coloque os PDFs na pasta:

```text
data/raw/
```

Exemplo:

```text
data/raw/srd_5_1.pdf
```

---

## 6. Processar os documentos

Execute os scripts na seguinte ordem:

---

### Extrair texto

```bash
python -m ingestion.extract_text
```

---

### Extrair tabelas

```bash
python -m ingestion.extract_tables
```

---

### Criar chunks

```bash
python -m ingestion.chunking
```

---

### Criar índice vetorial

```bash
python -m ingestion.build_index
```

---

## 7. Rodar a aplicação

```bash
streamlit run app/main.py
```

---

## 8. Abrir no navegador

```text
http://localhost:8501
```

---

# 💬 Exemplos de Perguntas

```text
Qual o dano da magia Fireball?
```

```text
Como funciona vantagem e desvantagem?
```

```text
Quanto custa uma longsword?
```

```text
O que acontece com uma criatura paralisada?
```

```text
Como funciona death saving throw?
```

---

# 📊 Avaliação da Solução

A avaliação foi realizada em duas partes.

---

## 1. Avaliação da Recuperação

Métricas:

```text
Precisão@3
Precisão@5
```

Exemplo:

```text
Precisão@3 = 0.80
Precisão@5 = 1.00
```

---

## 2. Avaliação Manual

Critérios:

- correção
- clareza
- fidelidade ao contexto
- fonte exibida

Exemplo:

| Pergunta | Nota |
|---|---:|
| Fireball | 5 |
| Paralyzed | 5 |
| Longsword | 4 |

---

# ⚠️ Limitações

- depende da qualidade do PDF
- algumas tabelas complexas podem falhar
- perguntas fora da base podem não ser respondidas
- não substitui interpretação do mestre

---

# 🔍 Casos de Falha

Exemplo:

```text
Qual a melhor build para derrotar um dragão?
```

Esse tipo de pergunta exige estratégia e opinião, não regra oficial.

O sistema deve responder:

```text
Não encontrei essa informação na base carregada.
```

---

# 📌 Diferenciais Técnicos

- pipeline RAG completo
- modelo open-source
- embeddings open-source
- banco vetorial
- extração de tabelas
- chunking com overlap
- metadata por categoria
- resposta com fonte

---

# 🏆 Requisitos Atendidos

✔ Pipeline RAG  
✔ Modelo open-source  
✔ Interface utilizável  
✔ Banco vetorial  
✔ Avaliação  
✔ Documentação  
✔ Repositório organizado  

---

# 📄 Licença e Atribuição

Este projeto utiliza conteúdo do **System Reference Document (SRD)** disponibilizado sob licença:

```text
Creative Commons Attribution 4.0 International
```

Atribuição obrigatória mantida conforme documentação oficial.

---

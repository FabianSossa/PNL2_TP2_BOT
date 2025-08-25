# RAG Chatbot (Flask + LangChain)

Este proyecto implementa un **Retrieval-Augmented Generation (RAG)** sencillo inspirado en el repo `ezeguins/chatbot`,
pero usando dependencias modernas de LangChain. Por defecto usa **Chroma** como vector store local (sin coste)
y permite alternar a **Pinecone** con variables de entorno.

## Estructura
```
.
├── app.py                 # Servidor Flask + cadena RAG con memoria de sesión
├── ingest.py              # Indexa documentos de ./docs al vector store
├── templates/
│   └── index.html         # UI mínima del chat
├── static/
│   └── style.css          # Estilos del frontend
├── storage/               # Persistencia de Chroma (auto-creada)
├── docs/                  # Coloca aquí tus PDFs/MD/TXT
├── requirements.txt
└── .env.example
```

## Requisitos
- Python 3.10+
- Cuenta/OpenAI API key (para `gpt-4o-mini` o el modelo que prefieras).

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # edita las claves
```

## Ingesta de documentos
Coloca tus archivos en `./docs` (PDF, TXT, MD). Luego ejecuta:
```bash
python ingest.py
```

## Ejecutar el servidor
```bash
flask --app app.py --debug run  # http://127.0.0.1:5000
```
o
```bash
python app.py
```

## Cambiar a Pinecone (opcional)
En `.env` define:
```
VECTOR_STORE=pinecone
PINECONE_API_KEY=...
PINECONE_INDEX=rag-chatbot
PINECONE_ENV=us-east-1
PINECONE_NAMESPACE=default
```
Ejecuta `python ingest.py` para reindexar en Pinecone y luego corre `app.py`.

## Notas
- El historial de conversación se mantiene por `session_id` (cookie).
- Ajusta los parámetros del *TextSplitter* y del *retriever* según el tamaño de tus documentos.

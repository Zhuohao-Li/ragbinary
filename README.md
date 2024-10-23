# ragbinary

How to run with `your prompt`:

`python query_data.py '<your prompt>'`, it will give your `k` (configurable) relevant items from DB and answer your prompts

Others:

`create_database.py` is for building our VectorDB using Chroma for RAG

You can check langchain API in [langchain](https://api.python.langchain.com/en/latest/vectorstores/langchain_core.vectorstores.VectorStore.html) document.

You need a `export OPENAI_KEY_API=<look at messages in our slack>` for getting access to GPT


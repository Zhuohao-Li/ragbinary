# ragbinary

How to run with `your prompt`:

`python query_data.py '<your prompt>'`, it will give your `k` (configurable) relevant items from DB and answer your prompts

## Usage:

```
usage: query_data.py [-h] [--query_bulk QUERY_BULK] [--query_bulk_prefix QUERY_BULK_PREFIX] [--query_bulk_suffix QUERY_BULK_SUFFIX] [--query_text QUERY_TEXT] [--output OUTPUT]

Queries the Chrome Database to Check for similarity

options:
  -h, --help            show this help message and exit
  --query_bulk QUERY_BULK
                        Provide the CSV filename to query in Bulk
  --query_bulk_prefix QUERY_BULK_PREFIX
                        The prefix to add to each query from the csv
  --query_bulk_suffix QUERY_BULK_SUFFIX
                        The suffix to add to each query from the csv
  --query_text QUERY_TEXT
                        The query text.
  --output OUTPUT       The output filename to store the results to.
```

NOTE: Query Bulk requires the field with in the CSV to be `query_text`

Others:

`create_database.py` is for building our VectorDB using Chroma for RAG

# updated with contextual RAG

You can check langchain API in [langchain](https://api.python.langchain.com/en/latest/vectorstores/langchain_core.vectorstores.VectorStore.html) document.

You need a `export OPENAI_KEY_API=<look at messages in our slack>` for getting access to GPT


import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

os.environ['OPENAI_API_KEY'] = "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"


CHROMA_PATH = "./contextual_rag/chroma"
# chroma helps to build a vectorDB

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def parse():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    return query_text

def retrieve_db(query_text):
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=20)
    return results
    
def print_scores(results):
    similarity_scores = [score for _, score in results]
    print(similarity_scores)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

def wrapper_function(csv_path):
    df = pd.read_csv(csv_path)
   
    results_dict = {}

    for index, row in df.iterrows():
        query_text = row['query_text']        
        results = retrieve_db(query_text=query_text)     
        similarity_scores = print_scores(results)
        results_dict[query_text] = similarity_scores
    
    return results_dict

def main():
    query_text = parse()
    results = retrieve_db(query_text=query_text)
    print_scores(results)

    csv_path = parse()
    results_dict = wrapper_function(csv_path=csv_path)
    for query, scores in results_dict.items():
        print(f"Query: {query} -> Similarity Scores: {scores}")


    # context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    # model = ChatOpenAI()
    # response_text = model.predict(prompt)


    # sources = [doc.metadata.get("source", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)


if __name__ == "__main__":
    main()

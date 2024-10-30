import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import pandas as pd


CHROMA_PATH = "./chroma"
# chroma helps to build a vectorDB

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def parse():
    # Create CLI.
    parser = argparse.ArgumentParser(
            prog="query_data.py",
            description="Queries the Chrome Database to Check for similarity",
            )
    parser.add_argument("--query_bulk", type=str, help="Provide the CSV filename to query in Bulk")
    parser.add_argument("--query_text", type=str, help="The query text.")
    parser.add_argument("--output", type=str, help="The output filename to store the results to.")
    args = parser.parse_args()
    return args

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
    return similarity_scores

def csv_similarity(csv_path):
    df = pd.read_csv(csv_path)
   
    results_dict = {}

    for index, row in df.iterrows():
        query_text = row['query_text']        
        results = retrieve_db(query_text=query_text)     
        similarity_scores = print_scores(results)
        results_dict[query_text] = similarity_scores
    
    return results_dict

def save_results_to_file(results, filename):
    with open(filename, "w+") as file:
        file.write(results)

def main():
    arguments = parse()
    if arguments.query_bulk:
        csv_path = arguments.query_bulk
        results_dict = csv_similarity(csv_path=csv_path)
        if arguments.output:
            save_results_to_file(json.dumps(results_dict), arguments.output)
        else:
            for query, scores in results_dict.items():
                print(f"Query: {query} -> Similarity Scores: {scores}")
    if arguments.query_text:
        query_text = arguments.query_text
        results = retrieve_db(query_text=query_text)
        similarity_scores = print_scores(results)
        if arguments.output:
            save_results_to_file(", ".join([str(i) for i in similarity_scores]), arguments.output)
        else:
            print_scores(results)
        
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        # print(prompt)

        model = ChatOpenAI()
        response_text = model.predict(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)


if __name__ == "__main__":
    main()

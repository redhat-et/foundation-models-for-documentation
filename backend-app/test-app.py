from document_retrieval import DocumentRetrieval
from answer_generation import AnswerGeneration
import argparse
import json
import os
from dotenv import load_dotenv, find_dotenv


if __name__ == "__main__":

    def answer(prompt, query):
        # Get top candidates
        config_path = './config.json'
        retrieval = DocumentRetrieval(config_path)
        top_candidates, sources = retrieval.search_candidates(query)
        sources = "\n".join(sources)
        print(sources)
        print("Top Candidates:")
        for idx, candidate in enumerate(top_candidates):
            print(f"{idx + 1}: {candidate}")

        # Get answers
        generation = AnswerGeneration(retrieval.vector_store,
                                        'llama2')
        generation.prompt = prompt
        # If you want to change the model prompt, it is in prompt.py file
        answer = generation.generate(query, top_candidates)
        answer = answer.strip("\"")
        
        print(f"Final answer: \n {answer}")
        return generation.prompt, sources, answer
    
    load_dotenv(find_dotenv("credentials.env"), override=True)
    parser = argparse.ArgumentParser(description="Document search and answer generation")
    parser.add_argument("--query", required=True, help="Enter your query about the ROSA service")
    parser.add_argument("--prompt", required=True, help="Enter the prompt file")
    args = parser.parse_args()
    with open(args.prompt, 'r') as pf:
        prompt = pf.read()
    prompt, sources, query_answer = answer(prompt, args.query)
    data_json = {"prompt": prompt,
                 "query": args.query,
                 "sources":sources,
                 "answer":query_answer}
    prompt_file = args.prompt.split('/')[1]
    result_file = f"{prompt_file[:-4]}.json"
    file_name = f"results/{result_file}"
    try:
        # Read the existing data from the JSON file
        with open(file_name, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist, creating a new file...")
        existing_data = []
    existing_data.append(data_json)
    with open(file_name, 'w') as json_file:
        json.dump(existing_data, json_file)







        

        

        
    
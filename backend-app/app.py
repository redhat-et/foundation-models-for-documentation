from document_retrieval import DocumentRetrieval
from answer_generation import PROMPT_TEMPLATE, AnswerGeneration
import gradio as gr
import argparse

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Document search and answer generation")
    # parser.add_argument("--query", required=True, help="Enter your query about the ROSA service")
    # args = parser.parse_args()

    def answer(query):
            config_path = './config.json'
            retrieval = DocumentRetrieval(config_path)
            top_candidates = retrieval.search_candidates(query)
            print("Top Candidates:")
            for idx, candidate in enumerate(top_candidates):
                print(f"{idx + 1}: {candidate}")
            generation = AnswerGeneration(retrieval.vector_store,
                                          'text-davinci-003')
            answer = generation.generate(query,
                                top_candidates,
                                PROMPT_TEMPLATE)
            print(f"Final answer: \n {answer}")
            return answer
    
    #answer("What is ROSA?")
        
    demo = gr.Interface(fn=answer,
                        inputs="text",
                        outputs="text")
    
    demo.launch(server_name="0.0.0.0",
                server_port=8080
                )   


        

        

        
    
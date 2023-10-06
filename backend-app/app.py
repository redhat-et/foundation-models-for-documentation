from document_retrieval import DocumentRetrieval
from answer_generation import PROMPT_TEMPLATE, AnswerGeneration
import gradio as gr

if __name__ == "__main__":
    def answer(query):
            config_path = './config.json'
            retrieval = DocumentRetrieval(config_path)
            top_candidates, sources = retrieval.search_candidates(query)
            print(sources)
            print("Top Candidates:")
            for idx, candidate in enumerate(top_candidates):
                print(f"{idx + 1}: {candidate}")
            generation = AnswerGeneration(retrieval.vector_store,
                                          'text-davinci-003')
            answer = generation.generate(query,
                                top_candidates,
                                PROMPT_TEMPLATE)
            print(f"Final answer: \n {answer}")
            return "\n".join(sources), answer.strip("\"")

    application_description = """
    * The application is a workbench to consume results of a quesiton answering system designed around public ROSA documents.\n
    * It uses retrieval-augmenented generation (document retrieval and text generation) to produce the final results. \n 
    * It should be used internally as a platform for the stakeholders to engage with the proof-of-concept and provide feedback. \n
    * The questions and the responses of the model will be recorded for feedback collection. """

    title = "ROSA Documentation Questions & Answers"

    demo = gr.Interface(fn=answer,
                        inputs=gr.Textbox(label="Question"),
                        outputs=[gr.Textbox(label="Candidate documents",
                                            lines=2,
                                            placeholder="Links"),
                                 gr.Textbox(label="Answer",
                                            lines=2,
                                            placeholder="Answer")],
                        theme=gr.themes.Base(),
                        title=title,
                        description=application_description)
    
    demo.launch(server_name="0.0.0.0",
                server_port=8080
                )   


        

        

        
    
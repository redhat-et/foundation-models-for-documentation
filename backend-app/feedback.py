import argilla as rg
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv("credentials.env"), override=True)

class FeedbackCollection:
    def __init__(self, dataset_name, workspace, create=False):
            # Setup connection with the Argilla instance
            rg.init(api_url=os.getenv("ARGILLA_API_URL"),
                    api_key=os.getenv("ARGILLA_API_KEY"))
            
            if create:
                 self.dataset = self.create_dataset_template()
                 self.dataset.push_to_argilla(name=dataset_name,
                                              workspace=workspace)
                 
            self.dataset = rg.FeedbackDataset.from_argilla(name=dataset_name,
                                                           workspace=workspace)
            
            
    def create_dataset_template(self):
        # Create an example feedback dataset schema, and feedback template
        dataset_template = rg.FeedbackDataset(
            guidelines="Please read the feedback questions and answer as accurately as possible. Your answers will be used to improve the application.",
            fields=[
                 rg.TextField(name="prompt", title="Human prompt", required=True),
                 rg.TextField(name="documents", title="Candidate documents"),
                 rg.TextField(name="output", title="Generated output", use_markdown=True)
            ],
            questions=[
                rg.TextQuestion(
                    name="document_retrieval_feedback",
                    title="Are there any missing candidate documents that contain the answer to the query?",
                    required=True,
                ),
                rg.RatingQuestion(
                    name="response_quality_likert_scale",
                    title="Rate the quality of the response:",
                    description="Rate the response's correctness and helpfulness, with 1 indicating it's completely useless/incorrect, and 5 meaning it's entirely helpful/correct.",
                    values=[1, 2, 3, 4, 5],
                    required=True,
                ),
                rg.TextQuestion(
                    name="rewrite_response",
                    title="What should be the exact response of the query? Please modify or recreate the generated answer:",
                    required=True,
                ),
                rg.TextQuestion(
                    name="additional_comments",
                    title="Are there any additional comments or suggestions for the application?",
                    required=False,
                )
            ])
        return dataset_template
    
    def add_record(self, prompt, candidates, response):
         # Create a record object
        record = rg.FeedbackRecord(
            fields={
                "prompt": prompt,
                "documents": candidates,
                "output": response
            })
        self.dataset.add_records(record)
        return record
         

         
         
          
          







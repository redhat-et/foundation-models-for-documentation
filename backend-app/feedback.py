import argilla as rg
import os

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
        guidelines="Answer the following questions based on your experience",
        fields=[
            rg.TextField(name="prompt", title="Human prompt"),
            rg.TextField(name="documents", title="Candidate documents"),
            rg.TextField(name="output", title="Generated output", use_markdown=True)
        ],
        questions =[
            rg.RatingQuestion(
                name="rating",
                title="Rate the quality of the response:",
                description="1 = very bad - 5= very good",
                required=True,
                values=[1,2,3,4,5]
            ),
            rg.TextQuestion(
                name="corrected-text",
                title="Provide a correction to the response:",
                required=False,
                use_markdown=True
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
         

         
         
          
          







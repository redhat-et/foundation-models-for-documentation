from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.prompts.prompt import PromptTemplate

PROMPT_TEMPLATE = """
As an engineer generating answers for questions around the
Red Hat Openshift Service on AWS (ROSA) product, the goal is
to generate answers from the given context. Do not make up answers and stick to the context. 
If you don't know the answer, please respond with: "I don't know"

Here are a few input, context, and output pairs examples to guide the model:

Question: "What is Red Hat OpenShift Service on AWS (ROSA)?"
Context: # Getting support for Red Hat OpenShift Service on AWS

Get support for Red Hat OpenShift Service on AWS (ROSA).

# Red Hat OpenShift Service on AWS - FAQ

## General

### What is Red Hat OpenShift Service on AWS (ROSA)?
Red Hat Openshift Service on AWS (ROSA) is a fully-managed turnkey application platform that allows
you to focus on what matters most, delivering value to your customers by building and deploying applications.
Red Hat SRE experts manage the underlying platform so you don’t have to worry about the complexity of infrastructure management.

### Where can I go to get more information/details?
- [ROSA Webpage](https://www.openshift.com/products/amazon-openshift)
- [ROSA Workshop](https://www.rosaworkshop.io)
- [ROSA Documentation](https://docs.openshift.com/rosa/welcome/index.html)

Additional key features of Red Hat OpenShift Service on AWS:

You can quickly create a Red Hat OpenShift Service on AWS (ROSA) cluster with the AWS Security Token Service (STS) by using the default installation options. The following summary describes the default cluster specifications.
Answer: "Red Hat Openshift Service on AWS (ROSA) is a fully-managed turnkey application platform that allows
you to focus on what matters most, delivering value to your customers by building and deploying applications.
Red Hat SRE experts manage the underlying platform so you don’t have to worry about the complexity of infrastructure management."


Question: {question}
Context: {context}
Answer:
"""

class AnswerGeneration:
    def __init__(self, vector_store, model_name):
        load_dotenv(find_dotenv("credentials.env"),
            override=True)
        self.vector_store = vector_store
        self.model = OpenAI(model=model_name, temperature=0)

    
    def _get_prompt(self, prompt_template):
        prompt = PromptTemplate(
            input_variables=["question", "context"],
            template=prompt_template)
        return prompt
        
    def generate(self,
                 query,
                 candidate_docs,
                 prompt_template,
                 chain_type="stuff"):
        
        prompt = self._get_prompt(prompt_template)
        chain = load_qa_chain(self.model,
                              chain_type=chain_type,
                              prompt=prompt)
        ## Generate answer
        answer = chain({"input_documents": candidate_docs,
                        "question": query},
                       return_only_outputs=True)
        
        return answer['output_text']
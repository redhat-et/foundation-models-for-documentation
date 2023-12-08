The readme contains description of experiment notebooks in this repository.

* [QA_extraction_generation.ipynb](./QA_extraction_generation.ipynb): This notebook uses [Hugging Face's transformers package](https://huggingface.co/docs/transformers) to experiment with extractive and generative question answering with ROSA docs. 
* [haystack-qa.ipynb](./haystack-qa.ipynb) explores the [Haystack framework](https://haystack.deepset.ai/) for question answering, both extractive and generative (with two different versions for that: a local seq2seq model and one based in the [OpenAI API](https://platform.openai.com/docs/introduction)).
* [create-validation-dataset.ipynb](create-validation-dataset.ipynb): reads the FAQ questionnaire from the ROSA workshop documents and creates a fine-tuning or validation dataset for text generation models.
* [langchain-openai.ipynb](langchain-openai.ipynb) explores the [langchain framework](https://python.langchain.com/en/latest/index.html) that helps develop with large language models for various tasks including [question answering](https://langchain.readthedocs.io/en/latest/modules/indexes/chain_examples/question_answering.html).
* [langchain-pipeline-rosa.ipynb](langchain-pipeline-rosa.ipynb) illustrates the same [LangChain](https://python.langchain.com/en/latest/index.html) worflow of prompt-engineering for ROSA question answering, but using a [Hugging Face](https://huggingface.co) model running locally, instead of accessing a remote model via an API.
* [langchain-api-client.ipynb](langchain-api-client.ipynb) defines a simple wrapper around a model exposed by the [text-generation-webui](https://github.com/oobabooga/text-generation-webui/) API and uses [LangChain](https://python.langchain.com/en/latest/index.html) to prompt-engineer it for ROSA question answering.
* [rosa-demo-open-ai-wfaq.ipynb](rosa-demo-open-ai-wfaq.ipynb) is a general demo of a Question Answering (QA) workflow for ROSA documentation, including vector embeddings for document search and generative answers orchestrated with LangChain. Prompt engineering is also covered. This demo uses the [OpenAI API](https://platform.openai.com/docs/introduction) for embeddings and language modeling.

## Resource utilization
* [gpu-footprint.ipynb](gpu-footprint.ipynb) computes gpu requirements of models with different number of model parameters.

## Fine tuning
* [flan-t5-3B-general-tasks](./finetune/Flan-T5-3B/general-tasks.ipynb): finetunes the flan t5 model for sentiment analysis task and text summarization task. 
* [flan-t5-3B-RosaQA](./finetune/Flan-T5-3B/RosaQA.ipynb): finetunes the flan t5 model for question answering with ROSA service documentation. It then shows before and after finetuning quality of model answers.

## Evaluation 
* [QA_evaluation_metrics_demo.ipynb](./QA_evaluation_metrics_demo.ipynb) explores evaluation metrics for LLMs in Question-Answering (QA) tasks. It covers metrics for QA as well as metrics related to model complexity and human evaluation.
* [retriever-evaluation.ipynb](./retriever-evaluation.ipynb) explores evaluation metrics for document retrieval techniques. 

## Model Serving
* [Model Serving with Ray](./model_serving/ray-serve-llm.ipynb) provides a demo for how to serve an LLM on OpenShift using a multi-GPU ray cluster. 

## Feedback

* [Argilla 101](./feedback/argilla_101.ipynb) shows how to connect with and use the Argilla instance on the cluster.
* ["Collect application feedback using Argilla](./feedback/Collect-application-feedback-using-Argilla.ipynb) shows how to create a feedback dataset and involve annotators for your project.

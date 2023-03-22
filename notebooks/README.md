The readme contains description of experiment notebooks in this repository.

* [QA_extraction_generation.ipynb](./QA_extraction_generation.ipynb): This notebook uses [Hugging Face's transformers package](https://huggingface.co/docs/transformers) to experiment with extractive and generative question answering with ROSA docs. 
* [haystack-qa.ipynb](./haystack-qa.ipynb) explores the [Haystack framework](https://haystack.deepset.ai/) for question answering, both extractive and generative (with two different versions for that: a local seq2seq model and one based in the [OpenAI API](https://platform.openai.com/docs/introduction)).
* [create-validation-dataset.ipynb](create-validation-dataset.ipynb): reads the FAQ questionnaire from the ROSA workshop documents and creates a fine-tuning or validation dataset for text generation models.
* [langchain-openai.ipynb](langchain-openai.ipynb) explores the [langchain framework](https://langchain.readthedocs.io/en/latest/index.html) that helps develop with large language models for various tasks including [question answering](https://langchain.readthedocs.io/en/latest/modules/indexes/chain_examples/question_answering.html).

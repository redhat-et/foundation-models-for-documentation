[Comment]: < Generated with the help of ChatGPT > 
# Large Language Models for Product Documentation Search

## Introduction

Product documentation is a crucial resource for any organization. It enables users to understand the product and its features, troubleshoot issues, and get the most out of the product. However, as product documentation grows in size and complexity, it becomes harder for users to find the information they need. This is where large language models can help.

Large Language Models (LLMs) are Machine Learning (ML) systems that are trained on vast amounts of text data. They can understand natural language and generate human-like responses to queries. In recent years, large language models like GPT-3 and BERT have shown impressive results in natural language processing tasks. They can be used for a variety of applications, including product documentation search.

Traditional search engines rely on keywords to find relevant documents. However, this approach has limitations. It can be hard to know which keywords to use, and it may not capture the nuances of natural language. LLMs, on the other hand, can understand natural language queries and take into account the user's intent. This means that users can ask questions in a natural way, and the model will understand what they mean. For example, a user might ask "How many nodes can I have in my ROSA cluster?" and the model can provide the answer with links to relevant documentation.

In this repository we will explore how large language models can be used to improve product documentation search. Our goal is to demonstrate the potential for leveraging foundation models to create an interactive, conversational interface that ROSA customers or potential clients can use to access helpful tips and information, in addition to providing comprehensive technical documentation.

### How Large Language Models Work

LLMs are based on deep learning algorithms which enable them to understand and generate natural language. They are trained on massive datasets of text, such as books, articles, and websites. During training, the model learns to recognize patterns in the data and make predictions based on those patterns.

Once the model is trained, it can be used for a variety of natural language processing tasks. For example, it can be used to generate text, answer questions, or classify text based on its content.

LLMs can be used directly, in which case they will make use of their capabilities for general language processing to generate meaningful text from a certain input (a question, a request). However, these models lack specific factual knowledge of specialized areas, which means that they are likely unable to address questions that are asked about non-general topics. Even worse, LLMs are prone to generate wrong answers, especially in this type of context.

On the other hand, LLMs can adapted to specific needs and/or knowledge areas. There are various mechanisms to do that, depending on the goal and the task at hand.

Due to their adaptability, LLMs are a type of ML model called Foundation Models, as they can serve as a building block for additional, specialized model development.

The goal of this repository is to explore the options available for that adaptation process, and to provide guidance and recommendations on how to perform these tasks in general, and to apply them to specific concrete cases that can highlight useful applications.

# Repo structure

- `data`: `The data/external` directory contains our initial example ROSA docs for training.
- `notebooks`: The experiment notebooks and their details are in the notebooks [README.](notebooks/README.md)

# References

[Open Source and other Question answering Implementations](https://github.com/redhat-et/foundation-models-for-documentation/issues/9)

[Metrics and evaluation](https://github.com/redhat-et/foundation-models-for-documentation/issues/2)

# How to use

## requirements.txt
Install these requirements in your environment.

## Config.json
Update the config file with the path to the documents, the vector database, the embedding model name, etc.

## credentials.env
The current version uses openai model that requires the OPEN_API_KEY in a credentials.env file.  

## Running
Get candidates and final answer by running the app.py file in your terminal with the query as the command line argument.
`app.py --query "What is ROSA?"`

You should see something like this:
```
Top Candidates:

1: page_content='## How does ROSA use STS?' metadata={'source': '../data/external/rosaworkshop/15-sts_expla
2:
...

Final answer: 

 "ROSA is a fully-managed, turnkey application platform that allows you to focus on delivering value to your customers by building and deploying applications. Red Hat and AWS Site reliability engineering (SRE) experts manage the underlying platform so you do not have to worry about the complexity of infrastructure management. ROSA provides seamless integration with a wide range of AWS compute, database, analytics, machine learning, networking, mobile, and other services to further accelerate the building and delivering of differentiating experiences to your customers."
```

If the application doesn't find the vector database collection in your specified path in `config.json`, it will create a new collection at the same path. This operation takes several hours to finish. 
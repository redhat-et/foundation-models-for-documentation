# How to use

## Openshift Deployment
* Go to the developer view of your Openshift cluster
* Select `import from git` option for an automatic deloyment
* Set git repository to `https://github.com/redhat-et/foundation-models-for-documentation` and the context directory to `backend-app`
* Click on `submit` and wait for s2i to build the image
* Check `routes` for the link to the deployed application 
* Set the api keys in the deployment environment variables
* Coming soon: yaml files for deployment

# Running locally 
## requirements.txt
Install these requirements in your environment.

## Config.json
Update the config file with the path to the documents, the vector database, the embedding model name, etc.

## credentials.env
The current version uses openai model that requires the OPEN_API_KEY in a credentials.env file.  

## Running the application
Run the app.py file in your terminal:
`python3 app.py`

You will see the application running at `0.0.0.0:8080`. You can change the hostname and the port in the app.py file. 

In the UI, give a query such as "What is ROSA?" to get responses like:
```
Candidate documents:

1: page_content='## How does ROSA use STS?' metadata={'source': '../data/external/rosaworkshop/15-sts_expla
2:
...

Answer: 

 "ROSA is a fully-managed, turnkey application platform that allows you to focus on delivering value to your customers by building and deploying applications. Red Hat and AWS Site reliability engineering (SRE) experts manage the underlying platform so you do not have to worry about the complexity of infrastructure management. ROSA provides seamless integration with a wide range of AWS compute, database, analytics, machine learning, networking, mobile, and other services to further accelerate the building and delivering of differentiating experiences to your customers."
```

If the application doesn't find the vector database collection in your specified path in `config.json`, it will create a new collection at the same path. This operation takes several hours to finish. 
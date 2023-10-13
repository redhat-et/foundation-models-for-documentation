# Deploy self-hosted Llama2 model on OpenShift with Ray

## PreReqs:

* OpenShift Cluster
* NFD Operator
* Nvidia Operator
* KubeRay Operator
* OpenShift Node with a g5.2xlarge instance running


## Deployment Instructions

### Assumptions + Extra Preperation Steps

This deployment makes a few assumption about your cluster. All of which are outlined below. If these are not accurate for your cluster they can be changed directly in the manifests contained in `model_deployment/base/`:
* The namespace we will deploy our model to is called `opendatahub`.
* The user has a [huggingface.co](https://huggingface.co/) api token that can be used to access llama2 models and it has been added as a secret in the `opendatahub` namespace. See [secrets.yaml](model_deployment/base/secrets.yaml) for additional details.  
* The user is expected to update the environment variables `RAY_CLIENT_URI` and `RAY_DASHBOARD_URI` in [deployment.yaml](model_deployment/base/deployment.yaml) to match the namespace and server address they are using. 
 

### Create Kustomize Deployment

Once all your manifests are updated to meet the needs of your specific cluster, you need to create the model deployment yaml. 

```bash
oc kustomize manifests/ray-serve-llama/model_deployment/base > model_deployment.yaml
```
This will create a single yaml file containing all the resources needed to deploy the model on your cluster. You can then deploy it using the following `oc` command.

```bash
oc apply -f model_deployment.yaml
```


It will a couple of minutes for the model to deploy. Once deployed you should be able to test it out and confirm its working running the below python code. 

```python
import requests

response = requests.get("http://llama2service-opendatahub.apps.<YOUR-SERVER-ADDRESS>",
                        params={"text": "What is the purpose of AI?"})

print(response.content)
```





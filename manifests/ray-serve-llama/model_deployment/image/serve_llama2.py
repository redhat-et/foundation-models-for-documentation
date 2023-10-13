
import os
import requests
from typing import Dict
from fastapi import FastAPI
from starlette.requests import Request
from transformers import pipeline
import torch
import ray
from ray import serve
import time



hf_token = os.getenv("HF_API_TOKEN", None)
address = os.getenv("RAY_CLIENT_URI", None)
model_name = os.getenv("MODEL_NAME","meta-llama/Llama-2-7b-chat-hf")
dashboard=os.getenv("RAY_DASHBOARD_URI", None)

while requests.get(dashboard).status_code != 200:
    time.sleep(3)
    print("Waiting for ray cluster to start")

runtime_env = {"pip": ["transformers", "accelerate"]}
ray.shutdown()
ray.init(address=f"ray://{address}:10001", runtime_env=runtime_env)
print("Ray cluster is up and running: ", ray.is_initialized())


@serve.deployment(num_replicas=1, ray_actor_options={"num_gpus":1, "num_cpus":4})
class RayServeDeployment:
    def __init__(self):
        self._model = pipeline("text-generation", model=model_name, 
                               torch_dtype= torch.float16, device_map="auto", token=hf_token,
                              num_return_sequences=1)

    def __call__(self, request: Request) -> Dict:
        response = self._model(request.query_params["text"])[0]["generated_text"]
        return response

serve.run(RayServeDeployment.bind(), host="0.0.0.0")
print("Model is Served!")
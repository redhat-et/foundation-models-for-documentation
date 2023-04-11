# OpenShift manifests

## Text generation web UI

The [text-generation-webui.yaml](./text-generation-webui.yaml) manifest builds and deploys [oobabooga's text generation webui](https://github.com/oobabooga/text-generation-webui/), a Gradio app for running Large Language Models.

The manifest includes:

- a `BuildConfig` to build an image from the repo, using s2i Python
- a `Deployment` to deploy the built image
- a `Service` and a `Route` to expose it

### Requirements

#### Persistent storage for the models

The manifest includes a `PersistentVolumeClaim` (PVC) definition, called `llms`. This is where the models are stored.

That PVC must be populated with the models to serve, one per directory.

**NOTE**: the provided `Deployment` is currently hardcoded to start up with `bloom-1b7`, so make sure to at least download that model into the PVC, or adjust the `Deployment` definition according to the models you have.

One way to populate the PVC is to use the [download-model.py script](https://github.com/oobabooga/text-generation-webui/blob/main/download-model.py) from the text-generation-webui repository:

1. Wait for your application's Pod to start up
2. Access your pod (either from the web console or via e.g. `oc rsh`). *Note*: if the pod is failing/restarting due to the lack of pre-loaded models you can use `oc debug` to create a temporary clone of the pod and perform the model download there
3. `cd models`
4. `python download-model.py bigscience/bloom-1b7`

Repeat step 4 to download all the models you want. Here are the contents of a sample PVC after a few model downloads:

```
(app-root) sh-4.4$ cd models
(app-root) sh-4.4$ ls *
bloom-1b7:
config.json  model.safetensors  README.md  special_tokens_map.json  tokenizer_config.json  tokenizer.json

gpt2:
config.json  generation_config.json  merges.txt  model.safetensors  README.md  tokenizer.json  vocab.json

lost+found:

opt-1.3b:
config.json  generation_config.json  LICENSE.md  merges.txt  pytorch_model.bin  README.md  special_tokens_map.json  tokenizer_config.json  vocab.json

opt-2.7b:
config.json  generation_config.json  merges.txt  pytorch_model.bin  README.md  special_tokens_map.json  tokenizer_config.json  vocab.json
```

#### GPU

The `Deployment` also assumes that there is a GPU available in the cluster, and will only work if that is available.

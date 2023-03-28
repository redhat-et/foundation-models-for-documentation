# OpenShift manifests

## Text generation web UI

The [text-generation-webui.yaml](./text-generation-webui.yaml) manifest builds and deploys [oobabooga's text generation webui](https://github.com/oobabooga/text-generation-webui/), a Gradio app for running Large Language Models.

The manifest includes:

- a `BuildConfig` to build an image from the repo, using s2i Python
- a `Deployment` to deploy the built image
- a `Service` and a `Route** to expose it

### Requirements

**IMPORTANT** about model persistence: the manifest does **NOT** include a `PersistentVolumeClaim` definition. However, the included `Deployment` assumes that a PVC called `llms` exists, and it is expected to be populated with the models to serve, one per directory. The `Deployment` expects to start up with `bloom-1b7`.

This means that in order to use this, a PVC named `llms` **must be created** first with the appropriate content.

Also, the `Deployment` also assumes that there is a GPU available in the cluster, and will only work if that is available.

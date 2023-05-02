# Red Hat OpenShift Data Science (RHODS) FAQ

## Executive Summary: Top 10 Questions

### What is Red Hat OpenShift Data Science?

Red Hat OpenShift Data Science gives data scientists and developers a powerful AI/ML platform for building intelligent applications. Teams can quickly move from experiment to production in a collaborative, consistent environment with their choice of certified tools. OpenShift Data Science is offered as an add-on cloud service to OpenShift Dedicated (AWS and GCP) and OpenShift Service on AWS (ROSA) or as a self-managed software offering for on-premise and cloud deployments.  OpenShift Data Science combines Red Hat components, open source software, and integrated technology partner offerings in a single, integrated offering.

### What is Open Data Hub?

Open Data Hub (opendatahub.io) is a blueprint for building an AI as a service platform on Red Hat OpenShift®  and select portfolio products like Red Hat Ceph Storage and Red Hat AMQ Streams. It inherits from upstream efforts such as Jupyter and Kubeflow, and is the foundation for Red Hat's own internal data science and AI platform. In the Open Data Hub service, data scientists can select from popular tools such as Jupyter Notebooks, PyTorch, TensorFlow™, scikit-learn, Apache Spark™ and more for developing and maintaining models.

### How is Red Hat OpenShift Data Science different from Open Data Hub?

Red Hat OpenShift Data Science (RHODS) is the commercial offering of the upstream Open Data Hub (ODH) project. RHODS offers a carefully designed UX and contains a subset of the tools currently available in the ODH project - including Jupyter, ML frameworks like TensorFlow and PyTorch, model serving, and initial model monitoring. Red Hat provides regular updates to the open source tools, taking that burden off of the customer.

### How will Red Hat OpenShift Data Science be offered to customers?  On what platforms will it be offered?

Red Hat OpenShift Data Science is offered as an add-on managed cloud service to OpenShift Dedicated (OSD) for AWS and GCP alike and OpenShift Service on AWS as well as a self-managed software product to run on top of OpenShift Container Platform.

### How can customers purchase and access it?

OpenShift Data Science is available for purchase worldwide.  It is available in yearly and consumption-based SKUs on the Red Hat price book.  Customers can also use their committed spend to purchase and run the cloud service option of Red Hat OpenShift Data Science directly from the AWS Marketplace ([North America](https://aws.amazon.com/marketplace/pp/prodview-co7uaxdm7qnkq?sr=0-1&ref_=beagle&applicationId=AWSMPContessa), [EMEA](https://aws.amazon.com/marketplace/pp/prodview-fuxkweo2tdmr2)).

Customers can also try out RHODS for free in the [Developer Sandbox](https://developers.redhat.com/developer-sandbox/activities/use-rhods-to-master-nlp).

### Is an on-prem option to OpenShift Data Science be offered?

A self-managed version of Red Hat OpenShift Data Science has become GA in January 2023.

### What are some of the Red Hat, upstream open source and commercial ISV tools that are offered in the current version of Red Hat OpenShift Data Science?

Red Hat OpenShift Data Science currently includes the following technology partner and Red Hat offerings integrated into the user interface dashboard.  The integrated partner software or SaaS offering can be purchased directly from the partners  For several of the partner offerings, a trial license can be enabled directly from the RHODS UI.

* Data Science & model development and experimentation:
  * Open Source:  JupyterLab UI. Out-of-the-box notebook images with common Python libraries & packages - Minimal, Standard Data Science, TensorFlow, PyTorch, CUDA
  * Kubeflow notebook controller for managing notebook sessions
  * Both CPU and GPU enabled
  * Optional ISV software: Anaconda (Professional), IBM Watson Studio, Intel OpenVINO, Intel AI Analytics Toolkit (AI Kit)
* Data ingestion, storage and data engineering:
  * Red Hat: OpenShift Streams for Apache Kafka (optional add-on); Amazon S3
  * Optional ISV software: Starburst Galaxy, Pachyderm
    * NOTE: Starburst Enterprise will work with RHODS as well and runs directly on OpenShift for customers consolidating analytics workloads.
* Model serving, versioning, monitoring
  * Red Hat: Source to image (OpenShift)
  * Red Hat OpenShift API Management (optional add-on)
  * Optional ISV software: Intel OpenVINO
  * Model serving (Model Mesh + UI)
  * Initial model monitoring

## Support and Consulting Services

### What level SLA will be offered?

Red Hat OpenShift Data Science cloud service follows the uptime SLAs that OpenShift Dedicated and Red Hat OpenShift Service on AWS offers.  This includes a SLA up to 99.5%.  The self-managed version does not have any SLAs associated with it.

### How does the support model work with the 3rd party ISV tools included in the service?

Red Hat provides level 1 support for the ISVs that have been integrated into the RHODS UI in our managed cloud service and the partner handles levels 2 & 3 support. Support handoffs to the software partner will leverage TSANet for bidirectional support processes. There may be some nuanced support recommendations for those SaaS ISV partner vendors where we recommend the customer go directly to the ISV for support.

### Does Red Hat offer any AI / ML consulting services that complement either the upstream Open Data Hub project or Red Hat OpenShift Data Science?

Red Hat consulting services offer several standard consulting services engagements such as OpenShift Data Science Platform Engagement, MLOps Foundation], intelligent app development pilot and data engineering pilot.  Red Hat consulting services can also offer custom engagements.  The Red Hat OpenShift Data Science Platform Engagement allows customers to gain support and assurance from Services Professionals during the integration of  RHODS into their environment to meet their organizational needs.

## Sales Engagement

### What are the primary use cases for RHODS?

There are two primary use cases:

* Experimentation with user-supplied data where the model outputs are hosted in the cloud service for testing or integration into a customer-defined Intelligent Application
* Experimentation with user-supplied data where the model outputs are exported or deployed to other OpenShift locations for integration into intelligent applications.

### Who is the primary user persona of Red Hat OpenShift Data Science?

The actual usage of this service is aimed at data scientists, data engineers, and application developers that use intelligent data analytics.  The goal of the service is to allow data scientists to work with tools and ecosystems with which they are comfortable  (eg Jupyter, TensorFlow, PyTorch), in an environment that does not require them to manage their underlying infrastructure, or file tickets with IT in order to experiment and access new tools. By working on OpenShift cloud services, data scientists can more easily adopt MLOps practices and develop assets that are more easily incorporated into larger intelligent applications. The abstraction layer provided by OpenShift cloud services enables Data Scientists to achieve this without having to become Kubernetes experts,  instead, allowing them to focus on getting value and insights from data.  

### Can Red Hat partners sell RHODS?

Yes.  The RHODS SKUs are in the Commercial Channel price book.  The entry in that channel price book is an older, more costly price.  The new price won’t be reflected in the channel price book until Q4, but Red Hat will commit to matching the new price for any opportunities in the interim.

### Is RHODS available in all regions?

RHODS cloud service and self managed can be sold worldwide.  Customers who want to purchase RHODS via AWS Marketplace will have to use one of the currently supported AWS Marketplaces ([EMEA](https://aws.amazon.com/marketplace/pp/prodview-fuxkweo2tdmr2), [North America and regions outside EMEA](https://aws.amazon.com/marketplace/pp/prodview-co7uaxdm7qnkq?sr=0-1&ref_=beagle&applicationId=AWSMPContessa)).  This list is constantly expanding.  

### How can my customers try it for free?

Customers can try out RHODS for free in the [Developer Sandbox](https://developers.redhat.com/developer-sandbox/activities/use-rhods-to-master-nlp). The developer sandbox will only provide limited cluster sizes and will provide limited 3rd party partner connectivity.  RHODS is also included as part of the OpenShift Dedicated 60-day trial.

### What is Red Hat’s AI / ML strategy and how do both the upstream Open Data Hub project and Red Hat OpenShift Data Science fit into it?

Red Hat seeks to promote the value of containers, Kubernetes, and DevOps as a foundation to accelerate AI/ML projects from pilot to production.  We continue to drive AI / ML innovation in the upstream community, with Open Data Hub being the primary example, leveraging our AI / ML consulting services practice. Red Hat continues to nurture an AI / ML ISV and hardware acceleration ecosystem with containers through OpenShift and Kubernetes operators, offered to customers through the Red Hat Marketplace. Red Hat OpenShift Data Science provides an environment for data scientists to experiment quickly with a subset of these AI ecosystem tools and create ML models that their operations counterparts can deploy in production, on containers, in the hybrid cloud.

### When would I lead with the upstream Open Data Hub project versus Red Hat OpenShift Data Science?

Just to be clear, Open Data Hub is not a product that can be sold.  It is a reference architecture or blueprint for a solution that can be built leveraging Red Hat commercial products and open source technologies.   Open Data Hub can be useful in the sales process to show open source innovation by Red Hat and get customers interested in leveraging our AI / ML Consulting services to implement ML workloads and tooling on OpenShift and the rest of the Red Hat portfolio.  Red Hat OpenShift Data Science contains an increasing subset of the technologies provided in the upstream Open Data Hub project, with some of the newer technologies included focused on MLOps. It enables customers to more quickly begin to implement models and deploy them in a container-ready format.  The AI / ML Consulting Services team has developed complementary services for Red Hat OpenShift Data Science as well as customers looking to include portions of ODH in their environment.

### Why are only a handful of the many tools that are currently offered through Open Data Hub offering in the initial Red Hat OpenShift Data Science offering?

We are offering a core subset of the tools to target the ‘standard’ machine learning tooling, Jupyter, Tensorflow and Pytorch. We want to offer components that we have experience running at scale and supporting through the Operate First framework. We are increasingly offering more MLOps components found in Open Data Hub, such as data science model serving (based on KubeFlow Model Mesh with a custom-built UI), model monitoring and in the near future, data science pipelines (based on Kubeflow Pipelines Tekton).

### Will Red Hat continue to participate in the upstream Open Data Hub project?

Yes, we will continue to work with the upstream Open Data Hub project. It will continue to offer a blueprint for customers who want to deploy a combination of Red Hat commercial as well as open source products and technologies in an on-premise environment.  Our Red Hat Consulting Services team will also continue to offer services to help guide customers who wish to adopt aspects of the Open Data Hub model.

## Managed Service Capabilities

### How will customers get their data into the cloud service?

Users are responsible for copying their data to and from Red Hat OpenShift Data Science on OpenShift cloud services.  We currently integrate with Amazon S3 as well as OpenShift Streams for Apache Kakfa (streaming data) and Starburst Galaxy (SQL query engine for your data sources: databases, warehouse, data lake, etc. ) to pull data into a customer’s Jupyter notebooks in RHODS. We are looking at other potential tools to make it easier to pull in data into RHODS in the future as well as architecture blueprints to show how to integrate with products like Snowflake in the future.

### How secure is the managed service?

Red Hat OpenShift Dedicated and Red Hat Service on AWS follow common industry best practices for security and controls. OpenShift Data Science leverages the work being done with OpenShift Cloud Services to certify and achieve compliance for multiple different standards.

### Model serving is a common challenge for data scientists, especially when integrated with containers.  How can this product help automate this?

Data scientists can build models using the RHODS service and leverage OpenShift source-to-image (S2i) capabilities to serve models. A JupyterLab plugin for Git integration makes it easy for data scientists to push models to Git repos that can be used to deploy models as a service. This [workshop](https://redhat-scholars.github.io/rhods-od-workshop/rhods-od-workshop/index.html) provides an example of these capabilities. We also have introduced options to serve models directly within the RHODS UI, with data science model serving (using Model Mesh with a UI) capabilities in late 2022 and have plans to include data science pipelines in 1H 2023.

### How are we integrating Jupyter Hub / Jupyter Notebook / Jupyter Lab within Red Hat OpenShift Data Science?

The Jupyter Lab technology integrated into Red Hat OpenShift Data Science has the following capabilities:

* Access Python notebooks - either connect to a git repo, or upload from a local machine. Save changes back to the local machine or push to git.
* Create new Python notebooks
* Access a set of ‘standard’ pre-made notebook images, containing packages you need to carry out data science in Python, including PyTorch and Tensorflow.
* Run notebooks on GPUs (introduced in July, 2022)

### What is Kubeflow and how is it integrated into the cloud service?

KubeFlow is a project dedicated to making deployments of ML workflows on Kubernetes simple, portable and scalable. Red Hat OpenShift Data Science leverages the KubeFlow control plane (manifests and operator) to deploy components of the managed service but does not include many components, such as model delivery.  Several elements of Kubeflow are being included in OpenShift Data Science such as Model Mesh, and Kubeflow Pipelines in late 2022 and 1H 2023.  

### The upstream Open Data Hub project provides an AI Library with several pre-trained and validated models for services like sentiment analysis.  Is Red Hat OpenShift Data Science offering pre-populated with a similar library?

No.  We have tutorials, examples, and “how to’s”, showing you how to make the most of the managed cloud service. All the assets used in these are open source so you can implement the models yourself.

## Other Questions

### Can data scientists get access to GPU-enabled hardware within the managed service, making it easier to stand up resource-intensive environments easier than on-prem provisioning?

RHODS supports the ability to run notebooks, and stand-alone models, on GPUs. This is integrated directly into the Jupyter spawner as an option when you spin up your notebook server session.  We support notebook images for GPU-enabled TensorFlow and GPU-enabled PyTorch. Commercial support must be purchased from NVIDIA. For the cloud service version of RHODS, no SRE proactive monitoring is provided.

### What are TensorFlow and Pytorch?

Tensorflow and PyTorch are OpenSource Machine Learning Frameworks. Tensorflow focuses on the training and inference of deep neural networks, and in the managed service we provide notebook images that contain the Python TensorFlow libraries, and optional GPU-compatible images (post-Field Trial). PyTorch is developed from Facebook’s AI Research lab and focuses on computer vision and natural language processing (NLP) models. Again, we provide Images that support both PyTorch and GPU-enabled PyTorch (post-GA).

### What is the spin-up latency for customers who are new to both OSD and RHODS?

Approximately 40 minutes for a new OSD cluster and another ten minutes to install the RHODS  add-on.

### Is the code for RHODS Open Source?

RHODS is an open source project.  All source code used to build the managed service is located on GitHub in the organization [red-hat-data-services](https://github.com/red-hat-data-services) and based on the upstream open source project, [Open Data Hub](https://github.com/opendatahub-io)..

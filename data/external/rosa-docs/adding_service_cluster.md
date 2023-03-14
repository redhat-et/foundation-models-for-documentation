# Adding services to a cluster using Red Hat OpenShift Cluster Manager console

You can add, access, and remove add-on services for your Red Hat OpenShift Service on AWS (ROSA) cluster by using Red Hat OpenShift Cluster Manager.

## Prerequisites

-   For the Amazon CloudWatch service, you must first install the `cluster-logging-operator` using the `rosa` CLI.

## Adding an add-on service to a cluster

You can add an add-on service to an existing Red Hat OpenShift Service on AWS (ROSA) cluster by using Red Hat OpenShift Cluster Manager.

-   You have created and provisioned a cluster for Red Hat OpenShift Service on AWS.

-   Your cluster meets all of the prerequisites for the service that you want to add on to your cluster.

-   For paid add-on services, note the following considerations:

    -   If the organization has sufficient quota, and if the service is compatible with the cluster, the service appears in OpenShift Cluster Manager.

    -   If the organization has never had quota, or if the cluster is not compatible, then the service does not display.

    -   If the organization had quota in the past, but the quota is currently `0`, the service is still visible but disabled in OpenShift Cluster Manager until you get more quota.



To add a service to a cluster, you must be the cluster owner.



1.  Navigate to the **Clusters** page in [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift).

2.  Select the cluster you want to add a service to.

3.  Click the **Add-ons** tab.

4.  Click the service option you want to add, click **Install**. An installing icon appears, indicating that the service has begun installing.

    A green check mark appears in the service option when the installation is complete. You might have to refresh your browser to see the installation status.

5.  When the service is **Installed**, click **View in console** to access the service.

## Accessing installed add-on services on your cluster

After you successfully install an add-on service on your Red Hat OpenShift Service on AWS (ROSA) cluster, you can access the service by using the OpenShift web console.

-   You have successfully installed a service on your Red Hat OpenShift Service on AWS cluster.

1.  Navigate to the **Clusters** page in [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift).

2.  Select the cluster with an installed service you want to access.

3.  Navigate to the **Add-ons** tab, and locate the installed service that you want to access.

4.  Click **View on console** from the service option to open the OpenShift web console.

5.  Enter your credentials to log in to the OpenShift web console.

6.  Click the **Red Hat Applications** menu by clicking the three-by-three matrix icon in the upper right corner of the main screen.

7.  Select the service you want to open from the drop-down menu. A new browser tab opens and you are required to authenticate through Red Hat Single Sign-On.

You have now accessed your service and can begin using it.

## Deleting an add-on service using Red Hat OpenShift Cluster Manager

You can delete an add-on service from your Red Hat OpenShift Service on AWS (ROSA) cluster by using Red Hat OpenShift Cluster Manager.

1.  Navigate to the **Clusters** page in [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift).

2.  Click the cluster with the installed service that you want to delete.

3.  Navigate to the **Add-ons** tab, and locate the installed service that you want to delete.

4.  From the installed service option, click the menu and select **Uninstall add-on** from the drop-down menu.

5.  You must type the name of the service that you want to delete in the confirmation message that appears.

6.  Click **Uninstall**. You are returned to the **Add-ons** tab and an uninstalling state icon is present on the service option you deleted.

## Additional resources

-   For information about the `cluster-logging-operator` and the AWS CloudWatch log forwarding service, see [Forwarding logs to Amazon CloudWatch](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/logging/#cluster-logging-collector-log-forward-cloudwatch_cluster-logging-external)

# Add-on services available for Red Hat OpenShift Service on AWS

You can add services to your existing Red Hat OpenShift Service on AWS (ROSA) cluster using the [Red Hat OpenShift Cluster Manager console](#adding-service).

These services can also be installed [using the `rosa` CLI](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/rosa_cli/#rosa-managing-objects-cli).

## Amazon CloudWatch

Amazon CloudWatch forwards logs from Red Hat OpenShift Service on AWS (ROSA) to the AWS console for viewing. You must first install the ROSA `cluster-logging-operator` using the `rosa` CLI before installing the Amazon CloudWatch service through Red Hat OpenShift Cluster Manager console.

-   [Amazon CloudWatch product information](https://aws.amazon.com/cloudwatch/)

-   [Forwarding logs to Amazon CloudWatch](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/logging/#cluster-logging-collector-log-forward-cloudwatch_cluster-logging-external)

## Red Hat OpenShift API Management

The Red Hat OpenShift API Management (OpenShift API Management) service is available as an add-on to your Red Hat OpenShift Service on AWS on AWS cluster. OpenShift API Management is a managed API traffic control and API program management solution. It is based on the 3scale API Management platform and implements single sign-on for Red Hat solutions to secure and protect your APIs.

This OpenShift API Management entitlement provides:

-   Availability to any cluster that meets the resource requirements listed in the Red Hat OpenShift API Management service definition.

-   Full production-level support.

-   No time limits on usage.

-   100K quota, or calls per day. Customers have the option to pay for an OpenShift API Management subscription with higher quotas.

<!-- -->

-   [Red Hat OpenShift API Management](https://access.redhat.com/documentation/en-us/red_hat_openshift_api_management) documentation

## Red Hat OpenShift Database Access

Red Hat OpenShift Database Access enables easy consumption of database-as-a-service (DBaaS) offerings from partners including MongoDB Atlas, Crunchy Bridge, CockroachDB, and Amazon Relational Database Service (RDS) directly from managed Red Hat OpenShift Service on AWS clusters. You can manage, monitor, and create cloud-hosted database instances for connecting to your applications.

Red Hat OpenShift Database Access is a Service Preview release. A Service Preview release contains features that are early in development. Service Preview releases are not production ready and are not fully tested. Do not use RHODA for production or business-critical workloads.

-   [Red Hat OpenShift Database Access](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-database-access) product page

## Red Hat OpenShift Data Science

Red Hat OpenShift Data Science (RHODS) enables users to integrate data and AI and machine learning software to run end-to-end machine learning workflows. It provides a collection of notebook images with the tools and libraries required to develop and deploy data models. This allows data scientists to easily develop data models, integrate models into applications, and deploy applications using Red Hat OpenShift. RHODS is available as an add-on to Red Hat managed environments such as OpenShift Dedicated and Red Hat OpenShift Service on AWS (ROSA).

-   [Red Hat OpenShift Data Science](https://access.redhat.com/documentation/en-us/red_hat_openshift_data_science/1) documentation

-   [Red Hat OpenShift Data Science](https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-data-science) product page

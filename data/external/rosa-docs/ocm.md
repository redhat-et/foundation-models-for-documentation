# Red Hat OpenShift Cluster Manager

Red Hat OpenShift Cluster Manager is a managed service where you can install, modify, operate, and upgrade your Red Hat OpenShift clusters. This service allows you to work with all of your organization’s clusters from a single dashboard.

OpenShift Cluster Manager guides you to install OpenShift Container Platform, Red Hat OpenShift Service on AWS (ROSA), and OpenShift Dedicated clusters. It is also responsible for managing both OpenShift Container Platform clusters after self-installation as well as your ROSA and OpenShift Dedicated clusters.

You can use OpenShift Cluster Manager to do the following actions:

-   Create new clusters

-   View cluster details and metrics

-   Manage your clusters with tasks such as scaling, changing node labels, networking, authentication

-   Manage access control

-   Monitor clusters

-   Schedule upgrades

## Accessing Red Hat OpenShift Cluster Manager

You can access OpenShift Cluster Manager with your configured OpenShift account.

-   You have an account that is part of an OpenShift organization.

-   If you are creating a cluster, your organization has specified quota.

<!-- -->

-   Log in to [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift) using your login credentials.

## General actions

On the top right of the cluster page, there are some actions that a user can perform on the entire cluster:

-   **Open console** launches a web console so that the cluster owner can issue commands to the cluster.

-   **Actions** drop-down menu allows the cluster owner to rename the display name of the cluster, change the amount of load balancers and persistent storage on the cluster, if applicable, manually set the node count, and delete the cluster.

-   **Refresh** icon forces a refresh of the cluster.

## Cluster tabs

Selecting an active, installed cluster shows tabs associated with that cluster. The following tabs display after the cluster’s installation completes:

-   Overview

-   Access control

-   Add-ons

-   Networking

-   Insights Advisor

-   Machine pools

-   Support

-   Settings

### Overview tab

The **Overview** tab provides information about how your cluster was configured:

-   **Cluster ID** is the unique identification for the created cluster. This ID can be used when issuing commands to the cluster from the command line.

-   **Type** shows the OpenShift version that the cluster is using.

-   **Region** is the server region.

-   **Provider** shows which cloud provider that the cluster was built upon.

-   **Availability** shows which type of availability zone that the cluster uses, either single or multizone.

-   **Version** is the OpenShift version that is installed on the cluster. If there is an update available, you can update from this field.

-   **Created at** shows the date and time that the cluster was created.

-   **Owner** identifies who created the cluster and has owner rights.

-   **Subscription type** shows the subscription model that was selected on creation.

-   **Infrastructure type** is the type of account that the cluster uses.

-   **Status** displays the current status of the cluster.

-   **Total vCPU** shows the total available virtual CPU for this cluster.

-   **Total memory** shows the total available memory for this cluster.

-   **Load balancers**

-   **Persistent storage** displays the amount of storage that is available on this cluster.

-   **Nodes** shows the actual and desired nodes on the cluster. These numbers might not match due to cluster scaling.

-   **Network** field shows the address and prefixes for network connectivity.

-   **Resource usage** section of the tab displays the resources in use with a graph.

-   **Advisor recommendations** section gives insight in relation to security, performance, availability, and stablility. This section requires the use of remote health functionality. See [Using Insights to identify issues with your cluster](https://docs.openshift.com/container-platform/4.9/support/remote_health_monitoring/using-insights-to-identify-issues-with-your-cluster.html).

-   **Cluster history** section shows everything that has been done with the cluster including creation and when a new version is identified.

### Access control tab

The **Access control** tab allows the cluster owner to set up an identity provider, grant elevated permissions, and grant roles to other users.

-   You must be the cluster owner or have the correct permissions to grant roles on the cluster.

1.  Select the **Grant role** button.

2.  Enter the Red Hat account login for the user that you wish to grant a role on the cluster.

3.  Select the **Grant role** button on the dialog box.

4.  The dialog box closes, and the selected user shows the "Cluster Editor" access.

### Add-ons tab

The **Add-ons** tab displays all of the optional add-ons that can be added to the cluster. Select the desired add-on, and then select **Install** below the description for the add-on that displays.

### Cluster history tab

The **Cluster history** tab shows all the history of the cluster including: changes made to the cluster, descriptions of changes, severity, dates, and who made the changes. You can also download the information using the **Download history** button.

### Networking tab

The **Networking** tab provides a control plane API endpoint as well as the default application router. Both the control plane API endpoint and the default application router can be made private by selecting the respective box below each of them.



For Security Token Service (STS) installations, these options cannot be changed. STS installations also do not allow you to change privacy nor allow you to add an additional router.



### Insights Advisor tab

The **Insights Advisor** tab uses the Remote Health functionality of the OpenShift Container Platform to identify and mitigate risks to security, performance, availability, and stability. See [Using Insights to identify issues with your cluster](https://docs.openshift.com/container-platform/latest/support/getting-support.html) in the OpenShift Container Platform documentation.

### Machine pools tab

The **Machine pools** tab allows the cluster owner to create new machine pools, if there is enough available quota, or edit an existing machine pool.

Selecting the **More options** \> **Scale** opens the "Edit node count" dialog. In this dialog, you can change the node count per availability zone. If autoscaling is enabled, you can also set the range for autoscaling.

### Support tab

In the **Support** tab, you can add notification contacts for individuals that should receive cluster notifications. The username or email address that you provide must relate to a user account in the Red Hat organization where the cluster is deployed. For the steps to add a notification contact, see *Adding cluster notification contacts*.

Also from this tab, you can open a support case to request technical support for your cluster.

### Settings tab

The **Settings** tab provides a few options for the cluster owner:

-   **Monitoring**, which is enabled by default, allows for reporting done on user-defined actions. See [Understanding the monitoring stack](https://docs.openshift.com/rosa/monitoring/osd-understanding-the-monitoring-stack.html).

-   **Update strategy** allows you to determine if the cluster automatically updates on a certain day of the week at a specified time or if all updates are scheduled manually.

-   **Node draining** sets the duration that protected workloads are respected during updates. When this duration has passed, the node is forcibly removed.

-   **Update status** shows the current version and if there are any updates available.

## Additional resources

-   For the complete documentation for OpenShift Cluster Manager, see [OpenShift Cluster Manager documentation](https://access.redhat.com/documentation/en-us/openshift_cluster_manager/2022/html-single/managing_clusters/index).

-   For steps to add cluster notification contacts, see [Adding cluster notification contacts](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/logging/#adding-cluster-notification-contacts_sd-accessing-the-service-logs).

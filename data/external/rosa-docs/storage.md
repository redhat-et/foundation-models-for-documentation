# Persistent storage

## Persistent storage using AWS Elastic Block Store (EBS)

Red Hat OpenShift Service on AWS (ROSA) clusters are prebuilt with two storage classes that use AWS Elastic Block Store (EBS) volumes. These storage classes are ready to use and some familiarity with Kubernetes and AWS is assumed.

Following are the two prebuilt storage classes:

| Name    | Provisioner           |
|---------|-----------------------|
| gp3     | kubernetes.io/aws-ebs |
| gp3-csi | ebs.csi.aws.com       |

The gp3 storage class is set as default; however, you can select either one as the default storage class.

The Kubernetes persistent volume framework enables administrators to provision a cluster with persistent storage and gives users a way to request those resources without having any knowledge of the underlying infrastructure. You can dynamically provision AWS EBS volumes. Persistent volumes are not bound to a single project or namespace; therefore, the volumes can be shared across ROSA clusters. Persistent volume claims are specific to a project or namespace and can be requested by users.



-   ROSA defaults to using an in-tree, or non-Container Storage Interface (CSI), plugin to provision AWS EBS storage. In future ROSA versions, volumes provisioned using existing in-tree plugins are planned for migration to their equivalent CSI driver. After full migration, the in-tree plugins are planned to be removed from the future versions of ROSA.

-   High-availability of storage in the infrastructure is left to the underlying storage provider.



### Format of persistent volumes

Before a ROSA cluster mounts the volume and passes it to a container, the cluster checks that the volume contains a file system as specified by the **fsType** parameter in the persistent volume definition. If the device is not formatted with a file system, all data from the device is erased and the device is automatically formatted with the given file system. This verification enables you to use unformatted AWS volumes as persistent volumes, as the ROSA cluster formats the AWS volumes before the first use.

### Capacity of EBS volumes on a node

By default, a ROSA cluster supports a maximum of 39 EBS volumes attached to one node. This limit is consistent with the [AWS volume limits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/volume_limits.html#linux-specific-volume-limits). The volume limit depends on the instance type.



You must use either in-tree or CSI volumes and their respective storage classes, but never both volume types at the same time. The maximum attached EBS volume number is counted separately for in-tree and CSI volumes, so you could have up to 39 EBS volumes of each type.



For information about accessing additional storage options, such as volume snapshots, that are not possible with in-tree volume plugins, see [Elastic Block Store CSI Driver Operator](https://docs.openshift.com/container-platform/4.9/storage/container_storage_interface/persistent-storage-csi-ebs.html#persistent-storage-csi-ebs).

### Creating a persistent volume claim



**Prerequisites**



Storage must exist in the underlying infrastructure before it can be mounted as a volume in the ROSA cluster.

1.  In the OpenShift Cluster console, click **Storage → Persistent Volume Claims**.

2.  In the persistent volume claims overview, click **Create Persistent Volume Claim**.

3.  Define the desired options on the page that appears.

    1.  Select the previously created storage class from the drop-down menu.

    2.  Enter a unique name for the storage claim.

    3.  Select the access mode. This selection determines the read and write access for the storage claim.

    4.  Define the size of the storage claim.

4.  Click **Create** to create the persistent volume claim and generate a persistent volume.

## Setting up AWS EFS for Red Hat OpenShift Service on AWS



This procedure is specific to the Amazon Web Services Elastic File System (AWS EFS) community Operator, which is only applicable up to Red Hat OpenShift Service on AWS 4.9.



The Amazon Web Services Elastic File System (AWS EFS) is a Network File System (NFS) that can be provisioned on Red Hat OpenShift Service on AWS clusters. AWS also provides and supports a CSI EFS Driver to be used with Kubernetes that allows Kubernetes workloads to leverage this shared file storage.

This document describes the basic steps needed to set up your AWS account to prepare EFS to be used by Red Hat OpenShift Service on AWS. For more information about AWS EFS, see the [AWS EFS documentation](https://docs.aws.amazon.com/efs/index.html).



Red Hat does not provide official support for this feature, including backup and recovery. The customer is responsible for backing up the EFS data and recovering it in the event of an outage or data loss.



The high-level process to enable EFS on a cluster is:

1.  Create an AWS EFS in the AWS account used by the cluster.

2.  Install the AWS EFS Operator from OperatorHub.

3.  Create `SharedVolume` custom resources.

4.  Use the generated persistent volume claims in pod `spec.volumes`.

### Prerequisites

-   A Red Hat OpenShift Service on AWS cluster

-   Administrator access to the AWS account of that cluster

### Configuring the AWS account

Set up your AWS account to prepare AWS EFS for use by Red Hat OpenShift Service on AWS.

1.  Log in to the [AWS EC2 Console](https://console.aws.amazon.com/ec2).

2.  Select the region that matches the cluster region.

3.  Filter only worker EC2 instances, and select an instance. Note the VPC ID and security group ID. These values are required later in the process.

4.  Click the **Security** tab, and click the Security Group Name.

5.  From the **Actions** dropdown menu, click **Edit Inbound Rules**. Scroll to the bottom, and click **Add Rule**.

6.  Add an NFS rule that allows NFS traffic from the VPC private CIDR.

7.  Open the [Amazon EFS page](https://console.aws.amazon.com/efs/). To create the EFS, click **Create file system**.

8.  Click **Customize** and proceed through the wizard.

    1.  In `Step 2:`, configure the network access:

        1.  Click the VPC of the cluster that you noted previously.

        2.  Ensure that the private subnets are selected.

        3.  Select the Security Group Name that you noted previously for the EC2 worker instances.

        4.  Click **Next**.

    2.  In `Step 3:`, configure the client access:

        1.  Click **Add access point**.

        2.  Enter a unique Path such as `/access_point_1`.

        3.  Configure the Owner fields with ownership or permissions that allow write access for your worker pods. For example, if your worker pods run with group ID `100`, you can set that ID as your `Owner Group ID` and ensure the permissions include `g+rwx`.

9.  Continue through the wizard steps, and click **Create File System**.

10. After the file system is created:

    1.  Note the file system ID for later use.

    2.  Click **Manage client access** and note the access point ID.

You can add more NFS rules, using steps 5-10, to create separate shared data stores. In each case, make note of the corresponding file system ID and access point ID.

### Installing the EFS Operator

1.  Log in to the OpenShift Web UI for your cluster.

2.  Click **Operators** → **OperatorHub**.

3.  Search for and select the AWS EFS Operator. Click **Install**.

4.  Accept the default settings, and click **Subscribe**.

### Creating `SharedVolume` resources using the console

You must create one `SharedVolume` resource per file system:access point pair in each project from which you want pods to access it.

1.  In the OpenShift web console, create and navigate to a project.

2.  Click **Operators** → **Installed Operators**. Find the entry for AWS EFS Operator, and click **SharedVolume** under Provided APIs.

3.  Click **Create SharedVolume**.

4.  Edit the sample YAML:

    1.  Type a suitable value for `name`.

    2.  Replace the values of `accessPointID` and `fileSystemID` with the values from the EFS resources you created earlier.

        ``` yaml
          apiVersion: aws-efs.managed.openshift.io/v1alpha1
          kind: SharedVolume
          metadata:
            name: sv1
            namespace: efsop2
          spec:
            accessPointID: fsap-0123456789abcdef
            fileSystemID: fs-0123cdef
        ```

5.  Click **Create**.

    The `SharedVolume` resource is created, and triggers the AWS EFS Operator to generate and associate a PersistentVolume:PersistentVolumeClaim pair with the specified EFS access point.

6.  To verify that the persistent volume claim (PVC) exists and is bound, click **Storage** → **Persistent Volume Claims**.

    The PVC name is `pvc-<shared_volume_name>`. The associated PV name is `pv-<project_name>-<shared_volume_name>`.

### Creating `SharedVolume` resources using the CLI

You must create one `SharedVolume` resource per file system:access point pair in each project from which you want pods to access it. You can create a SharedVolume manually by entering YAML or JSON definitions, or by dragging and dropping a file into an editor.

1.  Using the `oc` CLI, create the YAML file using the `accessPointID` and `fileSystemID` values from the EFS resources you created earlier.

    ``` yaml
      apiVersion: aws-efs.managed.openshift.io/v1alpha1
      kind: SharedVolume
      metadata:
        name: sv1
        namespace: efsop2
      spec:
        accessPointID: fsap-0123456789abcdef
        fileSystemID: fs-0123cdef
    ```

2.  Apply the file to the cluster using the following command:

    ``` terminal
    $ oc apply -f <filename>.yaml
    ```

    The `SharedVolume` resource is created, and triggers the AWS EFS Operator to generate and associate a PersistentVolume:PersistentVolumeClaim pair with the specified EFS access point.

3.  To verify that the PVC exists and is bound, navigate to **Storage** > **Persistent Volume Claims**.

    The PVC name is `pvc-{shared_volume_name}`. The associated PV name is `pv-{project_name}-{shared_volume_name}`.

### Connecting pods

The persistent volume claim (PVC) that was created in your project is ready for use. You can create a sample pod to test this PVC.

1.  Create and navigate to a project.

2.  Click **Workloads** → **Pods** → **Create Pod**.

3.  Enter the YAML information. Use the name of your `PersistentVolumeClaim` object under `.spec.volumes[].persistentVolumeClaim.claimName`.

    

    **Example**

    

    ``` terminal
    apiVersion: v1
    kind: Pod
    metadata:
     name: test-efs
    spec:
     volumes:
       - name: efs-storage-vol
         persistentVolumeClaim:
           claimName: pvc-sv1
     containers:
       - name: test-efs
         image: centos:latest
         command: [ "/bin/bash", "-c", "--" ]
         args: [ "while true; do touch /mnt/efs-data/verify-efs && echo 'hello efs' && sleep 30; done;" ]
         volumeMounts:
           - mountPath: "/mnt/efs-data"
             name: efs-storage-vol
    ```

4.  After the pods are created, click **Workloads** → **Pods** → **Logs** to verify the pod logs.

### Uninstalling the EFS Operator



**Procedure**



To remove the Operator from your cluster:

1.  Delete all of the workloads using the persistent volume claims that were generated by the Operator.

2.  Delete all of the shared volumes from all of the namespaces. The Operator automatically removes the associated persistent volumes and persistent volume claims.

3.  Uninstall the Operator:

    1.  Click **Operators** → **Installed Operators**.

    2.  Find the entry for AWS EFS Operator, and click the menu button on the right-hand side of the Operator.

    3.  Click **Uninstall** and confirm the deletion.

4.  Delete the shared volume CRD. This action triggers the deletion of the remaining Operator-owned resources.

## Setting up AWS Elastic File Service CSI Driver Operator



This procedure is specific to the Amazon Web Services Elastic File System (AWS EFS) CSI Driver Operator, which is only applicable for Red Hat OpenShift Service on AWS 4.10 and later versions.



### Overview

Red Hat OpenShift Service on AWS is capable of provisioning persistent volumes (PVs) using the Container Storage Interface (CSI) driver for AWS Elastic File Service (EFS).

Familiarity with [persistent storage](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.12/html-single/storage/index#persistent-storage-overview_understanding-persistent-storage) and [configuring CSI volumes](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.12/html-single/storage/index#persistent-storage-csi) is recommended when working with a CSI Operator and driver.

After installing the AWS EFS CSI Driver Operator, Red Hat OpenShift Service on AWS installs the AWS EFS CSI Operator and the AWS EFS CSI driver by default in the `openshift-cluster-csi-drivers` namespace. This allows the AWS EFS CSI Driver Operator to create CSI-provisioned PVs that mount to AWS EFS assets.

-   The *AWS EFS CSI Driver Operator*, after being installed, does not create a storage class by default to use to create persistent volume claims (PVCs). However, you can manually create the AWS EFS `StorageClass`. The AWS EFS CSI Driver Operator supports dynamic volume provisioning by allowing storage volumes to be created on-demand. This eliminates the need for cluster administrators to pre-provision storage.

-   The *AWS EFS CSI driver* enables you to create and mount AWS EFS PVs.



AWS EFS only supports regional volumes, not zonal volumes.



### About CSI

Storage vendors have traditionally provided storage drivers as part of Kubernetes. With the implementation of the Container Storage Interface (CSI), third-party providers can instead deliver storage plugins using a standard interface without ever having to change the core Kubernetes code.

CSI Operators give Red Hat OpenShift Service on AWS users storage options, such as volume snapshots, that are not possible with in-tree volume plugins.

### Installing the AWS EFS CSI Driver Operator

The AWS EFS CSI Driver Operator is not installed in Red Hat OpenShift Service on AWS by default. Use the following procedure to install and configure the AWS EFS CSI Driver Operator in your cluster.

-   Access to the Red Hat OpenShift Service on AWS web console.



**Procedure**



To install the AWS EFS CSI Driver Operator from the web console:

1.  Log in to the web console.

2.  Install the AWS EFS CSI Operator:

    1.  Click **Operators** → **OperatorHub**.

    2.  Locate the AWS EFS CSI Operator by typing **AWS EFS CSI** in the filter box.

    3.  Click the **AWS EFS CSI Driver Operator** button.

        

        Be sure to select the **AWS EFS CSI Driver Operator** and not the **AWS EFS Operator**. The **AWS EFS Operator** is a community Operator and is not supported by Red Hat.

        

    4.  On the **AWS EFS CSI Driver Operator** page, click **Install**.

    5.  On the **Install Operator** page, ensure that:

        -   **All namespaces on the cluster (default)** is selected.

        -   **Installed Namespace** is set to **openshift-cluster-csi-drivers**.

    6.  Click **Install**.

        After the installation finishes, the AWS EFS CSI Operator is listed in the **Installed Operators** section of the web console.

3.  Install the AWS EFS CSI Driver:

    1.  Click **administration** → **CustomResourceDefinitions** → **ClusterCSIDriver**.

    2.  On the **Instances** tab, click **Create ClusterCSIDriver**.

    3.  Use the following YAML file:

        ``` yaml
        apiVersion: operator.openshift.io/v1
        kind: ClusterCSIDriver
        metadata:
            name: efs.csi.aws.com
        spec:
          managementState: Managed
        ```

    4.  Click **Create**.

    5.  Wait for the following Conditions to change to a "true" status:

        -   AWSEFSDriverCredentialsRequestControllerAvailable

        -   AWSEFSDriverNodeServiceControllerAvailable

        -   AWSEFSDriverControllerServiceControllerAvailable

-   [Configuring AWS EFS CSI Driver with STS](#efs-sts_rosa-persistent-storage-aws-efs-csi)

### Configuring AWS EFS CSI Driver Operator with Security Token Service

This procedure explains how to configure the AWS EFS CSI Driver Operator with Red Hat OpenShift Service on AWS on AWS Security Token Service (STS).

Perform this procedure after installing the AWS EFS CSI Operator, but before installing the AWS EFS CSI driver as part of *Installing the AWS EFS CSI Driver Operator* procedure. If you perform this procedure after installing the driver and creating volumes, your volumes will fail to mount into pods.

-   AWS account credentials



**Procedure**



To configure the AWS EFS CSI Driver Operator with STS:

1.  Extract the CCO utility (`ccoctl`) binary from the Red Hat OpenShift Service on AWS release image, which you used to install the cluster with STS. For more information, see "Configuring the Cloud Credential Operator utility".

2.  Create and save an EFS `CredentialsRequest` YAML file, such as shown in the following example, and then place it in the `credrequests` directory:

    

    **Example**

    

    ``` yaml
    apiVersion: cloudcredential.openshift.io/v1
    kind: CredentialsRequest
    metadata:
      name: openshift-aws-efs-csi-driver
      namespace: openshift-cloud-credential-operator
    spec:
      providerSpec:
        apiVersion: cloudcredential.openshift.io/v1
        kind: AWSProviderSpec
        statementEntries:
        - action:
          - elasticfilesystem:*
          effect: Allow
          resource: '*'
      secretRef:
        name: aws-efs-cloud-credentials
        namespace: openshift-cluster-csi-drivers
      serviceAccountNames:
      - aws-efs-csi-driver-operator
      - aws-efs-csi-driver-controller-sa
    ```

3.  Run the `ccoctl` tool to generate a new IAM role in AWS, and create a YAML file for it in the local file system (`<path_to_ccoctl_output_dir>/manifests/openshift-cluster-csi-drivers-aws-efs-cloud-credentials-credentials.yaml`).

    ``` terminal
    $ ccoctl aws create-iam-roles --name=<name> --region=<aws_region> --credentials-requests-dir=<path_to_directory_with_list_of_credentials_requests>/credrequests --identity-provider-arn=arn:aws:iam::<aws_account_id>:oidc-provider/<name>-oidc.s3.<aws_region>.amazonaws.com
    ```

    -   `name=<name>` is the name used to tag any cloud resources that are created for tracking.

    -   `region=<aws_region>` is the AWS region where cloud resources are created.

    -   `dir=<path_to_directory_with_list_of_credentials_requests>/credrequests` is the directory containing the EFS CredentialsRequest file in previous step.

    -   `<aws_account_id>` is the AWS account ID.

        

        **Example**

        

        ``` terminal
        $ ccoctl aws create-iam-roles --name my-aws-efs --credentials-requests-dir credrequests --identity-provider-arn arn:aws:iam::123456789012:oidc-provider/my-aws-efs-oidc.s3.us-east-2.amazonaws.com
        ```

        

        **Example output**

        

        ``` terminal
        2022/03/21 06:24:44 Role arn:aws:iam::123456789012:role/my-aws-efs -openshift-cluster-csi-drivers-aws-efs-cloud- created
        2022/03/21 06:24:44 Saved credentials configuration to: /manifests/openshift-cluster-csi-drivers-aws-efs-cloud-credentials-credentials.yaml
        2022/03/21 06:24:45 Updated Role policy for Role my-aws-efs-openshift-cluster-csi-drivers-aws-efs-cloud-
        ```

4.  Create the AWS EFS cloud credentials and secret:

    ``` terminal
    $ oc create -f <path_to_ccoctl_output_dir>/manifests/openshift-cluster-csi-drivers-aws-efs-cloud-credentials-credentials.yaml
    ```

    

    **Example**

    

    ``` terminal
    $ oc create -f /manifests/openshift-cluster-csi-drivers-aws-efs-cloud-credentials-credentials.yaml
    ```

    

    **Example output**

    

    ``` terminal
    secret/aws-efs-cloud-credentials created
    ```

-   [Installing the AWS EFS CSI Driver Operator](#persistent-storage-csi-olm-operator-install_rosa-persistent-storage-aws-efs-csi)

-   [Configuring the Cloud Credential Operator utility](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.12/html-single/authentication_and_authorization/index#cco-ccoctl-configuring_cco-mode-sts)

### Creating the AWS EFS storage class

Storage classes are used to differentiate and delineate storage levels and usages. By defining a storage class, users can obtain dynamically provisioned persistent volumes.

The *AWS EFS CSI Driver Operator*, after being installed, does not create a storage class by default. However, you can manually create the AWS EFS storage class.

### Creating and configuring access to EFS volumes in AWS

This procedure explains how to create and configure EFS volumes in AWS so that you can use them in Red Hat OpenShift Service on AWS.

-   AWS account credentials



**Procedure**



To create and configure access to an EFS volume in AWS:

1.  On the AWS console, open <https://console.aws.amazon.com/efs>.

2.  Click **Create file system**:

    -   Enter a name for the file system.

    -   For **Virtual Private Cloud (VPC)**, select your Red Hat OpenShift Service on AWS’s' virtual private cloud (VPC).

    -   Accept default settings for all other selections.

3.  Wait for the volume and mount targets to finish being fully created:

    1.  Go to <https://console.aws.amazon.com/efs#/file-systems>.

    2.  Click your volume, and on the **Network** tab wait for all mount targets to become available (\~1-2 minutes).

4.  On the **Network** tab, copy the Security Group ID (you will need this in the next step).

5.  Go to <https://console.aws.amazon.com/ec2/v2/home#SecurityGroups>, and find the Security Group used by the EFS volume.

6.  On the **Inbound rules** tab, click **Edit inbound rules**, and then add a new rule with the following settings to allow Red Hat OpenShift Service on AWS nodes to access EFS volumes :

    -   **Type**: NFS

    -   **Protocol**: TCP

    -   **Port range**: 2049

    -   **Source**: Custom/IP address range of your nodes (for example: “10.0.0.0/16”)

        This step allows Red Hat OpenShift Service on AWS to use NFS ports from the cluster.

7.  Save the rule.

### Dynamic provisioning for AWS EFS

The AWS EFS CSI Driver supports a different form of dynamic provisioning than other CSI drivers. It provisions new PVs as subdirectories of a pre-existing EFS volume. The PVs are independent of each other. However, they all share the same EFS volume. When the volume is deleted, all PVs provisioned out of it are deleted too. The EFS CSI driver creates an AWS Access Point for each such subdirectory. Due to AWS AccessPoint limits, you can only dynamically provision 1000 PVs from a single `StorageClass`/EFS volume.



Note that `PVC.spec.resources` is not enforced by EFS.

In the example below, you request 5 GiB of space. However, the created PV is limitless and can store any amount of data (like petabytes). A broken application, or even a rogue application, can cause significant expenses when it stores too much data on the volume.

Using monitoring of EFS volume sizes in AWS is strongly recommended.



-   You have created AWS EFS volumes.

-   You have created the AWS EFS storage class.



**Procedure**



To enable dynamic provisioning:

-   Create a PVC (or StatefulSet or Template) as usual, referring to the `StorageClass` created above.

    ``` yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: test
    spec:
      storageClassName: efs-sc
      accessModes:
        - ReadWriteMany
      resources:
        requests:
          storage: 5Gi
    ```

If you have problems setting up dynamic provisioning, see [AWS EFS troubleshooting](#efs-troubleshooting_rosa-persistent-storage-aws-efs-csi).

### Creating static PVs with AWS EFS

It is possible to use an AWS EFS volume as a single PV without any dynamic provisioning. The whole volume is mounted to pods.

-   You have created AWS EFS volumes.

<!-- -->

-   Create the PV using the following YAML file:

    ``` yaml
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: efs-pv
    spec:
      capacity: 
        storage: 5Gi
      volumeMode: Filesystem
      accessModes:
        - ReadWriteMany
        - ReadWriteOnce
      persistentVolumeReclaimPolicy: Retain
      csi:
        driver: efs.csi.aws.com
        volumeHandle: fs-ae66151a 
        volumeAttributes:
          encryptInTransit: "false" 
    ```

    -   `spec.capacity` does not have any meaning and is ignored by the CSI driver. It is used only when binding to a PVC. Applications can store any amount of data to the volume.

    -   `volumeHandle` must be the same ID as the EFS volume you created in AWS. If you are providing your own access point, `volumeHandle` should be `<EFS volume ID>::<access point ID>`. For example: `fs-6e633ada::fsap-081a1d293f0004630`.

    -   If desired, you can disable encryption in transit. Encryption is enabled by default.

If you have problems setting up static PVs, see [AWS EFS troubleshooting](#efs-troubleshooting_rosa-persistent-storage-aws-efs-csi).

### AWS EFS security

The following information is important for AWS EFS security.

When using access points, for example, by using dynamic provisioning as described earlier, Amazon automatically replaces GIDs on files with the GID of the access point. In addition, EFS considers the user ID, group ID, and secondary group IDs of the access point when evaluating file system permissions. EFS ignores the NFS client’s IDs. For more information about access points, see <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>.

As a consequence, EFS volumes silently ignore FSGroup; Red Hat OpenShift Service on AWS is not able to replace the GIDs of files on the volume with FSGroup. Any pod that can access a mounted EFS access point can access any file on it.

Unrelated to this, encryption in transit is enabled by default. For more information, see <https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html>.

### AWS EFS troubleshooting

The following information provides guidance on how to troubleshoot issues with AWS EFS:

-   The AWS EFS Operator and CSI driver run in namespace `openshift-cluster-csi-drivers`.

-   To initiate gathering of logs of the AWS EFS Operator and CSI driver, run the following command:

    ``` terminal
    $ oc adm must-gather
    [must-gather      ] OUT Using must-gather plugin-in image: quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:125f183d13601537ff15b3239df95d47f0a604da2847b561151fedd699f5e3a5
    [must-gather      ] OUT namespace/openshift-must-gather-xm4wq created
    [must-gather      ] OUT clusterrolebinding.rbac.authorization.k8s.io/must-gather-2bd8x created
    [must-gather      ] OUT pod for plug-in image quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:125f183d13601537ff15b3239df95d47f0a604da2847b561151fedd699f5e3a5 created
    ```

-   To show AWS EFS Operator errors, view the `ClusterCSIDriver` status:

    ``` terminal
    $ oc get clustercsidriver efs.csi.aws.com -o yaml
    ```

-   If a volume cannot be mounted to a pod (as shown in the output of the following command):

    ``` terminal
    $ oc describe pod
    ...
      Type     Reason       Age    From               Message
      ----     ------       ----   ----               -------
      Normal   Scheduled    2m13s  default-scheduler  Successfully assigned default/efs-app to ip-10-0-135-94.ec2.internal
      Warning  FailedMount  13s    kubelet            MountVolume.SetUp failed for volume "pvc-d7c097e6-67ec-4fae-b968-7e7056796449" : rpc error: code = DeadlineExceeded desc = context deadline exceeded 
      Warning  FailedMount  10s    kubelet            Unable to attach or mount volumes: unmounted volumes=[persistent-storage], unattached volumes=[persistent-storage kube-api-access-9j477]: timed out waiting for the condition
    ```

    -   Warning message indicating volume not mounted.

    This error is frequently caused by AWS dropping packets between an Red Hat OpenShift Service on AWS node and AWS EFS.

    Check that the following are correct:

    -   AWS firewall and Security Groups

    -   Networking: port number and IP addresses

### Uninstalling the AWS EFS CSI Driver Operator

All EFS PVs are inaccessible after uninstalling the AWS EFS CSI Driver Operator.

-   Access to the Red Hat OpenShift Service on AWS web console.



**Procedure**



To uninstall the AWS EFS CSI Driver Operator from the web console:

1.  Log in to the web console.

2.  Stop all applications that use AWS EFS PVs.

3.  Delete all AWS EFS PVs:

    1.  Click **Storage** → **PersistentVolumeClaims**.

    2.  Select each PVC that is in use by the AWS EFS CSI Driver Operator, click the drop-down menu on the far right of the PVC, and then click **Delete PersistentVolumeClaims**.

4.  Uninstall the AWS EFS CSI Driver:

    

    Before you can uninstall the Operator, you must remove the CSI driver first.

    

    1.  Click **administration** → **CustomResourceDefinitions** → **ClusterCSIDriver**.

    2.  On the **Instances** tab, for **efs.csi.aws.com**, on the far left side, click the drop-down menu, and then click **Delete ClusterCSIDriver**.

    3.  When prompted, click **Delete**.

5.  Uninstall the AWS EFS CSI Operator:

    1.  Click **Operators** → **Installed Operators**.

    2.  On the **Installed Operators** page, scroll or type AWS EFS CSI into the **Search by name** box to find the Operator, and then click it.

    3.  On the upper, right of the **Installed Operators > Operator details** page, click **Actions** → **Uninstall Operator**.

    4.  When prompted on the **Uninstall Operator** window, click the **Uninstall** button to remove the Operator from the namespace. Any applications deployed by the Operator on the cluster need to be cleaned up manually.

        After uninstalling, the AWS EFS CSI Driver Operator is no longer listed in the **Installed Operators** section of the web console.



Before you can destroy a cluster (`openshift-install destroy cluster`), you must delete the EFS volume in AWS. An Red Hat OpenShift Service on AWS cluster cannot be destroyed when there is an EFS volume that uses the cluster’s VPC. Amazon does not allow deletion of such a VPC.



### Additional resources

-   [Configuring CSI volumes](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.12/html-single/storage/index#persistent-storage-csi)

# Assuming an AWS IAM role for a service account

Red Hat OpenShift Service on AWS clusters that use the AWS Security Token Service (STS) include a pod identity webhook for use with pods that run in user-defined projects.

You can use the pod identity webhook to enable a service account to automatically assume an AWS Identity and Access Management (IAM) role in your own pods. If the assumed IAM role has the required AWS permissions, the pods can run AWS SDK operations by using temporary STS credentials.

## Understanding the pod identity webhook workflow in user-defined projects

When you install a Red Hat OpenShift Service on AWS cluster that uses the AWS Security Token Service (STS), pod identity webhook resources are included by default.

You can use the pod identity webhook to enable a service account in a user-defined project to assume an AWS Identity and Access Management (IAM) role in a pod in the same project. When the IAM role is assumed, temporary STS credentials are provided for use by the service account in the pod. If the assumed role has the necessary AWS privileges, the service account can run AWS SDK operations in the pod.

To enable the pod identity webhook for a pod, you must create a service account with an `eks.amazonaws.com/role-arn` annotation in your project. The annotation must reference the Amazon Resource Name (ARN) of the AWS IAM role that you want the service account to assume. You must also reference the service account in your `Pod` specification and deploy the pod in the same project as the service account.

**Pod identity webhook workflow in user-defined projects**

The following diagram illustrates the pod identity webhook workflow in user-defined projects:

![Pod identity webhook workflow in user-defined projects](images/pod-identity-webhook-workflow-in-user-defined-projects.png)

The workflow has the following stages:

1.  Within a user-defined project, a user creates a service account that includes an `eks.amazonaws.com/role-arn` annotation. The annotation points to the ARN of the AWS IAM role that you want your service account to assume.

2.  When a pod is deployed in the same project using a configuration that references the annotated service account, the pod identity webhook mutates the pod. The mutation injects the following components into the pod without the need to specify them in your `Pod` or `Deployment` resource configurations:

    -   An `$AWS_ARN_ROLE` environment variable that contains the ARN for the IAM role that has the permissions required to run AWS SDK operations.

    -   An `$AWS_WEB_IDENTITY_TOKEN_FILE` environment variable that contains the full path in the pod to the OpenID Connect (OIDC) token for the service account. The full path is `/var/run/secrets/eks.amazonaws.com/serviceaccount/token`.

    -   An `aws-iam-token` volume mounted on the mount point `/var/run/secrets/eks.amazonaws.com/serviceaccount`. An OIDC token file named `token` is contained in the volume.

3.  The OIDC token is passed from the pod to the OIDC provider. The provider authenticates the service account identity if the following requirements are met:

    -   The identity signature is valid and signed by the private key.

    -   The `sts.amazonaws.com` audience is listed in the OIDC token and matches the audience configured in the OIDC provider.

        

        The pod identity webhook applies the `sts.amazonaws.com` audience to the OIDC token by default.

        In Red Hat OpenShift Service on AWS with STS clusters, the OIDC provider is created during install and set as the service account issuer by default. The `sts.amazonaws.com` audience is set by default in the OIDC provider.

        

    -   The OIDC token has not expired.

    -   The issuer value in the token contains the URL for the OIDC provider.

4.  If the project and service account are in the scope of the trust policy for the IAM role that is being assumed, then authorization succeeds.

5.  After successful authentication and authorization, temporary AWS STS credentials in the form of a session token are passed to the pod for use by the service account. By using the credentials, the service account is temporarily granted the AWS permissions enabled in the IAM role.

6.  When you run AWS SDK operations in the pod, the service account provides the temporary STS credentials to the AWS API to verify its identity.

## Assuming an AWS IAM role in your own pods

Follow the procedures in this section to enable a service account to assume an AWS Identity and Access Management (IAM) role in a pod deployed in a user-defined project.

You can create the required resources, including an AWS IAM role, a service account, a container image that includes an AWS SDK, and a pod deployed by using the image. In the example, the AWS Boto3 SDK for Python is used. You can also verify that the pod identity webhook mutates the AWS environment variables, the volume mount, and the token volume into your pod. Additionally, you can check that the service account assumes the AWS IAM role in your pod and can successfully run AWS SDK operations.

### Setting up an AWS IAM role for a service account

Create an AWS Identity and Access Management (IAM) role to be assumed by a service account in your Red Hat OpenShift Service on AWS cluster. Attach the permissions that are required by your service account to run AWS SDK operations in a pod.

-   You have the permissions required to install and configure IAM roles in your AWS account.

-   You have access to a Red Hat OpenShift Service on AWS cluster that uses the AWS Security Token Service (STS). Admin-level user privileges are not required.

-   You have the Amazon Resource Name (ARN) for the OpenID Connect (OIDC) provider that is configured as the service account issuer in your Red Hat OpenShift Service on AWS with STS cluster.

    

    In Red Hat OpenShift Service on AWS with STS clusters, the OIDC provider is created during install and set as the service account issuer by default. If you do not know the OIDC provider ARN, contact your cluster administrator.

    

-   You have installed the AWS CLI (`aws`).

1.  Create a file named `trust-policy.json` with the following JSON configuration:

    ``` json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": "<oidc_provider_arn>" 
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                    "StringEquals": {
                        "<oidc_provider_name>:sub": "system:serviceaccount:<project_name>:<service_account_name>" 
                    }
                }
            }
        ]
    }
    ```

    -   Replace `<oidc_provider_arn>` with the ARN of your OIDC provider, for example `arn:aws:iam::<aws_account_id>:oidc-provider/rh-oidc.s3.us-east-1.amazonaws.com/1v3r0n44npxu4g58so46aeohduomfres`.

    -   Limits the role to the specified project and service account. Replace `<oidc_provider_name>` with the name of your OIDC provider, for example `rh-oidc.s3.us-east-1.amazonaws.com/1v3r0n44npxu4g58so46aeohduomfres`. Replace `<project_name>:<service_account_name>` with your project name and service account name, for example `my-project:test-service-account`.

        

        Alternatively, you can limit the role to any service account within the specified project by using `"<oidc_provider_name>:sub": "system:serviceaccount:<project_name>:*"`. If you supply the `*` wildcard, you must replace `StringEquals` with `StringLike` in the preceding line.

        

2.  Create an AWS IAM role that uses the trust policy that is defined in the `trust-policy.json` file:

    ``` terminal
    $ aws iam create-role \
        --role-name <aws_iam_role_name> \ 
        --assume-role-policy-document file://trust-policy.json 
    ```

    -   Replace `<aws_iam_role_name>` with the name of your IAM role, for example `pod-identity-test-role`.

    -   References the `trust-policy.json` file that you created in the preceding step.

    

    **Example output:**

    

    ``` terminal
    ROLE    arn:aws:iam::<aws_account_id>:role/<aws_iam_role_name>        2022-09-28T12:03:17+00:00       /       AQWMS3TB4Z2N3SH7675JK   <aws_iam_role_name>
    ASSUMEROLEPOLICYDOCUMENT        2012-10-17
    STATEMENT       sts:AssumeRoleWithWebIdentity   Allow
    STRINGEQUALS    system:serviceaccount:<project_name>:<service_account_name>
    PRINCIPAL       <oidc_provider_arn>
    ```

    Retain the ARN for the role in the output. The format of the role ARN is `arn:aws:iam::<aws_account_id>:role/<aws_iam_role_name>`.

3.  Attach any managed AWS permissions that are required when the service account runs AWS SDK operations in your pod:

    ``` terminal
    $ aws iam attach-role-policy \
        --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess \ 
        --role-name <aws_iam_role_name> 
    ```

    -   The policy in this example adds read-only access permissions to the IAM role.

    -   Replace `<aws_iam_role_name>` with the name of the IAM role that you created in the preceding step.

4.  Optional: Add custom attributes or a permissions boundary to the role. For more information, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) in the AWS documentation.

### Creating a service account in your project

Add a service account in your user-defined project. Include an `eks.amazonaws.com/role-arn` annotation in the service account configuration that references the Amazon Resource Name (ARN) for the AWS Identity and Access Management (IAM) role that you want the service account to assume.

-   You have created an AWS IAM role for your service account. For more information, see *Setting up an AWS IAM role for a service account*.

-   You have access to a Red Hat OpenShift Service on AWS with AWS Security Token Service (STS) cluster. Admin-level user privileges are not required.

-   You have installed the OpenShift CLI (`oc`).

1.  In your Red Hat OpenShift Service on AWS cluster, create a project:

    ``` terminal
    $ oc new-project <project_name> 
    ```

    -   Replace `<project_name>` with the name of your project. The name must match the project name that you specified in your AWS IAM role configuration.

    

    You are automatically switched to the project when it is created.

    

2.  Create a file named `test-service-account.yaml` with the following service account configuration:

    ``` yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: <service_account_name> 
      namespace: <project_name> 
      annotations:
        eks.amazonaws.com/role-arn: "<aws_iam_role_arn>" 
    ```

    -   Replace `<service_account_name>` with the name of your service account. The name must match the service account name that you specified in your AWS IAM role configuration.

    -   Replace `<project_name>` with the name of your project. The name must match the project name that you specified in your AWS IAM role configuration.

    -   Specifies the ARN of the AWS IAM role that the service account assumes for use within your pod. Replace `<aws_iam_role_arn>` with the ARN for the AWS IAM role that you created for your service account. The format of the role ARN is `arn:aws:iam::<aws_account_id>:role/<aws_iam_role_name>`.

3.  Create the service account in your project:

    ``` terminal
    $ oc create -f test-service-account.yaml
    ```

    

    **Example output:**

    

    ``` terminal
    serviceaccount/<service_account_name> created
    ```

4.  Review the details of the service account:

    ``` terminal
    $ oc describe serviceaccount <service_account_name> 
    ```

    -   Replace `<service_account_name>` with the name of your service account.

    

    **Example output:**

    

    ``` terminal
    Name:                <service_account_name> 
    Namespace:           <project_name> 
    Labels:              <none>
    Annotations:         eks.amazonaws.com/role-arn: <aws_iam_role_arn> 
    Image pull secrets:  <service_account_name>-dockercfg-rnjkq
    Mountable secrets:   <service_account_name>-dockercfg-rnjkq
    Tokens:              <service_account_name>-token-4gbjp
    Events:              <none>
    ```

    -   Specifies the name of the service account.

    -   Specifies the project that contains the service account.

    -   Lists the annotation for the ARN of the AWS IAM role that the service account assumes.

### Creating an example AWS SDK container image

The steps in this procedure provide an example method to create a container image that includes an AWS SDK.

The example steps use Podman to create the container image and Quay.io to host the image. For more information about Quay.io, see [Getting Started with Quay.io](https://docs.quay.io/solution/getting-started.html). The container image can be used to deploy pods that can run AWS SDK operations.



In this example procedure, the AWS Boto3 SDK for Python is installed into a container image. For more information about installing and using the AWS Boto3 SDK, see the [AWS Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). For details about other AWS SDKs, see [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html) in the AWS documentation.



-   You have installed Podman on your installation host.

-   You have a Quay.io user account.

1.  Add the following configuration to a file named `Containerfile`:

    ``` terminal
    FROM ubi9/ubi 
    RUN dnf makecache && dnf install -y python3-pip && dnf clean all && pip3 install boto3>=1.15.0 
    ```

    -   Specifies the Red Hat Universal Base Image version 9.

    -   Installs the AWS Boto3 SDK by using the `pip` package management system. In this example, AWS Boto3 SDK version 1.15.0 or later is installed.

2.  From the directory that contains the file, build a container image named `awsboto3sdk`:

    ``` terminal
    $ podman build -t awsboto3sdk .
    ```

3.  Log in to Quay.io:

    ``` terminal
    $ podman login quay.io
    ```

4.  Tag the image in preparation for the upload to Quay.io:

    ``` terminal
    $ podman tag localhost/awsboto3sdk quay.io/<quay_username>/awsboto3sdk:latest 
    ```

    -   Replace `<quay_username>` with your Quay.io username.

5.  Push the tagged container image to Quay.io:

    ``` terminal
    $ podman push quay.io/<quay_username>/awsboto3sdk:latest 
    ```

    -   Replace `<quay_username>` with your Quay.io username.

6.  Make the Quay.io repository that contains the image public. This publishes the image so that it can be used to deploy a pod in your Red Hat OpenShift Service on AWS cluster:

    1.  On <https://quay.io/>, navigate to the **Repository Settings** page for repository that contains the image.

    2.  Click **Make Public** to make the repository publicly available.

### Deploying a pod that includes an AWS SDK

Deploy a pod in a user-defined project from a container image that includes an AWS SDK. In your pod configuration, specify the service account that includes the `eks.amazonaws.com/role-arn` annotation.

With the service account reference in place for your pod, the pod identity webhook injects the AWS environment variables, the volume mount, and the token volume into your pod. The pod mutation enables the service account to automatically assume the AWS IAM role in the pod.

-   You have created an AWS Identity and Access Management (IAM) role for your service account. For more information, see *Setting up an AWS IAM role for a service account*.

-   You have access to a Red Hat OpenShift Service on AWS cluster that uses the AWS Security Token Service (STS). Admin-level user privileges are not required.

-   You have installed the OpenShift CLI (`oc`).

-   You have created a service account in your project that includes an `eks.amazonaws.com/role-arn` annotation that references the Amazon Resource Name (ARN) for the IAM role that you want the service account to assume.

-   You have a container image that includes an AWS SDK and the image is available to your cluster. For detailed steps, see *Creating an example AWS SDK container image*.

    

    In this example procedure, the AWS Boto3 SDK for Python is used. For more information about installing and using the AWS Boto3 SDK, see the [AWS Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). For details about other AWS SDKs, see [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html) in the AWS documentation.

    

1.  Create a file named `awsboto3sdk-pod.yaml` with the following pod configuration:

    ``` yaml
    apiVersion: v1
    kind: Pod
    metadata:
      namespace: <project_name> 
      name: awsboto3sdk 
    spec:
      serviceAccountName: <service_account_name> 
      containers:
      - name: awsboto3sdk
        image: quay.io/<quay_username>/awsboto3sdk:latest 
        command:
        - /bin/bash
        - "-c"
        - "sleep 100000" 
      terminationGracePeriodSeconds: 0
      restartPolicy: Never
    ```

    -   Replace `<project_name>` with the name of your project. The name must match the project name that you specified in your AWS IAM role configuration.

    -   Specifies the name of the pod.

    -   Replace `<service_account_name>` with the name of the service account that is configured to assume the AWS IAM role. The name must match the service account name that you specified in your AWS IAM role configuration.

    -   Specifies the location of your `awsboto3sdk` container image. Replace `<quay_username>` with your Quay.io username.

    -   In this example pod configuration, this line keeps the pod running for 100000 seconds to enable verification testing in the pod directly. For detailed verification steps, see *Verifying the assumed IAM role in your pod*.

2.  Deploy an `awsboto3sdk` pod:

    ``` terminal
    $ oc create -f awsboto3sdk-pod.yaml
    ```

    

    **Example output:**

    

    ``` terminal
    pod/awsboto3sdk created
    ```

### Verifying the assumed IAM role in your pod

After deploying an `awsboto3sdk` pod in your project, verify that the pod identity webhook has mutated the pod. Check that the required AWS environment variables, volume mount, and OIDC token volume are present within the pod.

You can also verify that the service account assumes the AWS Identity and Access Management (IAM) role for your AWS account when you run AWS SDK operations in the pod.

-   You have created an AWS IAM role for your service account. For more information, see *Setting up an AWS IAM role for a service account*.

-   You have access to a Red Hat OpenShift Service on AWS cluster that uses the AWS Security Token Service (STS). Admin-level user privileges are not required.

-   You have installed the OpenShift CLI (`oc`).

-   You have created a service account in your project that includes an `eks.amazonaws.com/role-arn` annotation that references the Amazon Resource Name (ARN) for the IAM role that you want the service account to assume.

-   You have deployed a pod in your user-defined project that includes an AWS SDK. The pod references the service account that uses the pod identity webhook to assume the AWS IAM role required to run the AWS SDK operations. For detailed steps, see *Deploying a pod that includes an AWS SDK*.

    

    In this example procedure, a pod that includes the AWS Boto3 SDK for Python is used. For more information about installing and using the AWS Boto3 SDK, see the [AWS Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). For details about other AWS SDKs, see [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html) in the AWS documentation.

    

1.  Verify that the AWS environment variables, the volume mount, and the OIDC token volume are listed in the description of the deployed `awsboto3sdk` pod:

    ``` terminal
    $ oc describe pod awsboto3sdk
    ```

    

    **Example output:**

    

    ``` terminal
    Name:         awsboto3sdk
    Namespace:    <project_name>
    ...
    Containers:
      awsboto3sdk:
        ...
        Environment:
          AWS_ROLE_ARN:                 <aws_iam_role_arn> 
          AWS_WEB_IDENTITY_TOKEN_FILE:  /var/run/secrets/eks.amazonaws.com/serviceaccount/token 
        Mounts:
          /var/run/secrets/eks.amazonaws.com/serviceaccount from aws-iam-token (ro) 
    ...
    Volumes:
      aws-iam-token: 
        Type:                    Projected (a volume that contains injected data from multiple sources)
        TokenExpirationSeconds:  86400
    ...
    ```

    -   Lists the `AWS_ROLE_ARN` environment variable that was injected into the pod by the pod identity webhook. The variable contains the ARN of the AWS IAM role to be assumed by the service account.

    -   Lists the `AWS_WEB_IDENTITY_TOKEN_FILE` environment variable that was injected into the pod by the pod identity webhook. The variable contains the full path of the OIDC token that is used to verify the service account identity.

    -   Lists the volume mount that was injected into the pod by the pod identity webhook.

    -   Lists the `aws-iam-token` volume that is mounted onto the `/var/run/secrets/eks.amazonaws.com/serviceaccount` mount point. The volume contains the OIDC token that is used to authenticate the service account to assume the AWS IAM role.

2.  Start an interactive terminal in the `awsboto3sdk` pod:

    ``` terminal
    $ oc exec -ti awsboto3sdk -- /bin/sh
    ```

3.  In the interactive terminal for the pod, verify that the `$AWS_ROLE_ARN` environment variable was mutated into the pod by the pod identity webhook:

    ``` terminal
    $ echo $AWS_ROLE_ARN
    ```

    

    **Example output:**

    

    ``` terminal
    arn:aws:iam::<aws_account_id>:role/<aws_iam_role_name> 
    ```

    -   The output must specify the ARN for the AWS IAM role that has the permissions required to run AWS SDK operations.

4.  In the interactive terminal for the pod, verify that the `$AWS_WEB_IDENTITY_TOKEN_FILE` environment variable was mutated into the pod by the pod identity webhook:

    ``` terminal
    $ echo $AWS_WEB_IDENTITY_TOKEN_FILE
    ```

    

    **Example output:**

    

    ``` terminal
    /var/run/secrets/eks.amazonaws.com/serviceaccount/token 
    ```

    -   The output must specify the full path in the pod to the OIDC token for the service account.

5.  In the interactive terminal for the pod, verify that the `aws-iam-token` volume mount containing the OIDC token file was mounted by the pod identity webhook:

    ``` terminal
    $ mount | grep -is 'eks.amazonaws.com'
    ```

    

    **Example output:**

    

    ``` terminal
    tmpfs on /run/secrets/eks.amazonaws.com/serviceaccount type tmpfs (ro,relatime,seclabel,size=13376888k)
    ```

6.  In the interactive terminal for the pod, verify that an OIDC token file named `token` is present on the `/var/run/secrets/eks.amazonaws.com/serviceaccount/` mount point:

    ``` terminal
    $ ls /var/run/secrets/eks.amazonaws.com/serviceaccount/token
    ```

    

    **Example output:**

    

    ``` terminal
    /var/run/secrets/eks.amazonaws.com/serviceaccount/token 
    ```

    -   The OIDC token file in the `aws-iam-token` volume that was mounted in the pod by the pod identity webhook. The token is used to authenticate the identity of the service account in AWS.

7.  In the pod, verify that AWS Boto3 SDK operations run successfully:

    1.  In the interactive terminal for the pod, start a Python 3 shell:

        ``` terminal
        $ python3
        ```

    2.  In the Python 3 shell, import the `boto3` module:

        ``` python
        >>> import boto3
        ```

    3.  Create a variable that includes the Boto3 `s3` service resource:

        ``` python
        >>> s3 = boto3.resource('s3')
        ```

    4.  Print the names of all of the S3 buckets in your AWS account:

        ``` python
        >>> for bucket in s3.buckets.all():
        ...     print(bucket.name)
        ...
        ```

        

        **Example output:**

        

        ``` python
        <bucket_name>
        <bucket_name>
        <bucket_name>
        ...
        ```

        If the service account successfully assumed the AWS IAM role, the output lists all of the S3 buckets that are available in your AWS account.

## Additional resources

-   For more information about using AWS IAM roles with service accounts, see [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) in the AWS documentation.

-   For information about AWS IAM role delegation, see [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html) in the AWS documentation.

-   For details about AWS SDKs, see [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html) in the AWS documentation.

-   For more information about installing and using the AWS Boto3 SDK for Python, see the [AWS Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

-   For general information about webhook admission plugins for OpenShift, see [Webhook admission plugins](https://docs.openshift.com/container-platform/4.12/architecture/admission-plug-ins.html#admission-webhooks-about_admission-plug-ins) in the OpenShift Container Platform documentation.

# Managing security context constraints

In Red Hat OpenShift Service on AWS, you can use security context constraints (SCCs) to control permissions for the pods in your cluster.

Default SCCs are created during installation and when you install some Operators or other components. As a cluster administrator, you can also create your own SCCs by using the OpenShift CLI (`oc`).



Do not modify the default SCCs. Customizing the default SCCs can lead to issues when some of the platform pods deploy or ROSA is upgraded. Additionally, the default SCC values are reset to the defaults during some cluster upgrades, which discards all customizations to those SCCs.

Instead of modifying the default SCCs, create and modify your own SCCs as needed. For detailed steps, see [Creating security context constraints](#security-context-constraints-creating_configuring-internal-oauth).



## About security context constraints

Similar to the way that RBAC resources control user access, administrators can use security context constraints (SCCs) to control permissions for pods. These permissions determine the actions that a pod can perform and what resources it can access. You can use SCCs to define a set of conditions that a pod must run with to be accepted into the system.

Security context constraints allow an administrator to control:

-   Whether a pod can run privileged containers with the `allowPrivilegedContainer` flag

-   Whether a pod is constrained with the `allowPrivilegeEscalation` flag

-   The capabilities that a container can request

-   The use of host directories as volumes

-   The SELinux context of the container

-   The container user ID

-   The use of host namespaces and networking

-   The allocation of an `FSGroup` that owns the pod volumes

-   The configuration of allowable supplemental groups

-   Whether a container requires write access to its root file system

-   The usage of volume types

-   The configuration of allowable `seccomp` profiles



Do not set the `openshift.io/run-level` label on any namespaces in Red Hat OpenShift Service on AWS. This label is for use by internal Red Hat OpenShift Service on AWS components to manage the startup of major API groups, such as the Kubernetes API server and OpenShift API server. If the `openshift.io/run-level` label is set, no SCCs are applied to pods in that namespace, causing any workloads running in that namespace to be highly privileged.



### Default security context constraints

The cluster contains several default security context constraints (SCCs) as described in the table below. Additional SCCs might be installed when you install Operators or other components to Red Hat OpenShift Service on AWS.



Do not modify the default SCCs. Customizing the default SCCs can lead to issues when some of the platform pods deploy or ROSA is upgraded. Additionally, the default SCC values are reset to the defaults during some cluster upgrades, which discards all customizations to those SCCs.

Instead of modifying the default SCCs, create and modify your own SCCs as needed. For detailed steps, see *Creating security context constraints*.



<table>
<caption>Default security context constraints</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Security context constraint</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><code>anyuid</code></p></td>
<td style="text-align: left;"><p>Provides all features of the <code>restricted</code> SCC, but allows users to run with any UID and any GID.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>hostaccess</code></p></td>
<td style="text-align: left;"><p>Allows access to all host namespaces but still requires pods to be run with a UID and SELinux context that are allocated to the namespace.</p>

<p>This SCC allows host access to namespaces, file systems, and PIDs. It should only be used by trusted pods. Grant with caution.</p>
</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>hostmount-anyuid</code></p></td>
<td style="text-align: left;"><p>Provides all the features of the <code>restricted</code> SCC, but allows host mounts and running as any UID and any GID on the system.</p>

<p>This SCC allows host file system access as any UID, including UID 0. Grant with caution.</p>
</td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>hostnetwork</code></p></td>
<td style="text-align: left;"><p>Allows using host networking and host ports but still requires pods to be run with a UID and SELinux context that are allocated to the namespace.</p>

<p>If additional workloads are run on control plane hosts, use caution when providing access to <code>hostnetwork</code>. A workload that runs <code>hostnetwork</code> on a control plane host is effectively root on the cluster and must be trusted accordingly.</p>
</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>hostnetwork-v2</code></p></td>
<td style="text-align: left;"><p>Like the <code>hostnetwork</code> SCC, but with the following differences:</p>
<ul>
<li><p><code>ALL</code> capabilities are dropped from containers.</p></li>
<li><p>The <code>NET_BIND_SERVICE</code> capability can be added explicitly.</p></li>
<li><p><code>seccompProfile</code> is set to <code>runtime/default</code> by default.</p></li>
<li><p><code>allowPrivilegeEscalation</code> must be unset or set to <code>false</code> in security contexts.</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>node-exporter</code></p></td>
<td style="text-align: left;"><p>Used for the Prometheus node exporter.</p>

<p>This SCC allows host file system access as any UID, including UID 0. Grant with caution.</p>
</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>nonroot</code></p></td>
<td style="text-align: left;"><p>Provides all features of the <code>restricted</code> SCC, but allows users to run with any non-root UID. The user must specify the UID or it must be specified in the manifest of the container runtime.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>nonroot-v2</code></p></td>
<td style="text-align: left;"><p>Like the <code>nonroot</code> SCC, but with the following differences:</p>
<ul>
<li><p><code>ALL</code> capabilities are dropped from containers.</p></li>
<li><p>The <code>NET_BIND_SERVICE</code> capability can be added explicitly.</p></li>
<li><p><code>seccompProfile</code> is set to <code>runtime/default</code> by default.</p></li>
<li><p><code>allowPrivilegeEscalation</code> must be unset or set to <code>false</code> in security contexts.</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>privileged</code></p></td>
<td style="text-align: left;"><p>Allows access to all privileged and host features and the ability to run as any user, any group, any FSGroup, and with any SELinux context.</p>

<p>This is the most relaxed SCC and should be used only for cluster administration. Grant with caution.</p>

<p>The <code>privileged</code> SCC allows:</p>
<ul>
<li><p>Users to run privileged pods</p></li>
<li><p>Pods to mount host directories as volumes</p></li>
<li><p>Pods to run as any user</p></li>
<li><p>Pods to run with any MCS label</p></li>
<li><p>Pods to use the host’s IPC namespace</p></li>
<li><p>Pods to use the host’s PID namespace</p></li>
<li><p>Pods to use any FSGroup</p></li>
<li><p>Pods to use any supplemental group</p></li>
<li><p>Pods to use any seccomp profiles</p></li>
<li><p>Pods to request any capabilities</p></li>
</ul>

<p>Setting <code>privileged: true</code> in the pod specification does not necessarily select the <code>privileged</code> SCC. The SCC that has <code>allowPrivilegedContainer: true</code> and has the highest prioritization will be chosen if the user has the permissions to use it.</p>
</td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><code>restricted</code></p></td>
<td style="text-align: left;"><p>Denies access to all host features and requires pods to be run with a UID, and SELinux context that are allocated to the namespace.</p>
<p>The <code>restricted</code> SCC:</p>
<ul>
<li><p>Ensures that pods cannot run as privileged</p></li>
<li><p>Ensures that pods cannot mount host directory volumes</p></li>
<li><p>Requires that a pod is run as a user in a pre-allocated range of UIDs</p></li>
<li><p>Requires that a pod is run with a pre-allocated MCS label</p></li>
<li><p>Allows pods to use any FSGroup</p></li>
<li><p>Allows pods to use any supplemental group</p></li>
</ul>
<p>In clusters that were upgraded from Red Hat OpenShift Service on AWS 4.10 or earlier, this SCC is available for use by any authenticated user. The <code>restricted</code> SCC is no longer available to users of new Red Hat OpenShift Service on AWS 4.11 or later installations, unless the access is explicitly granted.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><code>restricted-v2</code></p></td>
<td style="text-align: left;"><p>Like the <code>restricted</code> SCC, but with the following differences:</p>
<ul>
<li><p><code>ALL</code> capabilities are dropped from containers.</p></li>
<li><p>The <code>NET_BIND_SERVICE</code> capability can be added explicitly.</p></li>
<li><p><code>seccompProfile</code> is set to <code>runtime/default</code> by default.</p></li>
<li><p><code>allowPrivilegeEscalation</code> must be unset or set to <code>false</code> in security contexts.</p></li>
</ul>
<p>This is the most restrictive SCC provided by a new installation and will be used by default for authenticated users.</p>

<p>The <code>restricted-v2</code> SCC is the most restrictive of the SCCs that is included by default with the system. However, you can create a custom SCC that is even more restrictive. For example, you can create an SCC that restricts <code>readOnlyRootFilesystem</code> to <code>true</code>.</p>
</td>
</tr>
</tbody>
</table>

Default security context constraints

### Security context constraints settings

Security context constraints (SCCs) are composed of settings and strategies that control the security features a pod has access to. These settings fall into three categories:

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Category</th>
<th style="text-align: left;">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Controlled by a boolean</p></td>
<td style="text-align: left;"><p>Fields of this type default to the most restrictive value. For example, <code>AllowPrivilegedContainer</code> is always set to <code>false</code> if unspecified.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Controlled by an allowable set</p></td>
<td style="text-align: left;"><p>Fields of this type are checked against the set to ensure their value is allowed.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Controlled by a strategy</p></td>
<td style="text-align: left;"><p>Items that have a strategy to generate a value provide:</p>
<ul>
<li><p>A mechanism to generate the value, and</p></li>
<li><p>A mechanism to ensure that a specified value falls into the set of allowable values.</p></li>
</ul></td>
</tr>
</tbody>
</table>

CRI-O has the following default list of capabilities that are allowed for each container of a pod:

-   `CHOWN`

-   `DAC_OVERRIDE`

-   `FSETID`

-   `FOWNER`

-   `SETGID`

-   `SETUID`

-   `SETPCAP`

-   `NET_BIND_SERVICE`

-   `KILL`

The containers use the capabilities from this default list, but pod manifest authors can alter the list by requesting additional capabilities or removing some of the default behaviors. Use the `allowedCapabilities`, `defaultAddCapabilities`, and `requiredDropCapabilities` parameters to control such requests from the pods. With these parameters you can specify which capabilities can be requested, which ones must be added to each container, and which ones must be forbidden, or dropped, from each container.



You can drop all capabilites from containers by setting the `requiredDropCapabilities` parameter to `ALL`. This is what the `restricted-v2` SCC does.



### Security context constraints strategies

-   `MustRunAs` - Requires a `runAsUser` to be configured. Uses the configured `runAsUser` as the default. Validates against the configured `runAsUser`.

    

    **Example `MustRunAs` snippet**

    

    ``` yaml
    ...
    runAsUser:
      type: MustRunAs
      uid: <id>
    ...
    ```

-   `MustRunAsRange` - Requires minimum and maximum values to be defined if not using pre-allocated values. Uses the minimum as the default. Validates against the entire allowable range.

    

    **Example `MustRunAsRange` snippet**

    

    ``` yaml
    ...
    runAsUser:
      type: MustRunAsRange
      uidRangeMax: <maxvalue>
      uidRangeMin: <minvalue>
    ...
    ```

-   `MustRunAsNonRoot` - Requires that the pod be submitted with a non-zero `runAsUser` or have the `USER` directive defined in the image. No default provided.

    

    **Example `MustRunAsNonRoot` snippet**

    

    ``` yaml
    ...
    runAsUser:
      type: MustRunAsNonRoot
    ...
    ```

-   `RunAsAny` - No default provided. Allows any `runAsUser` to be specified.

    

    **Example `RunAsAny` snippet**

    

    ``` yaml
    ...
    runAsUser:
      type: RunAsAny
    ...
    ```

<!-- -->

-   `MustRunAs` - Requires `seLinuxOptions` to be configured if not using pre-allocated values. Uses `seLinuxOptions` as the default. Validates against `seLinuxOptions`.

-   `RunAsAny` - No default provided. Allows any `seLinuxOptions` to be specified.

<!-- -->

-   `MustRunAs` - Requires at least one range to be specified if not using pre-allocated values. Uses the minimum value of the first range as the default. Validates against all ranges.

-   `RunAsAny` - No default provided. Allows any `supplementalGroups` to be specified.

<!-- -->

-   `MustRunAs` - Requires at least one range to be specified if not using pre-allocated values. Uses the minimum value of the first range as the default. Validates against the first ID in the first range.

-   `RunAsAny` - No default provided. Allows any `fsGroup` ID to be specified.

### Controlling volumes

The usage of specific volume types can be controlled by setting the `volumes` field of the SCC.

The allowable values of this field correspond to the volume sources that are defined when creating a volume:

-   [`awsElasticBlockStore`](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore)

-   [`azureDisk`](https://kubernetes.io/docs/concepts/storage/volumes/#azuredisk)

-   [`azureFile`](https://kubernetes.io/docs/concepts/storage/volumes/#azurefile)

-   [`cephFS`](https://kubernetes.io/docs/concepts/storage/volumes/#cephfs)

-   [`cinder`](https://kubernetes.io/docs/concepts/storage/volumes/#cinder)

-   [`configMap`](https://kubernetes.io/docs/concepts/storage/volumes/#configmap)

-   [`downwardAPI`](https://kubernetes.io/docs/concepts/storage/volumes/#downwardapi)

-   [`emptyDir`](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)

-   [`fc`](https://kubernetes.io/docs/concepts/storage/volumes/#fc)

-   [`flexVolume`](https://kubernetes.io/docs/concepts/storage/volumes/#flexvolume)

-   [`flocker`](https://kubernetes.io/docs/concepts/storage/volumes/#flocker)

-   [`gcePersistentDisk`](https://kubernetes.io/docs/concepts/storage/volumes/#gcepersistentdisk)

-   [`gitRepo`](https://kubernetes.io/docs/concepts/storage/volumes/#gitrepo)

-   [`glusterfs`](https://kubernetes.io/docs/concepts/storage/volumes/#glusterfs)

-   [`hostPath`](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath)

-   [`iscsi`](https://kubernetes.io/docs/concepts/storage/volumes/#iscsi)

-   [`nfs`](https://kubernetes.io/docs/concepts/storage/volumes/#nfs)

-   [`persistentVolumeClaim`](https://kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim)

-   `photonPersistentDisk`

-   [`portworxVolume`](https://kubernetes.io/docs/concepts/storage/volumes/#portworxvolume)

-   [`projected`](https://kubernetes.io/docs/concepts/storage/volumes/#projected)

-   [`quobyte`](https://kubernetes.io/docs/concepts/storage/volumes/#quobyte)

-   [`rbd`](https://kubernetes.io/docs/concepts/storage/volumes/#rbd)

-   [`scaleIO`](https://kubernetes.io/docs/concepts/storage/volumes/#scaleio)

-   [`secret`](https://kubernetes.io/docs/concepts/storage/volumes/#secret)

-   [`storageos`](https://kubernetes.io/docs/concepts/storage/volumes/#storageos)

-   [`vsphereVolume`](https://kubernetes.io/docs/concepts/storage/volumes/#vspherevolume)

-   **\*** (A special value to allow the use of all volume types.)

-   `none` (A special value to disallow the use of all volumes types. Exists only for backwards compatibility.)

The recommended minimum set of allowed volumes for new SCCs are `configMap`, `downwardAPI`, `emptyDir`, `persistentVolumeClaim`, `secret`, and `projected`.



This list of allowable volume types is not exhaustive because new types are added with each release of Red Hat OpenShift Service on AWS.





For backwards compatibility, the usage of `allowHostDirVolumePlugin` overrides settings in the `volumes` field. For example, if `allowHostDirVolumePlugin` is set to false but allowed in the `volumes` field, then the `hostPath` value will be removed from `volumes`.



### Admission control

*Admission control* with SCCs allows for control over the creation of resources based on the capabilities granted to a user.

In terms of the SCCs, this means that an admission controller can inspect the user information made available in the context to retrieve an appropriate set of SCCs. Doing so ensures the pod is authorized to make requests about its operating environment or to generate a set of constraints to apply to the pod.

The set of SCCs that admission uses to authorize a pod are determined by the user identity and groups that the user belongs to. Additionally, if the pod specifies a service account, the set of allowable SCCs includes any constraints accessible to the service account.

Admission uses the following approach to create the final security context for the pod:

1.  Retrieve all SCCs available for use.

2.  Generate field values for security context settings that were not specified on the request.

3.  Validate the final settings against the available constraints.

If a matching set of constraints is found, then the pod is accepted. If the request cannot be matched to an SCC, the pod is rejected.

A pod must validate every field against the SCC. The following are examples for just two of the fields that must be validated:



These examples are in the context of a strategy using the pre-allocated values.



**An FSGroup SCC strategy of `MustRunAs`**

If the pod defines a `fsGroup` ID, then that ID must equal the default `fsGroup` ID. Otherwise, the pod is not validated by that SCC and the next SCC is evaluated.

If the `SecurityContextConstraints.fsGroup` field has value `RunAsAny` and the pod specification omits the `Pod.spec.securityContext.fsGroup`, then this field is considered valid. Note that it is possible that during validation, other SCC settings will reject other pod fields and thus cause the pod to fail.

**A `SupplementalGroups` SCC strategy of `MustRunAs`**

If the pod specification defines one or more `supplementalGroups` IDs, then the pod’s IDs must equal one of the IDs in the namespace’s `openshift.io/sa.scc.supplemental-groups` annotation. Otherwise, the pod is not validated by that SCC and the next SCC is evaluated.

If the `SecurityContextConstraints.supplementalGroups` field has value `RunAsAny` and the pod specification omits the `Pod.spec.securityContext.supplementalGroups`, then this field is considered valid. Note that it is possible that during validation, other SCC settings will reject other pod fields and thus cause the pod to fail.

### Security context constraints prioritization

Security context constraints (SCCs) have a priority field that affects the ordering when attempting to validate a request by the admission controller.

A priority value of `0` is the lowest possible priority. A nil priority is considered a `0`, or lowest, priority. Higher priority SCCs are moved to the front of the set when sorting.

When the complete set of available SCCs is determined, the SCCs are ordered in the following manner:

1.  The highest priority SCCs are ordered first.

2.  If the priorities are equal, the SCCs are sorted from most restrictive to least restrictive.

3.  If both the priorities and restrictions are equal, the SCCs are sorted by name.

By default, the `anyuid` SCC granted to cluster administrators is given priority in their SCC set. This allows cluster administrators to run pods as any user by specifying `RunAsUser` in the pod’s `SecurityContext`.

## About pre-allocated security context constraints values

The admission controller is aware of certain conditions in the security context constraints (SCCs) that trigger it to look up pre-allocated values from a namespace and populate the SCC before processing the pod. Each SCC strategy is evaluated independently of other strategies, with the pre-allocated values, where allowed, for each policy aggregated with pod specification values to make the final values for the various IDs defined in the running pod.

The following SCCs cause the admission controller to look for pre-allocated values when no ranges are defined in the pod specification:

1.  A `RunAsUser` strategy of `MustRunAsRange` with no minimum or maximum set. Admission looks for the `openshift.io/sa.scc.uid-range` annotation to populate range fields.

2.  An `SELinuxContext` strategy of `MustRunAs` with no level set. Admission looks for the `openshift.io/sa.scc.mcs` annotation to populate the level.

3.  A `FSGroup` strategy of `MustRunAs`. Admission looks for the `openshift.io/sa.scc.supplemental-groups` annotation.

4.  A `SupplementalGroups` strategy of `MustRunAs`. Admission looks for the `openshift.io/sa.scc.supplemental-groups` annotation.

During the generation phase, the security context provider uses default values for any parameter values that are not specifically set in the pod. Default values are based on the selected strategy:

1.  `RunAsAny` and `MustRunAsNonRoot` strategies do not provide default values. If the pod needs a parameter value, such as a group ID, you must define the value in the pod specification.

2.  `MustRunAs` (single value) strategies provide a default value that is always used. For example, for group IDs, even if the pod specification defines its own ID value, the namespace’s default parameter value also appears in the pod’s groups.

3.  `MustRunAsRange` and `MustRunAs` (range-based) strategies provide the minimum value of the range. As with a single value `MustRunAs` strategy, the namespace’s default parameter value appears in the running pod. If a range-based strategy is configurable with multiple ranges, it provides the minimum value of the first configured range.



`FSGroup` and `SupplementalGroups` strategies fall back to the `openshift.io/sa.scc.uid-range` annotation if the `openshift.io/sa.scc.supplemental-groups` annotation does not exist on the namespace. If neither exists, the SCC is not created.





By default, the annotation-based `FSGroup` strategy configures itself with a single range based on the minimum value for the annotation. For example, if your annotation reads `1/3`, the `FSGroup` strategy configures itself with a minimum and maximum value of `1`. If you want to allow more groups to be accepted for the `FSGroup` field, you can configure a custom SCC that does not use the annotation.





The `openshift.io/sa.scc.supplemental-groups` annotation accepts a comma-delimited list of blocks in the format of `<start>/<length` or `<start>-<end>`. The `openshift.io/sa.scc.uid-range` annotation accepts only a single block.



## Example security context constraints

The following examples show the security context constraints (SCC) format and annotations:



**Annotated `privileged` SCC**



``` yaml
allowHostDirVolumePlugin: true
allowHostIPC: true
allowHostNetwork: true
allowHostPID: true
allowHostPorts: true
allowPrivilegedContainer: true
allowedCapabilities: 
- '*'
apiVersion: security.openshift.io/v1
defaultAddCapabilities: [] 
fsGroup: 
  type: RunAsAny
groups: 
- system:cluster-admins
- system:nodes
kind: SecurityContextConstraints
metadata:
  annotations:
    kubernetes.io/description: 'privileged allows access to all privileged and host
      features and the ability to run as any user, any group, any fsGroup, and with
      any SELinux context.  WARNING: this is the most relaxed SCC and should be used
      only for cluster administration. Grant with caution.'
  creationTimestamp: null
  name: privileged
priority: null
readOnlyRootFilesystem: false
requiredDropCapabilities: 
- KILL
- MKNOD
- SETUID
- SETGID
runAsUser: 
  type: RunAsAny
seLinuxContext: 
  type: RunAsAny
seccompProfiles:
- '*'
supplementalGroups: 
  type: RunAsAny
users: 
- system:serviceaccount:default:registry
- system:serviceaccount:default:router
- system:serviceaccount:openshift-infra:build-controller
volumes: 
- '*'
```

-   A list of capabilities that a pod can request. An empty list means that none of capabilities can be requested while the special symbol `*` allows any capabilities.

-   A list of additional capabilities that are added to any pod.

-   The `FSGroup` strategy, which dictates the allowable values for the security context.

-   The groups that can access this SCC.

-   A list of capabilities to drop from a pod. Or, specify `ALL` to drop all capabilities.

-   The `runAsUser` strategy type, which dictates the allowable values for the security context.

-   The `seLinuxContext` strategy type, which dictates the allowable values for the security context.

-   The `supplementalGroups` strategy, which dictates the allowable supplemental groups for the security context.

-   The users who can access this SCC.

-   The allowable volume types for the security context. In the example, `*` allows the use of all volume types.

The `users` and `groups` fields on the SCC control which users can access the SCC. By default, cluster administrators, nodes, and the build controller are granted access to the privileged SCC. All authenticated users are granted access to the `restricted-v2` SCC.



**Without explicit `runAsUser` setting**



``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext: 
  containers:
  - name: sec-ctx-demo
    image: gcr.io/google-samples/node-hello:1.0
```

-   When a container or pod does not request a user ID under which it should be run, the effective UID depends on the SCC that emits this pod. Because the `restricted-v2` SCC is granted to all authenticated users by default, it will be available to all users and service accounts and used in most cases. The `restricted-v2` SCC uses `MustRunAsRange` strategy for constraining and defaulting the possible values of the `securityContext.runAsUser` field. The admission plugin will look for the `openshift.io/sa.scc.uid-range` annotation on the current project to populate range fields, as it does not provide this range. In the end, a container will have `runAsUser`
    equal to the first value of the range that is hard to predict because every project has different ranges.



**With explicit `runAsUser` setting**



``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:
    runAsUser: 1000 
  containers:
    - name: sec-ctx-demo
      image: gcr.io/google-samples/node-hello:1.0
```

-   A container or pod that requests a specific user ID will be accepted by Red Hat OpenShift Service on AWS only when a service account or a user is granted access to a SCC that allows such a user ID. The SCC can allow arbitrary IDs, an ID that falls into a range, or the exact user ID specific to the request.

This configuration is valid for SELinux, fsGroup, and Supplemental Groups.

## Creating security context constraints

You can create security context constraints (SCCs) by using the OpenShift CLI (`oc`).



Creating and modifying your own SCCs are advanced operations that might cause instability to your cluster. If you have questions about using your own SCCs, contact Red Hat Support. For information about contacting Red Hat support, see *Getting support*.



-   Install the OpenShift CLI (`oc`).

-   Log in to the cluster as a user with the `cluster-admin` role.

1.  Define the SCC in a YAML file named `scc-admin.yaml`:

    ``` yaml
    kind: SecurityContextConstraints
    apiVersion: security.openshift.io/v1
    metadata:
      name: scc-admin
    allowPrivilegedContainer: true
    runAsUser:
      type: RunAsAny
    seLinuxContext:
      type: RunAsAny
    fsGroup:
      type: RunAsAny
    supplementalGroups:
      type: RunAsAny
    users:
    - my-admin-user
    groups:
    - my-admin-group
    ```

    Optionally, you can drop specific capabilities for an SCC by setting the `requiredDropCapabilities` field with the desired values. Any specified capabilities are dropped from the container. To drop all capabilities, specify `ALL`. For example, to create an SCC that drops the `KILL`, `MKNOD`, and `SYS_CHROOT` capabilities, add the following to the SCC object:

    ``` yaml
    requiredDropCapabilities:
    - KILL
    - MKNOD
    - SYS_CHROOT
    ```

    

    You cannot list a capability in both `allowedCapabilities` and `requiredDropCapabilities`.

    

    CRI-O supports the same list of capability values that are found in the [Docker documentation](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities).

2.  Create the SCC by passing in the file:

    ``` terminal
    $ oc create -f scc-admin.yaml
    ```

    

    **Example output**

    

    ``` terminal
    securitycontextconstraints "scc-admin" created
    ```

-   Verify that the SCC was created:

    ``` terminal
    $ oc get scc scc-admin
    ```

    

    **Example output**

    

    ``` terminal
    NAME        PRIV      CAPS      SELINUX    RUNASUSER   FSGROUP    SUPGROUP   PRIORITY   READONLYROOTFS   VOLUMES
    scc-admin   true      []        RunAsAny   RunAsAny    RunAsAny   RunAsAny   <none>     false            [awsElasticBlockStore azureDisk azureFile cephFS cinder configMap downwardAPI emptyDir fc flexVolume flocker gcePersistentDisk gitRepo glusterfs iscsi nfs persistentVolumeClaim photonPersistentDisk quobyte rbd secret vsphere]
    ```

## Role-based access to security context constraints

You can specify SCCs as resources that are handled by RBAC. This allows you to scope access to your SCCs to a certain project or to the entire cluster. Assigning users, groups, or service accounts directly to an SCC retains cluster-wide scope.



You cannot assign a SCC to pods created in one of the default namespaces: `default`, `kube-system`, `kube-public`, `openshift-node`, `openshift-infra`, `openshift`. These namespaces should not be used for running pods or services.



To include access to SCCs for your role, specify the `scc` resource when creating a role.

``` terminal
$ oc create role <role-name> --verb=use --resource=scc --resource-name=<scc-name> -n <namespace>
```

This results in the following role definition:

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
...
  name: role-name 
  namespace: namespace 
...
rules:
- apiGroups:
  - security.openshift.io 
  resourceNames:
  - scc-name 
  resources:
  - securitycontextconstraints 
  verbs: 
  - use
```

-   The role’s name.

-   Namespace of the defined role. Defaults to `default` if not specified.

-   The API group that includes the `SecurityContextConstraints` resource. Automatically defined when `scc` is specified as a resource.

-   An example name for an SCC you want to have access.

-   Name of the resource group that allows users to specify SCC names in the `resourceNames` field.

-   A list of verbs to apply to the role.

A local or cluster role with such a rule allows the subjects that are bound to it with a role binding or a cluster role binding to use the user-defined SCC called `scc-name`.



Because RBAC is designed to prevent escalation, even project administrators are unable to grant access to an SCC. By default, they are not allowed to use the verb `use` on SCC resources, including the `restricted-v2` SCC.



## Reference of security context constraints commands

You can manage security context constraints (SCCs) in your instance as normal API objects using the OpenShift CLI (`oc`).

### Listing security context constraints

To get a current list of SCCs:

``` terminal
$ oc get scc
```



**Example output**



``` terminal
NAME                              PRIV    CAPS                   SELINUX     RUNASUSER          FSGROUP     SUPGROUP    PRIORITY     READONLYROOTFS   VOLUMES
anyuid                            false   <no value>             MustRunAs   RunAsAny           RunAsAny    RunAsAny    10           false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
hostaccess                        false   <no value>             MustRunAs   MustRunAsRange     MustRunAs   RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","hostPath","persistentVolumeClaim","projected","secret"]
hostmount-anyuid                  false   <no value>             MustRunAs   RunAsAny           RunAsAny    RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","hostPath","nfs","persistentVolumeClaim","projected","secret"]
hostnetwork                       false   <no value>             MustRunAs   MustRunAsRange     MustRunAs   MustRunAs   <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
hostnetwork-v2                    false   ["NET_BIND_SERVICE"]   MustRunAs   MustRunAsRange     MustRunAs   MustRunAs   <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
node-exporter                     true    <no value>             RunAsAny    RunAsAny           RunAsAny    RunAsAny    <no value>   false            ["*"]
nonroot                           false   <no value>             MustRunAs   MustRunAsNonRoot   RunAsAny    RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
nonroot-v2                        false   ["NET_BIND_SERVICE"]   MustRunAs   MustRunAsNonRoot   RunAsAny    RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
privileged                        true    ["*"]                  RunAsAny    RunAsAny           RunAsAny    RunAsAny    <no value>   false            ["*"]
restricted                        false   <no value>             MustRunAs   MustRunAsRange     MustRunAs   RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
restricted-v2                     false   ["NET_BIND_SERVICE"]   MustRunAs   MustRunAsRange     MustRunAs   RunAsAny    <no value>   false            ["configMap","downwardAPI","emptyDir","persistentVolumeClaim","projected","secret"]
```

### Examining security context constraints

You can view information about a particular SCC, including which users, service accounts, and groups the SCC is applied to.

For example, to examine the `restricted` SCC:

``` terminal
$ oc describe scc restricted
```



**Example output**



``` terminal
Name:                                  restricted
Priority:                              <none>
Access:
  Users:                               <none> 
  Groups:                              <none> 
Settings:
  Allow Privileged:                    false
  Allow Privilege Escalation:          true
  Default Add Capabilities:            <none>
  Required Drop Capabilities:          KILL,MKNOD,SETUID,SETGID
  Allowed Capabilities:                <none>
  Allowed Seccomp Profiles:            <none>
  Allowed Volume Types:                configMap,downwardAPI,emptyDir,persistentVolumeClaim,projected,secret
  Allowed Flexvolumes:                 <all>
  Allowed Unsafe Sysctls:              <none>
  Forbidden Sysctls:                   <none>
  Allow Host Network:                  false
  Allow Host Ports:                    false
  Allow Host PID:                      false
  Allow Host IPC:                      false
  Read Only Root Filesystem:           false
  Run As User Strategy: MustRunAsRange
    UID:                               <none>
    UID Range Min:                     <none>
    UID Range Max:                     <none>
  SELinux Context Strategy: MustRunAs
    User:                              <none>
    Role:                              <none>
    Type:                              <none>
    Level:                             <none>
  FSGroup Strategy: MustRunAs
    Ranges:                            <none>
  Supplemental Groups Strategy: RunAsAny
    Ranges:                            <none>
```

-   Lists which users and service accounts the SCC is applied to.

-   Lists which groups the SCC is applied to.

## Additional resources

-   [Getting support](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-getting-support)

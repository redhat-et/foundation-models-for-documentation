# Red Hat OpenShift Service on AWS quickstart guide



If you are looking for a comprehensive getting started guide for ROSA, see [Comprehensive guide to getting started with Red Hat OpenShift Service on AWS](#rosa-getting-started).



Follow this guide to quickly create a Red Hat OpenShift Service on AWS (ROSA) cluster using the Red Hat OpenShift Cluster Manager Hybrid Cloud Console, grant user access, deploy your first application, and learn how to revoke user access and delete your cluster.

The procedures in this document enable you to create a cluster that uses AWS Security Token Service (STS). For more information about using AWS STS with ROSA clusters, see [Using the AWS Security Token Service](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-understanding-aws-sts_rosa-understanding).

![Red Hat OpenShift Service on AWS](images/291_OpenShift_on_AWS_Intro_1122_docs.png)

## Prerequisites

-   You reviewed the [introduction to Red Hat OpenShift Service on AWS (ROSA)](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-understanding), and the documentation on ROSA [architecture models](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-architecture-models) and [architecture concepts](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-basic-architecture-concepts).

-   You have read the documentation on [limits and scalability](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-limits-scalability) and the [guidelines for planning your environment](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-planning-environment).

-   You have reviewed the detailed [AWS prerequisites for ROSA with STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-aws-prereqs).

-   You have the [AWS service quotas that are required to run a ROSA cluster](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-required-aws-service-quotas).

## Setting up the environment

Before you create a Red Hat OpenShift Service on AWS (ROSA) cluster, you must set up your environment by completing the following tasks:

-   Enable ROSA in your AWS account.

-   Install and configure the required command line interface (CLI) tools.

-   Verify the configuration of the CLI tools.

-   Verify that the AWS Elastic Load Balancing (ELB) service role exists.

-   Verify that the required AWS resource quotas are available.

You can follow the procedures in this section to complete these setup requirements.

**Enabling ROSA in your AWS account**

Use the steps in this procedure to enable Red Hat OpenShift Service on AWS (ROSA) in your AWS account.

-   You created an AWS account.

    

    Consider using a dedicated AWS account to run production clusters. If you are using AWS Organizations, you can use an AWS account within your organization or [create a new one](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html#orgs_manage_accounts_create-new).

    

1.  Sign in to the [AWS Management Console](https://console.aws.amazon.com/rosa/home).

2.  Activate ROSA in your AWS account by navigating to the [ROSA service](https://console.aws.amazon.com/rosa/home) and selecting **Enable OpenShift**.

**Installing and configuring the required CLI tools**

Use the following steps to install and configure on your workstation.

1.  Install and configure the latest AWS CLI (`aws`).

    1.  Follow the [AWS Command Line Interface](https://aws.amazon.com/cli/) documentation to install and configure the AWS CLI for your operating system.

        Specify your `aws_access_key_id`, `aws_secret_access_key`, and `region` in the `.aws/credentials` file. See [AWS Configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) in the AWS documentation.

        

        You can alternatively use the `AWS_DEFAULT_REGION` environment variable to set the default AWS region.

        

    2.  Query the AWS API to verify if the AWS CLI is installed and configured correctly:

        ``` terminal
        $ aws sts get-caller-identity
        ```

        

        **Example output**

        

        ``` terminal
        <aws_account_id>    arn:aws:iam::<aws_account_id>:user/<username>  <aws_user_id>
        ```

2.  Install and configure the latest ROSA CLI (`rosa`).

    1.  Download the latest version of the `rosa` CLI for your operating system from the [**Downloads**](https://console.redhat.com/openshift/downloads) page on the Red Hat OpenShift Cluster Manager Hybrid Cloud Console.

    2.  Extract the `rosa` binary file from the downloaded archive. The following example extracts the binary from a Linux tar archive:

        ``` terminal
        $ tar xvf rosa-linux.tar.gz
        ```

    3.  Add `rosa` to your path. In the following example, the `/usr/local/bin` directory is included in the path of the user:

        ``` terminal
        $ sudo mv rosa /usr/local/bin/rosa
        ```

    4.  Verify if the `rosa` CLI tool is installed correctly by querying the `rosa` version:

        ``` terminal
        $ rosa version
        ```

        

        **Example output**

        

        ``` terminal
        1.2.8
        ```

    5.  Log in to your Red Hat account by using the `rosa` CLI:

        ``` terminal
        $ rosa login
        ```

        

        **Example output**

        

        ``` terminal
        To login to your Red Hat account, get an offline access token at https://console.redhat.com/openshift/token/rosa
        ? Copy the token and paste it here:
        ```

        Go to the URL listed in the command output to obtain an offline access token. Specify the token at the CLI prompt to log in.

        

        You can subsequently specify the offline access token by using the `--token="<offline_access_token>"` argument when you run the `rosa login` command.

        

    6.  Verify if you are logged in successfully and check your credentials:

        ``` terminal
        $ rosa whoami
        ```

        

        **Example output**

        

        ``` terminal
        AWS Account ID:               <aws_account_number>
        AWS Default Region:           us-east-1
        AWS ARN:                      arn:aws:iam::<aws_account_number>:user/<aws_user_name>
        OCM API:                      https://api.openshift.com
        OCM Account ID:               <red_hat_account_id>
        OCM Account Name:             Your Name
        OCM Account Username:         you@domain.com
        OCM Account Email:            you@domain.com
        OCM Organization ID:          <org_id>
        OCM Organization Name:        Your organization
        OCM Organization External ID: <external_org_id>
        ```

        Check that the information in the output is correct before proceeding.

**Creating the ELB service role**

Check if the `AWSServiceRoleForElasticLoadBalancing` AWS Elastic Load Balancing (ELB) service role exists and if not, create it.



`Error creating network Load Balancer: AccessDenied:` is produced if you attempt to create a Red Hat OpenShift Service on AWS (ROSA) cluster without the AWS ELB service role in place.



1.  Check if the `AWSServiceRoleForElasticLoadBalancing` role exists for your AWS account:

    ``` terminal
    $ aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
    ```

    

    **Example output**

    

    The following example output confirms that the role exists:

    ``` terminal
    ROLE    arn:aws:iam::<aws_account_number>:role/aws-service-role/elasticloadbalancing.amazonaws.com/AWSServiceRoleForElasticLoadBalancing  2018-09-27T19:49:23+00:00       Allows ELB to call AWS services on your behalf. 3600      /aws-service-role/elasticloadbalancing.amazonaws.com/   <role_id>   AWSServiceRoleForElasticLoadBalancing
    ASSUMEROLEPOLICYDOCUMENT        2012-10-17
    STATEMENT       sts:AssumeRole  Allow
    PRINCIPAL       elasticloadbalancing.amazonaws.com
    ROLELASTUSED    2022-01-06T09:27:57+00:00       us-east-1
    ```

2.  If the AWS ELB service role does not exist, create it:

    ``` terminal
    $ aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
    ```

**Verifying AWS quota availability**

Verify that the required resource quotas are available for your account in the default AWS region.

1.  Verify if the required resource quotas are available in your default region:

    ``` terminal
    $ rosa verify quota
    ```

    

    **Example output**

    

    ``` terminal
    I: Validating AWS quota...
    I: AWS quota ok. If cluster installation fails, validate actual AWS resource usage against https://docs.openshift.com/rosa/rosa_getting_started/rosa-required-aws-service-quotas.html
    ```

## Creating a ROSA cluster with AWS STS using the default auto mode

The procedures in this document use the `auto` modes in the OpenShift Cluster Manager Hybrid Cloud Console to immediately create the required Identity and Access Management (IAM) resources using the current AWS account. The required resources include the account-wide IAM roles and policies, cluster-specific Operator roles and policies, and OpenID Connect (OIDC) identity provider.

When using the OpenShift Cluster Manager Hybrid Cloud Console to create a Red Hat OpenShift Service on AWS (ROSA) cluster that uses the STS, you can select the default options to create the cluster quickly.

Before you can use the OpenShift Cluster Manager Hybrid Cloud Console to deploy ROSA with STS clusters, you must associate your AWS account with your Red Hat organization and create the required account-wide STS roles and policies.

**Overview of the default cluster specifications**

You can quickly create a Red Hat OpenShift Service on AWS (ROSA) cluster with the AWS Security Token Service (STS) by using the default installation options. The following summary describes the default cluster specifications.

<table>
<caption>Default ROSA with STS cluster specifications</caption>
<colgroup>
<col style="width: 25%" />
<col style="width: 75%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Component</th>
<th style="text-align: left;">Default specifications</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Accounts and roles</p></td>
<td style="text-align: left;"><ul>
<li><p>Default IAM role prefix: <code>ManagedOpenShift</code></p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Cluster settings</p></td>
<td style="text-align: left;"><ul>
<li><p>Default cluster version: Latest</p></li>
<li><p>Default AWS region for installations using the Red Hat OpenShift Cluster Manager Hybrid Cloud Console: us-east-1 (US East, North Virginia)</p></li>
<li><p>Default AWS region for installations using the <code>rosa</code> CLI: Defined by your <code>aws</code> CLI configuration</p></li>
<li><p>Availability: Single zone</p></li>
<li><p>Monitoring for user-defined projects: Enabled</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Encryption</p></td>
<td style="text-align: left;"><ul>
<li><p>Cloud storage is encrypted at rest</p></li>
<li><p>Additional etcd encryption is not enabled</p></li>
<li><p>The default AWS Key Management Service (KMS) key is used as the encryption key for persistent data</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Control plane node configuration</p></td>
<td style="text-align: left;"><ul>
<li><p>Control plane node instance type: m5.2xlarge (8 vCPU, 32 GiB RAM)</p></li>
<li><p>Control plane node count: 3</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Infrastructure node configuration</p></td>
<td style="text-align: left;"><ul>
<li><p>Infrastructure node instance type: r5.xlarge (4 vCPU, 32 GiB RAM)</p></li>
<li><p>Infrastructure node count: 2</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Compute node machine pool</p></td>
<td style="text-align: left;"><ul>
<li><p>Compute node instance type: m5.xlarge (4 vCPU 16, GiB RAM)</p></li>
<li><p>Compute node count: 2</p></li>
<li><p>Autoscaling: Not enabled</p></li>
<li><p>No additional node labels</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Networking configuration</p></td>
<td style="text-align: left;"><ul>
<li><p>Cluster privacy: Public</p></li>
<li><p>A new VPC is created for your cluster</p></li>
<li><p>No cluster-wide proxy is configured</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Classless Inter-Domain Routing (CIDR) ranges</p></td>
<td style="text-align: left;"><ul>
<li><p>Machine CIDR: 10.0.0.0/16</p></li>
<li><p>Service CIDR: 172.30.0.0/16</p></li>
<li><p>Pod CIDR: 10.128.0.0/16</p></li>
<li><p>Host prefix: /23</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Cluster roles and policies</p></td>
<td style="text-align: left;"><ul>
<li><p>Mode used to create the Operator roles and the OpenID Connect (OIDC) provider: <code>auto</code></p>

<p>For installations using the OpenShift Cluster Manager Hybrid Cloud Console, the <code>auto</code> mode requires an admin-privileged OpenShift Cluster Manager role.</p>
</li>
<li><p>Default Operator role prefix: <code>&lt;cluster_name&gt;-&lt;4_digit_random_string&gt;</code></p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Cluster update strategy</p></td>
<td style="text-align: left;"><ul>
<li><p>Individual updates</p></li>
<li><p>1 hour grace period for node draining</p></li>
</ul></td>
</tr>
</tbody>
</table>

Default ROSA with STS cluster specifications

**Understanding AWS account association**

Before you can use the Red Hat OpenShift Cluster Manager Hybrid Cloud Console to create Red Hat OpenShift Service on AWS (ROSA) clusters that use the AWS Security Token Service (STS), you must associate your AWS account with your Red Hat organization. You can associate your account by creating and linking the following IAM roles.

OpenShift Cluster Manager role  
Create an OpenShift Cluster Manager IAM role and link it to your Red Hat organization.

You can apply basic or administrative permissions to the OpenShift Cluster Manager role. The basic permissions enable cluster maintenance using the OpenShift Cluster Manager Hybrid Cloud Console. The administrative permissions enable automatic deployment of the cluster-specific Operator roles and the OpenID Connect (OIDC) provider using the OpenShift Cluster Manager Hybrid Cloud Console.

User role  
Create a user IAM role and link it to your Red Hat user account. The Red Hat user account must exist in the Red Hat organization that is linked to your OpenShift Cluster Manager role.

The user role is used by Red Hat to verify your AWS identity when you use the OpenShift Cluster Manager Hybrid Cloud Console to install a cluster and the required STS resources.

**Associating your AWS account with your Red Hat organization**

Before using the Red Hat OpenShift Cluster Manager Hybrid Cloud Console to create Red Hat OpenShift Service on AWS (ROSA) clusters that use the AWS Security Token Service (STS), create an OpenShift Cluster Manager IAM role and link it to your Red Hat organization. Then, create a user IAM role and link it to your Red Hat user account in the same Red Hat organization.

1.  Create an OpenShift Cluster Manager role and link it to your Red Hat organization:

    

    To enable automatic deployment of the cluster-specific Operator roles and the OpenID Connect (OIDC) provider using the OpenShift Cluster Manager Hybrid Cloud Console, you must apply the administrative privileges to the role by choosing the *Admin OCM role* command in the **Accounts and roles** step of creating a ROSA cluster. For more information about the basic and administrative privileges for the OpenShift Cluster Manager role, see *Understanding AWS account association*.

    

    

    If you choose the *Basic OCM role* command in the **Accounts and roles** step of creating a ROSA cluster in the OpenShift Cluster Manager Hybrid Cloud Console, you must deploy a ROSA cluster using manual mode. You will be prompted to configure the cluster-specific Operator roles and the OpenID Connect (OIDC) provider in a later step.

    

    ``` terminal
    $ rosa create ocm-role
    ```

    Select the default values at the prompts to quickly create and link the role.

2.  Create a user role and link it to your OpenShift Cluster Manager user account:

    ``` terminal
    $ rosa create user-role
    ```

    Select the default values at the prompts to quickly create and link the role.

    

    The Red Hat user account must exist in the Red Hat organization that is linked to your OpenShift Cluster Manager role.

    

**Creating the account-wide STS roles and policies**

Before using the Red Hat OpenShift Cluster Manager Hybrid Cloud Console to create Red Hat OpenShift Service on AWS (ROSA) clusters that use the AWS Security Token Service (STS), create the required account-wide STS roles and policies, including the Operator policies.

1.  If they do not exist in your AWS account, create the required account-wide STS roles and policies:

    ``` terminal
    $ rosa create account-roles
    ```

    Select the default values at the prompts to quickly create the roles and policies.

**Creating a cluster with the default options using OpenShift Cluster Manager Hybrid Cloud Console**

When using the Red Hat OpenShift Cluster Manager Hybrid Cloud Console to create a Red Hat OpenShift Service on AWS (ROSA) cluster that uses the AWS Security Token Service (STS), you can select the default options to create the cluster quickly. You can also use the admin OpenShift Cluster Manager IAM role to enable automatic deployment of the cluster-specific Operator roles and the OpenID Connect (OIDC) provider.

1.  Navigate to [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift) and select **Create cluster**.

2.  On the **Create an OpenShift cluster** page, select **Create cluster** in the **Red Hat OpenShift Service on AWS (ROSA)** row.

3.  Verify that your AWS account ID is listed in the **Associated AWS accounts** drop-down menu and that the installer, support, worker, and control plane account role Amazon Resource Names (ARNs) are listed on the **Accounts and roles** page.

    

    If your AWS account ID is not listed, check that you have successfully associated your AWS account with your Red Hat organization. If your account role ARNs are not listed, check that the required account-wide STS roles exist in your AWS account.

    

4.  Click **Next**.

5.  On the **Cluster details** page, provide a **Cluster name**. Leave the default values in the remaining fields and click **Next**.

6.  To deploy a cluster quickly, leave the default options in the **Cluster settings**, **Networking**, **Cluster roles and policies**, and **Cluster updates** pages and click **Next** on each page.

7.  On the **Review your ROSA cluster** page, review the summary of your selections and click **Create cluster** to start the installation.

-   You can monitor the progress of the installation in the **Overview** page for your cluster. You can view the installation logs on the same page. Your cluster is ready when the **Status** in the **Details** section of the page is listed as **Ready**.

    

    If the installation fails or the cluster **State** does not change to **Ready** after about 40 minutes, check the installation troubleshooting documentation for details. For more information, see *Troubleshooting installations*. For steps to contact Red Hat Support for assistance, see *Getting support for Red Hat OpenShift Service on AWS*.

    

## Creating a cluster administrator user for quick cluster access

Before configuring an identity provider, you can create a user with `cluster-admin` privileges for immediate access to your Red Hat OpenShift Service on AWS (ROSA) cluster.



The cluster administrator user is useful when you need quick access to a newly deployed cluster. However, consider configuring an identity provider and granting cluster administrator privileges to the identity provider users as required. For more information about setting up an identity provider for your ROSA cluster, see *Configuring an identity provider and granting cluster access*.



1.  Create a cluster administrator user:

    ``` terminal
    $ rosa create admin --cluster=<cluster_name> 
    ```

    -   Replace `<cluster_name>` with the name of your cluster.

    

    **Example output**

    

    ``` terminal
    W: It is recommended to add an identity provider to login to this cluster. See 'rosa create idp --help' for more information.
    I: Admin account has been added to cluster '<cluster_name>'.
    I: Please securely store this generated password. If you lose this password you can delete and recreate the cluster admin user.
    I: To login, run the following command:

       oc login https://api.example-cluster.wxyz.p1.openshiftapps.com:6443 --username cluster-admin --password d7Rca-Ba4jy-YeXhs-WU42J

    I: It may take up to a minute for the account to become active.
    ```

    

    It might take approximately one minute for the `cluster-admin` user to become active.

    

-   For steps to log in to the ROSA web console, see [Accessing a cluster through the web console](#rosa-getting-started-access-cluster-web-console_rosa-quickstart-guide-ui).

## Configuring an identity provider and granting cluster access

Red Hat OpenShift Service on AWS (ROSA) includes a built-in OAuth server. After your ROSA cluster is created, you must configure OAuth to use an identity provider. You can then add members to your configured identity provider to grant them access to your cluster.

You can also grant the identity provider users with `cluster-admin` or `dedicated-admin` privileges as required.

**Configuring an identity provider**

You can configure different identity provider types for your Red Hat OpenShift Service on AWS (ROSA) cluster. Supported types include GitHub, GitHub Enterprise, GitLab, Google, LDAP, OpenID Connect and htpasswd identity providers.



The htpasswd identity provider option is included only to enable the creation of a single, static administration user. htpasswd is not supported as a general-use identity provider for Red Hat OpenShift Service on AWS.



The following procedure configures a GitHub identity provider as an example.

1.  Go to [github.com](https://github.com) and log in to your GitHub account.

2.  If you do not have an existing GitHub organization to use for identity provisioning for your ROSA cluster, create one. Follow the steps in the [GitHub documentation](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch).

3.  Configure a GitHub identity provider for your cluster that is restricted to the members of your GitHub organization.

    1.  Configure an identity provider using the interactive mode:

        ``` terminal
        $ rosa create idp --cluster=<cluster_name> --interactive 
        ```

        -   Replace `<cluster_name>` with the name of your cluster.

        

        **Example output**

        

        ``` terminal
        I: Interactive mode enabled.
        Any optional fields can be left empty and a default will be selected.
        ? Type of identity provider: github
        ? Identity provider name: github-1
        ? Restrict to members of: organizations
        ? GitHub organizations: <github_org_name> 
        ? To use GitHub as an identity provider, you must first register the application:
          - Open the following URL:
            https://github.com/organizations/<github_org_name>/settings/applications/new?oauth_application%5Bcallback_url%5D=https%3A%2F%2Foauth-openshift.apps.<cluster_name>/<random_string>.p1.openshiftapps.com%2Foauth2callback%2Fgithub-1&oauth_application%5Bname%5D=<cluster_name>&oauth_application%5Burl%5D=https%3A%2F%2Fconsole-openshift-console.apps.<cluster_name>/<random_string>.p1.openshiftapps.com
          - Click on 'Register application'
        ...
        ```

        -   Replace `<github_org_name>` with the name of your GitHub organization.

    2.  Follow the URL in the output and select **Register application** to register a new OAuth application in your GitHub organization. By registering the application, you enable the OAuth server that is built into ROSA to authenticate members of your GitHub organization into your cluster.

        

        The fields in the **Register a new OAuth application** GitHub form are automatically filled with the required values through the URL defined by the `rosa` CLI tool.

        

    3.  Use the information from your GitHub OAuth application page to populate the remaining `rosa create idp` interactive prompts.

        

        **Continued example output**

        

        ``` terminal
        ...
        ? Client ID: <github_client_id> 
        ? Client Secret: [? for help] <github_client_secret> 
        ? GitHub Enterprise Hostname (optional):
        ? Mapping method: claim 
        I: Configuring IDP for cluster '<cluster_name>'
        I: Identity Provider 'github-1' has been created.
           It will take up to 1 minute for this configuration to be enabled.
           To add cluster administrators, see 'rosa grant user --help'.
           To login into the console, open https://console-openshift-console.apps.<cluster_name>.<random_string>.p1.openshiftapps.com and click on github-1.
        ```

        -   Replace `<github_client_id>` with the client ID for your GitHub OAuth application.

        -   Replace `<github_client_secret>` with a client secret for your GitHub OAuth application.

        -   Specify `claim` as the mapping method.

        

        It might take approximately two minutes for the identity provider configuration to become active. If you have configured a `cluster-admin` user, you can watch the OAuth pods redeploy with the updated configuration by running `oc get pods -n openshift-authentication --watch`.

        

    4.  Enter the following command to verify that the identity provider has been configured correctly:

        ``` terminal
        $ rosa list idps --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        NAME        TYPE      AUTH URL
        github-1    GitHub    https://oauth-openshift.apps.<cluster_name>.<random_string>.p1.openshiftapps.com/oauth2callback/github-1
        ```

-   For detailed steps to configure each of the supported identity provider types, see [Configuring identity providers for STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-config-identity-providers).

**Granting user access to a cluster**

You can grant a user access to your Red Hat OpenShift Service on AWS (ROSA) cluster by adding them to your configured identity provider.

You can configure different types of identity providers for your ROSA cluster. The following example procedure adds a user to a GitHub organization that is configured for identity provision to the cluster.

1.  Navigate to [github.com](https://github.com) and log in to your GitHub account.

2.  Invite users that require access to the ROSA cluster to your GitHub organization. Follow the steps in [Inviting users to join your organization](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization) in the GitHub documentation.

**Granting administrator privileges to a user**

After you have added a user to your configured identity provider, you can grant the user `cluster-admin` or `dedicated-admin` privileges for your Red Hat OpenShift Service on AWS (ROSA) cluster.

-   To configure `cluster-admin` privileges for an identity provider user:

    1.  Grant the user `cluster-admin` privileges:

        ``` terminal
        $ rosa grant user cluster-admin --user=<idp_user_name> --cluster=<cluster_name> 
        ```

        -   Replace `<idp_user_name>` and `<cluster_name>` with the name of the identity provider user and your cluster name.

        

        **Example output**

        

        ``` terminal
        I: Granted role 'cluster-admins' to user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify if the user is listed as a member of the `cluster-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ID                 GROUPS
        <idp_user_name>    cluster-admins
        ```

-   To configure `dedicated-admin` privileges for an identity provider user:

    1.  Grant the user `dedicated-admin` privileges:

        ``` terminal
        $ rosa grant user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        I: Granted role 'dedicated-admins' to user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify if the user is listed as a member of the `dedicated-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ID                 GROUPS
        <idp_user_name>    dedicated-admins
        ```

## Accessing a cluster through the web console

After you have created a cluster administrator user or added a user to your configured identity provider, you can log into your Red Hat OpenShift Service on AWS (ROSA) cluster through the web console.

1.  Obtain the console URL for your cluster:

    ``` terminal
    $ rosa describe cluster -c <cluster_name> | grep Console 
    ```

    -   Replace `<cluster_name>` with the name of your cluster.

    

    **Example output**

    

    ``` terminal
    Console URL:                https://console-openshift-console.apps.example-cluster.wxyz.p1.openshiftapps.com
    ```

2.  Go to the console URL in the output of the preceding step and log in.

    -   If you created a `cluster-admin` user, log in by using the provided credentials.

    -   If you configured an identity provider for your cluster, select the identity provider name in the **Log in with…​** dialog and complete any authorization requests that are presented by your provider.

## Deploying an application from the Developer Catalog

From the Red Hat OpenShift Service on AWS web console, you can deploy a test application from the Developer Catalog and expose it with a route.

-   You logged in to [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift).

-   You created an Red Hat OpenShift Service on AWS cluster.

-   You configured an identity provider for your cluster.

-   You added your user account to the configured identity provider.

1.  From the OpenShift Cluster Manager Hybrid Cloud Console, click **Open console**.

2.  In the **Administrator** perspective, select **Home** → **Projects** → **Create Project**.

3.  Enter a name for your project and optionally add a **Display Name** and **Description**.

4.  Click **Create** to create the project.

5.  Switch to the **Developer** perspective and select **+Add**. Verify that the selected **Project** is the one that you just created.

6.  In the **Developer Catalog** dialog, select **All services**.

7.  In the **Developer Catalog** page, select **Languages** → **JavaScript** from the menu.

8.  Click **Node.js**, and then click **Create** to open the **Create Source-to-Image application** page.

    

    You might need to click **Clear All Filters** to display the **Node.js** option.

    

9.  In the **Git** section, click **Try sample**.

10. Add a unique name in the **Name** field. The value will be used to name the associated resources.

11. Confirm that **Deployment** and **Create a route** are selected.

12. Click **Create** to deploy the application. It will take a few minutes for the pods to deploy.

13. Optional: Check the status of the pods in the **Topology** pane by selecting your **nodejs** app and reviewing its sidebar. You must wait for the `nodejs` build to complete and for the `nodejs` pod to be in a **Running** state before continuing.

14. When the deployment is complete, click the route URL for the application, which has a format similar to the following:

        https://nodejs-<project>.<cluster_name>.<hash>.<region>.openshiftapps.com/

    A new tab in your browser opens with a message similar to the following:

        Welcome to your Node.js application on OpenShift

15. Optional: Delete the application and clean up the resources that you created:

    1.  In the **Administrator** perspective, navigate to **Home** → **Projects**.

    2.  Click the action menu for your project and select **Delete Project**.

## Revoking administrator privileges and user access

You can revoke `cluster-admin` or `dedicated-admin` privileges from a user by using the ROSA CLI (`rosa`).

To revoke cluster access from a user, you must remove the user from your configured identity provider.

Follow the procedures in this section to revoke administrator privileges or cluster access from a user.

**Revoking administrator privileges from a user**

Follow the steps in this section to revoke `cluster-admin` or `dedicated-admin` privileges from a user.

-   To revoke `cluster-admin` privileges from an identity provider user:

    1.  Revoke the `cluster-admin` privilege:

        ``` terminal
        $ rosa revoke user cluster-admin --user=<idp_user_name> --cluster=<cluster_name> 
        ```

        -   Replace `<idp_user_name>` and `<cluster_name>` with the name of the identity provider user and your cluster name.

        

        **Example output**

        

        ``` terminal
        ? Are you sure you want to revoke role cluster-admins from user <idp_user_name> in cluster <cluster_name>? Yes
        I: Revoked role 'cluster-admins' from user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify that the user is not listed as a member of the `cluster-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        W: There are no users configured for cluster '<cluster_name>'
        ```

-   To revoke `dedicated-admin` privileges from an identity provider user:

    1.  Revoke the `dedicated-admin` privilege:

        ``` terminal
        $ rosa revoke user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ? Are you sure you want to revoke role dedicated-admins from user <idp_user_name> in cluster <cluster_name>? Yes
        I: Revoked role 'dedicated-admins' from user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify that the user is not listed as a member of the `dedicated-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        W: There are no users configured for cluster '<cluster_name>'
        ```

**Revoking user access to a cluster**

You can revoke cluster access for an identity provider user by removing them from your configured identity provider.

You can configure different types of identity providers for your ROSA cluster. The following example procedure revokes cluster access for a member of a GitHub organization that is configured for identity provision to the cluster.

1.  Navigate to [github.com](https://github.com) and log in to your GitHub account.

2.  Remove the user from your GitHub organization. Follow the steps in [Removing a member from your organization](https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization) in the GitHub documentation.

## Deleting a ROSA cluster and the AWS STS resources

You can delete a ROSA cluster that uses the AWS Security Token Service (STS) by using the ROSA CLI (`rosa`). You can also use the ROSA CLI to delete the AWS Identity and Access Management (IAM) account-wide roles, the cluster-specific Operator roles, and the OpenID Connect (OIDC) provider. To delete the account-wide inline and Operator policies, you can use the AWS IAM Console.



Account-wide IAM roles and policies might be used by other ROSA clusters in the same AWS account. You must only remove the resources if they are not required by other clusters.



1.  Delete a cluster and watch the logs, replacing `<cluster_name>` with the name or ID of your cluster:

    ``` terminal
    $ rosa delete cluster --cluster=<cluster_name> --watch
    ```

    

    You must wait for the cluster deletion to complete before you remove the IAM roles, policies, and OIDC provider. The account-wide roles are required to delete the resources created by the installer. The cluster-specific Operator roles are required to clean-up the resources created by the OpenShift Operators. The Operators use the OIDC provider to authenticate.

    

2.  Delete the OIDC provider that the cluster Operators use to authenticate:

    ``` terminal
    $ rosa delete oidc-provider -c <cluster_id> --mode auto 
    ```

    -   Replace `<cluster_id>` with the ID of the cluster.

    

    You can use the `-y` option to automatically answer yes to the prompts.

    

3.  Delete the cluster-specific Operator IAM roles:

    ``` terminal
    $ rosa delete operator-roles -c <cluster_id> --mode auto 
    ```

    -   Replace `<cluster_id>` with the ID of the cluster.

4.  Delete the account-wide roles:

    

    Account-wide IAM roles and policies might be used by other ROSA clusters in the same AWS account. You must only remove the resources if they are not required by other clusters.

    

    ``` terminal
    $ rosa delete account-roles --prefix <prefix> --mode auto 
    ```

    -   You must include the `--<prefix>` argument. Replace `<prefix>` with the prefix of the account-wide roles to delete. If you did not specify a custom prefix when you created the account-wide roles, specify the default prefix, `ManagedOpenShift`.

5.  Delete the account-wide inline and Operator IAM policies that you created for ROSA deployments that use STS:

    1.  Log in to the [AWS IAM Console](https://console.aws.amazon.com/iamv2/home#/home).

    2.  Navigate to **Access management** → **Policies** and select the checkbox for one of the account-wide policies.

    3.  With the policy selected, click on **Actions** → **Delete** to open the delete policy dialog.

    4.  Enter the policy name to confirm the deletion and select **Delete** to delete the policy.

    5.  Repeat this step to delete each of the account-wide inline and Operator policies for the cluster.

## Next steps

-   [Adding services to a cluster using the OpenShift Cluster Manager console](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/add-on_services/#adding-service)

-   [Managing compute nodes](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/cluster_administration/#rosa-managing-worker-nodes)

-   [Configuring the monitoring stack](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/cluster_administration/#rosa-configuring-the-monitoring-stack)

## Additional resources

-   For more information about setting up accounts and ROSA clusters using AWS STS, see [Understanding the ROSA with STS deployment workflow](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-overview-of-the-deployment-workflow).

-   For information about setting up accounts and ROSA clusters without using AWS STS, see [Understanding the ROSA deployment workflow](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-understanding-the-deployment-workflow).

-   For documentation on upgrading your cluster, see [Upgrading ROSA clusters](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/upgrading/#rosa-upgrading).

# Comprehensive guide to getting started with Red Hat OpenShift Service on AWS



If you are looking for a quickstart guide for ROSA, see [Red Hat OpenShift Service on AWS quickstart guide](#rosa-quickstart-guide-ui).



Follow this getting started document to create a Red Hat OpenShift Service on AWS (ROSA) cluster, grant user access, deploy your first application, and learn how to revoke user access and delete your cluster.

You can create a ROSA cluster either with or without the AWS Security Token Service (STS). The procedures in this document enable you to create a cluster that uses AWS STS. For more information about using AWS STS with ROSA clusters, see [Using the AWS Security Token Service](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-understanding-aws-sts_rosa-understanding).

## Prerequisites

-   You reviewed the [introduction to Red Hat OpenShift Service on AWS (ROSA)](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-understanding), and the documentation on ROSA [architecture models](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-architecture-models) and [architecture concepts](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-basic-architecture-concepts).

-   You have read the documentation on [limits and scalability](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-limits-scalability) and the [guidelines for planning your environment](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-planning-environment).

-   You have reviewed the detailed [AWS prerequisites for ROSA with STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-aws-prereqs).

-   You have the [AWS service quotas that are required to run a ROSA cluster](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-required-aws-service-quotas).

## Setting up the environment

Before you create a Red Hat OpenShift Service on AWS (ROSA) cluster, you must set up your environment by completing the following tasks:

-   Enable ROSA in your AWS account.

-   Install and configure the required command line interface (CLI) tools.

-   Verify the configuration of the CLI tools.

-   Verify that the AWS Elastic Load Balancing (ELB) service role exists.

-   Verify that the required AWS resource quotas are available.

You can follow the procedures in this section to complete these setup requirements.

### Enabling ROSA in your AWS account

Use the steps in this procedure to enable Red Hat OpenShift Service on AWS (ROSA) in your AWS account.

-   You created an AWS account.

    

    Consider using a dedicated AWS account to run production clusters. If you are using AWS Organizations, you can use an AWS account within your organization or [create a new one](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html#orgs_manage_accounts_create-new).

    

1.  Sign in to the [AWS Management Console](https://console.aws.amazon.com/rosa/home).

2.  Activate ROSA in your AWS account by navigating to the [ROSA service](https://console.aws.amazon.com/rosa/home) and selecting **Enable OpenShift**.

### Installing and configuring the required CLI tools

Use the following steps to install and configure AWS, Red Hat OpenShift Service on AWS (ROSA), and OpenShift CLI tools on your workstation.

-   You have an AWS account.

-   You created a Red Hat account.

    

    You can create a Red Hat account by navigating to [console.redhat.com](https://console.redhat.com) and selecting **Register for a Red Hat account**.

    

1.  Install and configure the latest AWS CLI (`aws`).

    1.  Follow the [AWS Command Line Interface](https://aws.amazon.com/cli/) documentation to install and configure the AWS CLI for your operating system.

        Specify your `aws_access_key_id`, `aws_secret_access_key`, and `region` in the `.aws/credentials` file. See [AWS Configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) in the AWS documentation.

        

        You can alternatively use the `AWS_DEFAULT_REGION` environment variable to set the default AWS region.

        

    2.  Query the AWS API to verify if the AWS CLI is installed and configured correctly:

        ``` terminal
        $ aws sts get-caller-identity
        ```

        

        **Example output**

        

        ``` terminal
        <aws_account_id>    arn:aws:iam::<aws_account_id>:user/<username>  <aws_user_id>
        ```

2.  Install and configure the latest ROSA CLI (`rosa`).

    1.  Download the latest version of the `rosa` CLI for your operating system from the [**Downloads**](https://console.redhat.com/openshift/downloads) page on the Red Hat OpenShift Cluster Manager Hybrid Cloud Console.

    2.  Extract the `rosa` binary file from the downloaded archive. The following example extracts the binary from a Linux tar archive:

        ``` terminal
        $ tar xvf rosa-linux.tar.gz
        ```

    3.  Add `rosa` to your path. In the following example, the `/usr/local/bin` directory is included in the path of the user:

        ``` terminal
        $ sudo mv rosa /usr/local/bin/rosa
        ```

    4.  Verify if the `rosa` CLI tool is installed correctly by querying the `rosa` version:

        ``` terminal
        $ rosa version
        ```

        

        **Example output**

        

        ``` terminal
        1.2.8
        ```

    5.  Optional: Enable tab completion for the `rosa` CLI. With tab completion enabled, you can press the `Tab` key twice to automatically complete subcommands and receive command suggestions.

        `rosa` tab completion is available for different shell types. The following example enables persistent tab completion for Bash on a Linux host. The command generates a `rosa` tab completion configuration file for Bash and saves it to the `/etc/bash_completion.d/` directory:

        ``` terminal
        # rosa completion bash > /etc/bash_completion.d/rosa
        ```

        You must open a new terminal to activate the configuration.

        

        For steps to configure `rosa` tab completion for different shell types, see the help menu by running `rosa completion --help`.

        

    6.  Log in to your Red Hat account by using the `rosa` CLI:

        ``` terminal
        $ rosa login
        ```

        

        **Example output**

        

        ``` terminal
        To login to your Red Hat account, get an offline access token at https://console.redhat.com/openshift/token/rosa
        ? Copy the token and paste it here:
        ```

        Go to the URL listed in the command output to obtain an offline access token. Specify the token at the CLI prompt to log in.

        

        You can subsequently specify the offline access token by using the `--token="<offline_access_token>"` argument when you run the `rosa login` command.

        

    7.  Verify if you are logged in successfully and check your credentials:

        ``` terminal
        $ rosa whoami
        ```

        

        **Example output**

        

        ``` terminal
        AWS Account ID:               <aws_account_number>
        AWS Default Region:           us-east-1
        AWS ARN:                      arn:aws:iam::<aws_account_number>:user/<aws_user_name>
        OCM API:                      https://api.openshift.com
        OCM Account ID:               <red_hat_account_id>
        OCM Account Name:             Your Name
        OCM Account Username:         you@domain.com
        OCM Account Email:            you@domain.com
        OCM Organization ID:          <org_id>
        OCM Organization Name:        Your organization
        OCM Organization External ID: <external_org_id>
        ```

        Check that the information in the output is correct before proceeding.

3.  Install and configure the latest OpenShift CLI (`oc`).

    1.  Use the `rosa` CLI to download the latest version of the `oc` CLI:

        ``` terminal
        $ rosa download openshift-client
        ```

    2.  Extract the `oc` binary file from the downloaded archive. The following example extracts the files from a Linux tar archive:

        ``` terminal
        $ tar xvf openshift-client-linux.tar.gz
        ```

    3.  Add the `oc` binary to your path. In the following example, the `/usr/local/bin` directory is included in the path of the user:

        ``` terminal
        $ sudo mv oc /usr/local/bin/oc
        ```

    4.  Verify if the `oc` CLI is installed correctly:

        ``` terminal
        $ rosa verify openshift-client
        ```

        

        **Example output**

        

        ``` terminal
        I: Verifying whether OpenShift command-line tool is available...
        I: Current OpenShift Client Version: 4.9.12
        ```

### Creating the ELB service role

Check if the `AWSServiceRoleForElasticLoadBalancing` AWS Elastic Load Balancing (ELB) service role exists and if not, create it.



`Error creating network Load Balancer: AccessDenied:` is produced if you attempt to create a Red Hat OpenShift Service on AWS (ROSA) cluster without the AWS ELB service role in place.



-   You have an AWS account.

-   You installed and configured the latest AWS CLI (`aws`) on your workstation.

1.  Check if the `AWSServiceRoleForElasticLoadBalancing` role exists for your AWS account:

    ``` terminal
    $ aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing"
    ```

    

    **Example output**

    

    The following example output confirms that the role exists:

    ``` terminal
    ROLE    arn:aws:iam::<aws_account_number>:role/aws-service-role/elasticloadbalancing.amazonaws.com/AWSServiceRoleForElasticLoadBalancing  2018-09-27T19:49:23+00:00       Allows ELB to call AWS services on your behalf. 3600      /aws-service-role/elasticloadbalancing.amazonaws.com/   <role_id>   AWSServiceRoleForElasticLoadBalancing
    ASSUMEROLEPOLICYDOCUMENT        2012-10-17
    STATEMENT       sts:AssumeRole  Allow
    PRINCIPAL       elasticloadbalancing.amazonaws.com
    ROLELASTUSED    2022-01-06T09:27:57+00:00       us-east-1
    ```

2.  If the AWS ELB service role does not exist, create it:

    ``` terminal
    $ aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
    ```

### Verifying AWS quota availability

Verify that the required resource quotas are available for your account in the default AWS region.

-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

1.  Verify if the required resource quotas are available in your default region:

    ``` terminal
    $ rosa verify quota
    ```

    

    **Example output**

    

    ``` terminal
    I: Validating AWS quota...
    I: AWS quota ok. If cluster installation fails, validate actual AWS resource usage against https://docs.openshift.com/rosa/rosa_getting_started/rosa-required-aws-service-quotas.html
    ```

## Creating a ROSA cluster with STS

Choose from one of the following methods to deploy a Red Hat OpenShift Service on AWS (ROSA) cluster that uses the AWS Security Token Service (STS). In both scenarios, you can deploy your cluster by using Red Hat OpenShift Cluster Manager or the ROSA CLI (`rosa`):

-   **[Creating a ROSA cluster with STS using the default options](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-creating-a-cluster-quickly)**: You can create a ROSA cluster with STS quickly by using the default options and automatic STS resource creation.

-   **[Creating a ROSA cluster with STS using customizations](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-creating-a-cluster-with-customizations)**: You can create a ROSA cluster with STS using customizations. You can also choose between the `auto` and `manual` modes when creating the required STS resources.

<!-- -->

-   For detailed steps to deploy a ROSA cluster without STS, see [Creating a ROSA cluster without AWS STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-creating-cluster) and [Creating an AWS PrivateLink cluster on ROSA](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-aws-privatelink-creating-cluster).

-   For information about the account-wide IAM roles and policies that are required for ROSA deployments that use STS, see [Account-wide IAM role and policy reference](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-sts-account-wide-roles-and-policies_rosa-sts-about-iam-resources).

-   For details about using the `auto` and `manual` modes to create the required STS resources, see [Understanding the auto and manual deployment modes](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-understanding-deployment-modes_rosa-sts-creating-a-cluster-with-customizations).

-   For information about the update life cycle for ROSA, see [Red Hat OpenShift Service on AWS update life cycle](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-life-cycle).

## Creating a cluster administrator user for quick cluster access

Before configuring an identity provider, you can create a user with `cluster-admin` privileges for immediate access to your Red Hat OpenShift Service on AWS (ROSA) cluster.



The cluster administrator user is useful when you need quick access to a newly deployed cluster. However, consider configuring an identity provider and granting cluster administrator privileges to the identity provider users as required. For more information about setting up an identity provider for your ROSA cluster, see *Configuring an identity provider and granting cluster access*.



-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

1.  Create a cluster administrator user:

    ``` terminal
    $ rosa create admin --cluster=<cluster_name> 
    ```

    -   Replace `<cluster_name>` with the name of your cluster.

    

    **Example output**

    

    ``` terminal
    W: It is recommended to add an identity provider to login to this cluster. See 'rosa create idp --help' for more information.
    I: Admin account has been added to cluster '<cluster_name>'.
    I: Please securely store this generated password. If you lose this password you can delete and recreate the cluster admin user.
    I: To login, run the following command:

       oc login https://api.example-cluster.wxyz.p1.openshiftapps.com:6443 --username cluster-admin --password d7Rca-Ba4jy-YeXhs-WU42J

    I: It may take up to a minute for the account to become active.
    ```

    

    It might take approximately one minute for the `cluster-admin` user to become active.

    

2.  Log in to the cluster through the CLI:

    1.  Run the command provided in the output of the preceding step to log in:

        ``` terminal
        $ oc login <api_url> --username cluster-admin --password <cluster_admin_password> 
        ```

        -   Replace `<api_url>` and `<cluster_admin_password>` with the API URL and cluster administrator password for your environment.

    2.  Verify if you are logged in to the ROSA cluster as the `cluster-admin` user:

        ``` terminal
        $ oc whoami
        ```

        

        **Example output**

        

        ``` terminal
        cluster-admin
        ```

-   For steps to log in to the ROSA web console, see [Accessing a cluster through the web console](#rosa-getting-started-access-cluster-web-console_rosa-getting-started)

## Configuring an identity provider and granting cluster access

Red Hat OpenShift Service on AWS (ROSA) includes a built-in OAuth server. After your ROSA cluster is created, you must configure OAuth to use an identity provider. You can then add members to your configured identity provider to grant them access to your cluster.

You can also grant the identity provider users with `cluster-admin` or `dedicated-admin` privileges as required.

### Configuring an identity provider

You can configure different identity provider types for your Red Hat OpenShift Service on AWS (ROSA) cluster. Supported types include GitHub, GitHub Enterprise, GitLab, Google, LDAP, OpenID Connect and htpasswd identity providers.



The htpasswd identity provider option is included only to enable the creation of a single, static administration user. htpasswd is not supported as a general-use identity provider for Red Hat OpenShift Service on AWS.



The following procedure configures a GitHub identity provider as an example.

-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

-   You have a GitHub user account.

1.  Go to [github.com](https://github.com) and log in to your GitHub account.

2.  If you do not have an existing GitHub organization to use for identity provisioning for your ROSA cluster, create one. Follow the steps in the [GitHub documentation](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch).

3.  Configure a GitHub identity provider for your cluster that is restricted to the members of your GitHub organization.

    1.  Configure an identity provider using the interactive mode:

        ``` terminal
        $ rosa create idp --cluster=<cluster_name> --interactive 
        ```

        -   Replace `<cluster_name>` with the name of your cluster.

        

        **Example output**

        

        ``` terminal
        I: Interactive mode enabled.
        Any optional fields can be left empty and a default will be selected.
        ? Type of identity provider: github
        ? Identity provider name: github-1
        ? Restrict to members of: organizations
        ? GitHub organizations: <github_org_name> 
        ? To use GitHub as an identity provider, you must first register the application:
          - Open the following URL:
            https://github.com/organizations/<github_org_name>/settings/applications/new?oauth_application%5Bcallback_url%5D=https%3A%2F%2Foauth-openshift.apps.<cluster_name>/<random_string>.p1.openshiftapps.com%2Foauth2callback%2Fgithub-1&oauth_application%5Bname%5D=<cluster_name>&oauth_application%5Burl%5D=https%3A%2F%2Fconsole-openshift-console.apps.<cluster_name>/<random_string>.p1.openshiftapps.com
          - Click on 'Register application'
        ...
        ```

        -   Replace `<github_org_name>` with the name of your GitHub organization.

    2.  Follow the URL in the output and select **Register application** to register a new OAuth application in your GitHub organization. By registering the application, you enable the OAuth server that is built into ROSA to authenticate members of your GitHub organization into your cluster.

        

        The fields in the **Register a new OAuth application** GitHub form are automatically filled with the required values through the URL defined by the `rosa` CLI tool.

        

    3.  Use the information from your GitHub OAuth application page to populate the remaining `rosa create idp` interactive prompts.

        

        **Continued example output**

        

        ``` terminal
        ...
        ? Client ID: <github_client_id> 
        ? Client Secret: [? for help] <github_client_secret> 
        ? GitHub Enterprise Hostname (optional):
        ? Mapping method: claim 
        I: Configuring IDP for cluster '<cluster_name>'
        I: Identity Provider 'github-1' has been created.
           It will take up to 1 minute for this configuration to be enabled.
           To add cluster administrators, see 'rosa grant user --help'.
           To login into the console, open https://console-openshift-console.apps.<cluster_name>.<random_string>.p1.openshiftapps.com and click on github-1.
        ```

        -   Replace `<github_client_id>` with the client ID for your GitHub OAuth application.

        -   Replace `<github_client_secret>` with a client secret for your GitHub OAuth application.

        -   Specify `claim` as the mapping method.

        

        It might take approximately two minutes for the identity provider configuration to become active. If you have configured a `cluster-admin` user, you can watch the OAuth pods redeploy with the updated configuration by running `oc get pods -n openshift-authentication --watch`.

        

    4.  Enter the following command to verify that the identity provider has been configured correctly:

        ``` terminal
        $ rosa list idps --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        NAME        TYPE      AUTH URL
        github-1    GitHub    https://oauth-openshift.apps.<cluster_name>.<random_string>.p1.openshiftapps.com/oauth2callback/github-1
        ```

-   For detailed steps to configure each of the supported identity provider types, see [Configuring identity providers for STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-config-identity-providers)

### Granting user access to a cluster

You can grant a user access to your Red Hat OpenShift Service on AWS (ROSA) cluster by adding them to your configured identity provider.

You can configure different types of identity providers for your ROSA cluster. The following example procedure adds a user to a GitHub organization that is configured for identity provision to the cluster.

-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

-   You have a GitHub user account.

-   You have configured a GitHub identity provider for your cluster.

1.  Navigate to [github.com](https://github.com) and log in to your GitHub account.

2.  Invite users that require access to the ROSA cluster to your GitHub organization. Follow the steps in [Inviting users to join your organization](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization) in the GitHub documentation.

### Granting administrator privileges to a user

After you have added a user to your configured identity provider, you can grant the user `cluster-admin` or `dedicated-admin` privileges for your Red Hat OpenShift Service on AWS (ROSA) cluster.

-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

-   You have configured a GitHub identity provider for your cluster and added identity provider users.

<!-- -->

-   To configure `cluster-admin` privileges for an identity provider user:

    1.  Grant the user `cluster-admin` privileges:

        ``` terminal
        $ rosa grant user cluster-admin --user=<idp_user_name> --cluster=<cluster_name> 
        ```

        -   Replace `<idp_user_name>` and `<cluster_name>` with the name of the identity provider user and your cluster name.

        

        **Example output**

        

        ``` terminal
        I: Granted role 'cluster-admins' to user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify if the user is listed as a member of the `cluster-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ID                 GROUPS
        <idp_user_name>    cluster-admins
        ```

-   To configure `dedicated-admin` privileges for an identity provider user:

    1.  Grant the user `dedicated-admin` privileges:

        ``` terminal
        $ rosa grant user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        I: Granted role 'dedicated-admins' to user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify if the user is listed as a member of the `dedicated-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ID                 GROUPS
        <idp_user_name>    dedicated-admins
        ```

## Accessing a cluster through the web console

After you have created a cluster administrator user or added a user to your configured identity provider, you can log into your Red Hat OpenShift Service on AWS (ROSA) cluster through the web console.

-   You have an AWS account.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

-   You have created a cluster administrator user or added your user account to the configured identity provider.

1.  Obtain the console URL for your cluster:

    ``` terminal
    $ rosa describe cluster -c <cluster_name> | grep Console 
    ```

    -   Replace `<cluster_name>` with the name of your cluster.

    

    **Example output**

    

    ``` terminal
    Console URL:                https://console-openshift-console.apps.example-cluster.wxyz.p1.openshiftapps.com
    ```

2.  Go to the console URL in the output of the preceding step and log in.

    -   If you created a `cluster-admin` user, log in by using the provided credentials.

    -   If you configured an identity provider for your cluster, select the identity provider name in the **Log in with…​** dialog and complete any authorization requests that are presented by your provider.

## Deploying an application from the Developer Catalog

From the Red Hat OpenShift Service on AWS web console, you can deploy a test application from the Developer Catalog and expose it with a route.

-   You logged in to [OpenShift Cluster Manager Hybrid Cloud Console](https://console.redhat.com/openshift).

-   You created an Red Hat OpenShift Service on AWS cluster.

-   You configured an identity provider for your cluster.

-   You added your user account to the configured identity provider.

1.  From the OpenShift Cluster Manager Hybrid Cloud Console, click **Open console**.

2.  In the **Administrator** perspective, select **Home** → **Projects** → **Create Project**.

3.  Enter a name for your project and optionally add a **Display Name** and **Description**.

4.  Click **Create** to create the project.

5.  Switch to the **Developer** perspective and select **+Add**. Verify that the selected **Project** is the one that you just created.

6.  In the **Developer Catalog** dialog, select **All services**.

7.  In the **Developer Catalog** page, select **Languages** → **JavaScript** from the menu.

8.  Click **Node.js**, and then click **Create** to open the **Create Source-to-Image application** page.

    

    You might need to click **Clear All Filters** to display the **Node.js** option.

    

9.  In the **Git** section, click **Try sample**.

10. Add a unique name in the **Name** field. The value will be used to name the associated resources.

11. Confirm that **Deployment** and **Create a route** are selected.

12. Click **Create** to deploy the application. It will take a few minutes for the pods to deploy.

13. Optional: Check the status of the pods in the **Topology** pane by selecting your **nodejs** app and reviewing its sidebar. You must wait for the `nodejs` build to complete and for the `nodejs` pod to be in a **Running** state before continuing.

14. When the deployment is complete, click the route URL for the application, which has a format similar to the following:

        https://nodejs-<project>.<cluster_name>.<hash>.<region>.openshiftapps.com/

    A new tab in your browser opens with a message similar to the following:

        Welcome to your Node.js application on OpenShift

15. Optional: Delete the application and clean up the resources that you created:

    1.  In the **Administrator** perspective, navigate to **Home** → **Projects**.

    2.  Click the action menu for your project and select **Delete Project**.

## Revoking administrator privileges and user access

You can revoke `cluster-admin` or `dedicated-admin` privileges from a user by using the ROSA CLI (`rosa`).

To revoke cluster access from a user, you must remove the user from your configured identity provider.

Follow the procedures in this section to revoke administrator privileges or cluster access from a user.

### Revoking administrator privileges from a user

Follow the steps in this section to revoke `cluster-admin` or `dedicated-admin` privileges from a user.

-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

-   You have configured a GitHub identity provider for your cluster and added an identity provider user.

-   You granted `cluster-admin` or `dedicated-admin` privileges to a user.

<!-- -->

-   To revoke `cluster-admin` privileges from an identity provider user:

    1.  Revoke the `cluster-admin` privilege:

        ``` terminal
        $ rosa revoke user cluster-admin --user=<idp_user_name> --cluster=<cluster_name> 
        ```

        -   Replace `<idp_user_name>` and `<cluster_name>` with the name of the identity provider user and your cluster name.

        

        **Example output**

        

        ``` terminal
        ? Are you sure you want to revoke role cluster-admins from user <idp_user_name> in cluster <cluster_name>? Yes
        I: Revoked role 'cluster-admins' from user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify that the user is not listed as a member of the `cluster-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        W: There are no users configured for cluster '<cluster_name>'
        ```

-   To revoke `dedicated-admin` privileges from an identity provider user:

    1.  Revoke the `dedicated-admin` privilege:

        ``` terminal
        $ rosa revoke user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        ? Are you sure you want to revoke role dedicated-admins from user <idp_user_name> in cluster <cluster_name>? Yes
        I: Revoked role 'dedicated-admins' from user '<idp_user_name>' on cluster '<cluster_name>'
        ```

    2.  Verify that the user is not listed as a member of the `dedicated-admins` group:

        ``` terminal
        $ rosa list users --cluster=<cluster_name>
        ```

        

        **Example output**

        

        ``` terminal
        W: There are no users configured for cluster '<cluster_name>'
        ```

### Revoking user access to a cluster

You can revoke cluster access for an identity provider user by removing them from your configured identity provider.

You can configure different types of identity providers for your ROSA cluster. The following example procedure revokes cluster access for a member of a GitHub organization that is configured for identity provision to the cluster.

-   You have a ROSA cluster.

-   You have a GitHub user account.

-   You have configured a GitHub identity provider for your cluster and added an identity provider user.

1.  Navigate to [github.com](https://github.com) and log in to your GitHub account.

2.  Remove the user from your GitHub organization. Follow the steps in [Removing a member from your organization](https://docs.github.com/en/organizations/managing-membership-in-your-organization/removing-a-member-from-your-organization) in the GitHub documentation.

## Deleting a ROSA cluster and the AWS STS resources

You can delete a ROSA cluster that uses the AWS Security Token Service (STS) by using the ROSA CLI (`rosa`). You can also use the ROSA CLI to delete the AWS Identity and Access Management (IAM) account-wide roles, the cluster-specific Operator roles, and the OpenID Connect (OIDC) provider. To delete the account-wide inline and Operator policies, you can use the AWS IAM Console.



Account-wide IAM roles and policies might be used by other ROSA clusters in the same AWS account. You must only remove the resources if they are not required by other clusters.



-   You installed and configured the latest AWS (`aws`), ROSA (`rosa`), and OpenShift (`oc`) CLIs on your workstation.

-   You logged in to your Red Hat account by using the `rosa` CLI.

-   You created a ROSA cluster.

1.  Delete a cluster and watch the logs, replacing `<cluster_name>` with the name or ID of your cluster:

    ``` terminal
    $ rosa delete cluster --cluster=<cluster_name> --watch
    ```

    

    You must wait for the cluster deletion to complete before you remove the IAM roles, policies, and OIDC provider. The account-wide roles are required to delete the resources created by the installer. The cluster-specific Operator roles are required to clean-up the resources created by the OpenShift Operators. The Operators use the OIDC provider to authenticate.

    

2.  Delete the OIDC provider that the cluster Operators use to authenticate:

    ``` terminal
    $ rosa delete oidc-provider -c <cluster_id> --mode auto 
    ```

    -   Replace `<cluster_id>` with the ID of the cluster.

    

    You can use the `-y` option to automatically answer yes to the prompts.

    

3.  Delete the cluster-specific Operator IAM roles:

    ``` terminal
    $ rosa delete operator-roles -c <cluster_id> --mode auto 
    ```

    -   Replace `<cluster_id>` with the ID of the cluster.

4.  Delete the account-wide roles:

    

    Account-wide IAM roles and policies might be used by other ROSA clusters in the same AWS account. You must only remove the resources if they are not required by other clusters.

    

    ``` terminal
    $ rosa delete account-roles --prefix <prefix> --mode auto 
    ```

    -   You must include the `--<prefix>` argument. Replace `<prefix>` with the prefix of the account-wide roles to delete. If you did not specify a custom prefix when you created the account-wide roles, specify the default prefix, `ManagedOpenShift`.

5.  Delete the account-wide inline and Operator IAM policies that you created for ROSA deployments that use STS:

    1.  Log in to the [AWS IAM Console](https://console.aws.amazon.com/iamv2/home#/home).

    2.  Navigate to **Access management** → **Policies** and select the checkbox for one of the account-wide policies.

    3.  With the policy selected, click on **Actions** → **Delete** to open the delete policy dialog.

    4.  Enter the policy name to confirm the deletion and select **Delete** to delete the policy.

    5.  Repeat this step to delete each of the account-wide inline and Operator policies for the cluster.

## Next steps

-   [Adding services to a cluster using the OpenShift Cluster Manager console](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/add-on_services/#adding-service)

-   [Managing compute nodes](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/cluster_administration/#rosa-managing-worker-nodes)

-   [Configuring the monitoring stack](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/cluster_administration/#rosa-configuring-the-monitoring-stack)

## Additional resources

-   For more information about setting up accounts and ROSA clusters using AWS STS, see [Understanding the ROSA with STS deployment workflow](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-overview-of-the-deployment-workflow)

-   For information about setting up accounts and ROSA clusters without using AWS STS, see [Understanding the ROSA deployment workflow](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-understanding-the-deployment-workflow)

-   For documentation on upgrading your cluster, see [Upgrading ROSA clusters](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/upgrading/#rosa-upgrading)

# Understanding the ROSA with STS deployment workflow

Before you create a Red Hat OpenShift Service on AWS (ROSA) cluster, you must complete the AWS prerequisites, verify that the required AWS service quotas are available, and set up your environment.

This document provides an overview of the ROSA with STS deployment workflow stages and refers to detailed resources for each stage.

## Overview of the ROSA with STS deployment workflow

The AWS Security Token Service (STS) is a global web service that provides short-term credentials for IAM or federated users. You can use AWS STS with Red Hat OpenShift Service on AWS (ROSA) to allocate temporary, limited-privilege credentials for component-specific IAM roles. The service enables cluster components to make AWS API calls using secure cloud resource management practices.

You can follow the workflow stages outlined in this section to set up and access a ROSA cluster that uses STS.

1.  [Complete the AWS prerequisites for ROSA with STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-aws-prereqs). To deploy a ROSA cluster with STS, your AWS account must meet the prerequisite requirements.

2.  [Review the required AWS service quotas](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-required-aws-service-quotas). To prepare for your cluster deployment, review the AWS service quotas that are required to run a ROSA cluster.

3.  [Set up the environment and install ROSA using STS](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/prepare_your_environment/#rosa-sts-setting-up-environment). Before you create a ROSA with STS cluster, you must enable ROSA in your AWS account, install and configure the required CLI tools, and verify the configuration of the CLI tools. You must also verify that the AWS Elastic Load Balancing (ELB) service role exists and that the required AWS resource quotas are available.

4.  [Create a ROSA cluster with STS quickly](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-creating-a-cluster-quickly) or [create a cluster using customizations](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-creating-a-cluster-with-customizations). Use the ROSA CLI (`rosa`) or Red Hat OpenShift Cluster Manager to create a cluster with STS. You can create a cluster quickly by using the default options, or you can apply customizations to suit the needs
    of your organization.

5.  [Access your cluster](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-accessing-cluster). You can configure an identity provider and grant cluster administrator privileges to the identity provider users as required. You can also access a newly-deployed cluster quickly by configuring a `cluster-admin` user.

6.  [Revoke access to a ROSA cluster for a user](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-deleting-access-cluster). You can revoke access to a ROSA with STS cluster from a user by using the ROSA CLI or the web console.

7.  [Delete a ROSA cluster](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-deleting-cluster). You can delete a ROSA with STS cluster by using the ROSA CLI (`rosa`). After deleting a cluster, you can delete the STS resources by using the AWS Identity and Access Management (IAM) Console.

## Additional resources

-   For information about using the ROSA deployment workflow to create a cluster that does not use AWS STS, see [Understanding the ROSA deployment workflow](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-understanding-the-deployment-workflow).

# Getting started with the rosa CLI

Setup and basic usage of the `rosa` CLI.

## About the rosa CLI

Use the `rosa` command-line utility for Red Hat OpenShift Service on AWS (ROSA) to create, update, manage, and delete Red Hat OpenShift Service on AWS clusters and resources.

## Setting up the rosa CLI

Use the following steps to install and configure the Red Hat OpenShift Service on AWS (ROSA) CLI (`rosa`) on your installation host.

1.  Download the latest version of the `rosa` CLI for your operating system from the [**Downloads**](https://console.redhat.com/openshift/downloads) page on OpenShift Cluster Manager.

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
    1.2.6
    ```

5.  Optional: Enable tab completion for the `rosa` CLI. With tab completion enabled, you can press the `Tab` key twice to automatically complete subcommands and receive command suggestions:

    -   To enable persistent tab completion for Bash on a Linux host:

        1.  Generate a `rosa` tab completion configuration file for Bash and save it to your `/etc/bash_completion.d/` directory:

            ``` terminal
            # rosa completion bash > /etc/bash_completion.d/rosa
            ```

        2.  Open a new terminal to activate the configuration.

    -   To enable persistent tab completion for Bash on a macOS host:

        1.  Generate a `rosa` tab completion configuration file for Bash and save it to your `/usr/local/etc/bash_completion.d/` directory:

            ``` terminal
            $ rosa completion bash > /usr/local/etc/bash_completion.d/rosa
            ```

        2.  Open a new terminal to activate the configuration.

    -   To enable persistent tab completion for Zsh:

        1.  If tab completion is not enabled for your Zsh environment, enable it by running the following command:

            ``` terminal
            $ echo "autoload -U compinit; compinit" >> ~/.zshrc
            ```

        2.  Generate a `rosa` tab completion configuration file for Zsh and save it to the first directory in your functions path:

            ``` terminal
            $ rosa completion zsh > "${fpath[1]}/_rosa"
            ```

        3.  Open a new terminal to activate the configuration.

    -   To enable persistent tab completion for fish:

        1.  Generate a `rosa` tab completion configuration file for fish and save it to your `~/.config/fish/completions/` directory:

            ``` terminal
            $ rosa completion fish > ~/.config/fish/completions/rosa.fish
            ```

        2.  Open a new terminal to activate the configuration.

    -   To enable persistent tab completion for PowerShell:

        1.  Generate a `rosa` tab completion configuration file for PowerShell and save it to a file named `rosa.ps1`:

            ``` terminal
            PS> rosa completion powershell | Out-String | Invoke-Expression
            ```

        2.  Source the `rosa.ps1` file from your PowerShell profile.

    

    For more information about configuring `rosa` tab completion, see the help menu by running `rosa completion --help`.

    

## Configuring the rosa CLI

Use the following commands to configure the `rosa` CLI.

### login

Log in to your Red Hat account, saving the credentials to the `rosa` configuration file. You must provide a token when logging in. You can copy your token from [the Red Hat OpenShift Service on AWS token page](https://console.redhat.com/openshift/token/rosa).

The `rosa` CLI looks for a token in the following priority order:

1.  Command-line arguments

2.  The `ROSA_TOKEN` environment variable

3.  The `rosa` configuration file

4.  Interactively from a command-line prompt



**Syntax**



``` terminal
$ rosa login [arguments]
```

| Option          | Definition                                                                                                                                                           |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --client-id     | The OpenID client identifier (string). Default: `cloud-services`                                                                                                     |
| --client-secret | The OpenID client secret (string).                                                                                                                                   |
| --insecure      | Enables insecure communication with the server. This disables verification of TLS certificates and host names.                                                       |
| --scope         | The OpenID scope (string). If this option is used, it replaces the default scopes. This can be repeated multiple times to specify multiple scopes. Default: `openid` |
| --token         | Accesses or refreshes the token (string).                                                                                                                            |
| --token-url     | The OpenID token URL (string). Default: `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`                                           |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands

### logout

Log out of `rosa`. Logging out also removes the `rosa` configuration file.



**Syntax**



``` terminal
$ rosa logout [arguments]
```

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands

### verify permissions

Verify that the AWS permissions required to create a ROSA cluster are configured correctly:



**Syntax**



``` terminal
$ rosa verify permissions [arguments]
```



This command verifies permissions only for clusters that do not use the AWS Security Token Service (STS).



| Option       | Definition                                                                                                       |
|--------------|------------------------------------------------------------------------------------------------------------------|
| --help       | Shows help for this command.                                                                                     |
| --debug      | Enables debug mode.                                                                                              |
| --region     | The AWS region (string) in which to run the command. This value overrides the `AWS_REGION` environment variable. |
| --profile    | Specifies an AWS profile (string) from your credentials file.                                                    |
| --v \<level> | The log level for V logs.                                                                                        |

Optional arguments inherited from parent commands



**Examples**



Verify that the AWS permissions are configured correctly:

``` terminal
$ rosa verify permissions
```

Verify that the AWS permissions are configured correctly in a specific region:

``` terminal
$ rosa verify permissions --region=us-west-2
```

### verify quota

Verifies that AWS quotas are configured correctly for your default region.



**Syntax**



``` terminal
$ rosa verify quota [arguments]
```

| Option       | Definition                                                                                                       |
|--------------|------------------------------------------------------------------------------------------------------------------|
| --help       | Shows help for this command.                                                                                     |
| --debug      | Enables debug mode.                                                                                              |
| --region     | The AWS region (string) in which to run the command. This value overrides the `AWS_REGION` environment variable. |
| --profile    | Specifies an AWS profile (string) from your credentials file.                                                    |
| --v \<level> | The log level for V logs.                                                                                        |

Optional arguments inherited from parent commands



**Examples**



Verify that the AWS quotas are configured correctly for the default region:

``` terminal
$ rosa verify quota
```

Verify that the AWS quotas are configured correctly in a specific region:

``` terminal
$ rosa verify quota --region=us-west-2
```

### download oc

Download the latest compatible version of the OpenShift Container Platform CLI (`oc`).

After downloading `oc`, you must unzip the archive and add it to your path.



**Syntax**



``` terminal
$ rosa download oc [arguments]
```

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Download `oc` client tools:

``` terminal
$ rosa download oc
```

### verify oc

Verifies that the OpenShift Container Platform CLI (`oc`) is installed correctly.



**Syntax**



``` terminal
$ rosa verify oc [arguments]
```

| Option       | Definition                                                                                                     |
|--------------|----------------------------------------------------------------------------------------------------------------|
| --help       | Shows help for this command.                                                                                   |
| --debug      | Enables debug mode.                                                                                            |
| --region     | The AWS region (string) in which to run the command. This value overrides the AWS_REGION environment variable. |
| --profile    | Specifies an AWS profile (string) from your credentials file.                                                  |
| --v \<level> | The log level for V logs.                                                                                      |

Optional arguments inherited from parent commands



**Example**



Verify `oc` client tools:

``` terminal
$ rosa verify oc
```

## Initializing Red Hat OpenShift Service on AWS

Use the `init` command to initialize Red Hat OpenShift Service on AWS (ROSA) only if you are using non-STS.

### init

Perform a series of checks to verify that you are ready to deploy an Red Hat OpenShift Service on AWS cluster.

The list of checks includes the following:

-   Checks to see that you have logged in (see `login`)

-   Checks that your AWS credentials are valid

-   Checks that your AWS permissions are valid (see `verify permissions`)

-   Checks that your AWS quota levels are high enough (see `verify quota`)

-   Runs a cluster simulation to ensure cluster creation will perform as expected

-   Checks that the `osdCcsAdmin` user has been created in your AWS account

-   Checks that the OpenShift Container Platform command-line tool is available on your system



**Syntax**



``` terminal
$ rosa init [arguments]
```

| Option          | Definition                                                                                                                                                                                                            |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --region        | The AWS region (string) in which to verify quota and permissions. This value overrides the `AWS_REGION` environment variable only when running the `init` command, but it does not change your AWS CLI configuration. |
| --delete        | Deletes the stack template that is applied to your AWS account during the `init` command.                                                                                                                             |
| --client-id     | The OpenID client identifier (string). Default: `cloud-services`                                                                                                                                                      |
| --client-secret | The OpenID client secret (string).                                                                                                                                                                                    |
| --insecure      | Enables insecure communication with the server. This disables verification of TLS certificates and host names.                                                                                                        |
| --scope         | The OpenID scope (string). If this option is used, it completely replaces the default scopes. This can be repeated multiple times to specify multiple scopes. Default: `openid`                                       |
| --token         | Accesses or refreshes the token (string).                                                                                                                                                                             |
| --token-url     | The OpenID token URL (string). Default: `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`                                                                                            |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Configure your AWS account to allow ROSA clusters:

``` terminal
$ rosa init
```

Configure a new AWS account using pre-existing OpenShift Cluster Manager credentials:

``` terminal
$ rosa init --token=$OFFLINE_ACCESS_TOKEN
```

## Using a Bash script

This is an example workflow of how to use a Bash script with the `rosa` CLI.



**Prerequisites**



Make sure that AWS credentials are available as one of the following options:

-   AWS profile

-   Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)

1.  Initialize `rosa` using an Red Hat OpenShift Cluster Manager offline token [from Red Hat](https://console.redhat.com/openshift/token/rosa):

    ``` terminal
    $ rosa init --token=<token>
    ```

2.  Create the Red Hat OpenShift Service on AWS (ROSA) cluster:

    ``` terminal
    $ rosa create cluster --cluster-name=<cluster_name>
    ```

3.  Add an identity provider (IDP):

    ``` terminal
    $ rosa create idp --cluster=<cluster_name> --type=<identity_provider> [arguments]
    ```

4.  Add a `dedicated-admin` user:

    ``` terminal
    $ rosa grant user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
    ```

# Managing objects with the rosa CLI

Managing objects with the `rosa` CLI, such as adding `dedicated-admin` users, managing clusters, and scheduling cluster upgrades.

## Common commands and arguments

These common commands and arguments are available for the `rosa` CLI.

### debug

Enables debug mode for the parent command.



**Example**



``` terminal
$ rosa create cluster --cluster=<cluster_name> --debug
```

### help

Displays general help information for the `rosa` CLI and a list of available commands. This option can also be used as an argument to display help information for a parent command, such as `version` or `create`.



**Examples**



Displays general help for the `rosa` CLI:

``` terminal
$ rosa --help
```

Displays general help for `version`:

``` terminal
$ rosa version --help
```

### interactive

Enables interactive mode.



**Example**



``` terminal
$ rosa create cluster --cluster=<cluster_name> --interactive
```

### profile

Specifies an AWS profile from your credential file.



**Example**



``` terminal
$ rosa create cluster --cluster=<cluster_name> --profile=myAWSprofile
```

### v level

Specifies the log level for V logs.



**Example**



``` terminal
$ rosa create cluster --cluster=<cluster_name> --v <level>
```

### version

Displays the `rosa` version.



**Example**



``` terminal
$ rosa version [arguments]
```

## Parent commands

The `rosa` CLI uses parent commands with child commands to manage objects. The parent commands are `create`, `edit`, `delete`, `list`, and `describe`. Not all parent commands can be used with all child commands. For more information, see the specific reference topics that describes the child commands.

### create

Creates an object or resource when paired with a child command.



**Example**



``` terminal
$ rosa create cluster --cluster-name=mycluster
```

### edit

Edits options for an object, such as making a cluster private.



**Example**



``` terminal
$ rosa edit cluster --cluster=mycluster --private
```

### delete

Deletes an object or resource when paired with a child command.



**Example**



``` terminal
$ rosa delete ingress --cluster=mycluster
```

### list

Lists clusters or resources for a specific cluster.



**Example**



``` terminal
$ rosa list users --cluster=mycluster
```

### describe

Shows the details for a cluster.



**Example**



``` terminal
$ rosa describe --cluster=mycluster
```

## Create objects

This section describes the `create` commands for clusters and resources.

### create account-roles

Create the needed account-wide role and policy resources for your cluster.



**Syntax**



``` terminal
$ rosa create account-roles [flags]
```

| Option                        | Definition                                                                                                                                                                                                           |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --debug                       | Enable debug mode.                                                                                                                                                                                                   |
| -i, --interactive             | Enable interactive mode.                                                                                                                                                                                             |
| -m, --mode string             | How to perform the operation. Valid options are: auto: Resource changes will be automatic applied using the current AWS account manual: Commands necessary to modify AWS resources will be output to be run manually |
| --path string                 | The ARN path for the account-wide roles and policies, including the Operator policies.                                                                                                                               |
| --permissions-boundary string | The ARN of the policy that is used to set the permissions boundary for the account roles.                                                                                                                            |
| --prefix string               | User-defined prefix for all generated AWS resources. The default is `ManagedOpenShift`.                                                                                                                              |
| --profile string              | Use a specific AWS profile from your credential file.                                                                                                                                                                |
| -y, --yes                     | Automatically answer yes to confirm operation.                                                                                                                                                                       |

Flags

### create admin

Create a cluster administrator with an automatically generated password that can log in to a cluster.



**Syntax**



``` terminal
$ rosa create admin --cluster=<cluster_name> | <cluster_id>
```

| Option    | Definition                                                                              |
|-----------|-----------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to add to the identity provider (IDP). |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Create a cluster administrator that can log in to a cluster named `mycluster`:

``` terminal
$ rosa create admin --cluster=mycluster
```

### create cluster

Create a new cluster.



**Syntax**



``` terminal
$ rosa create cluster --cluster=<cluster_name> | <cluster_id> [arguments]
```

<table>
<caption>Arguments</caption>
<colgroup>
<col style="width: 30%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Option</th>
<th style="text-align: left;">Definition</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>--cluster</p></td>
<td style="text-align: left;"><p>Required: The name or ID (string) of the cluster. When used with the <code>create cluster</code> command, this argument is used to generate a sub-domain for your cluster on <code>openshiftapps.com</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--compute-machine-type</p></td>
<td style="text-align: left;"><p>The instance type (string) for the compute nodes. Determines the amount of memory and vCPU that are allocated to each compute node.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--compute-nodes</p></td>
<td style="text-align: left;"><p>The number (integer) of worker nodes to provision per zone. Single-zone clusters require at least 2 nodes. Multi-zone clusters require at least 3 nodes. Default: <code>2</code> for single-az; <code>3</code> for multi-az</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--controlplane-iam-role string</p></td>
<td style="text-align: left;"><p>The Amazon Resource Name (ARN) of the IAM role that will be attached to control plane instances.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--disable-scp-checks</p></td>
<td style="text-align: left;"><p>Indicates whether cloud permission checks are disabled when attempting to install a cluster.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--dry-run</p></td>
<td style="text-align: left;"><p>Simulates creating the cluster.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--enable-autoscaling</p></td>
<td style="text-align: left;"><p>Enables autoscaling of compute nodes. By default, autoscaling is set to <code>2</code> nodes. To set non-default node limits, use this argument with the <code>--min-replicas</code> and <code>--max-replicas</code> arguments.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--host-prefix</p></td>
<td style="text-align: left;"><p>The subnet prefix length (integer) to assign to each individual node. For example, if host prefix is set to <code>23</code>, then each node is assigned a <code>/23</code> subnet out of the given CIDR.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--machine-cidr</p></td>
<td style="text-align: left;"><p>Block of IP addresses (ipNet) used by Red Hat OpenShift Service on AWS while installing the cluster. Example: <code>10.0.0.0/16</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--max-replicas</p></td>
<td style="text-align: left;"><p>Specifies the maximum number of compute nodes when enabling autoscaling. Default: <code>2</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--min-replicas</p></td>
<td style="text-align: left;"><p>Specifies the minimum number of compute nodes when enabling autoscaling. Default: <code>2</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--multi-az</p></td>
<td style="text-align: left;"><p>Deploys to multiple data centers.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--pod-cidr</p></td>
<td style="text-align: left;"><p>Block of IP addresses (ipNet) from which pod IP addresses are allocated. Example: <code>10.128.0.0/14</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--private</p></td>
<td style="text-align: left;"><p>Restricts primary API endpoint and application routes to direct, private connectivity.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--private-link</p></td>
<td style="text-align: left;"><p>Specifies to use AWS PrivateLink to provide private connectivity between VPCs and services. The <code>--subnet-ids</code> argument is required when using <code>--private-link</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--region</p></td>
<td style="text-align: left;"><p>The AWS region (string) where your worker pool will be located. This argument overrides the <code>AWS_REGION</code> environment variable.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--role-arn string</p></td>
<td style="text-align: left;"><p>The Amazon Resource Name (ARN) of the installer role that OpenShift Cluster Manager will assume to create the cluster.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--service-cidr</p></td>
<td style="text-align: left;"><p>Block of IP addresses (ipNet) for services. Example: <code>172.30.0.0/16</code></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--subnet-ids</p></td>
<td style="text-align: left;"><p>The subnet IDs (string) to use when installing the cluster. Subnet IDs must be in pairs with one private subnet ID and one public subnet ID per availability zone. Subnets are comma-delimited. Example: <code>--subnet-ids=subnet-1,subnet-2</code>. Leave the value empty for installer-provisioned subnet IDs.</p>
<p>When using <code>--private-link</code>, the <code>--subnet-ids</code> argument is required and only one private subnet is allowed per zone.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--support-role-arn string</p></td>
<td style="text-align: left;"><p>The Amazon Resource Name (ARN) of the role used by Red Hat Site Reliabilty Engineers (SREs) to enable access to the cluster account to provide support.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--version</p></td>
<td style="text-align: left;"><p>The version (string) of Red Hat OpenShift Service on AWS that will be used to install the cluster or cluster resources, including <code>account-role</code>. Example: <code>4.12</code></p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--worker-iam-role string</p></td>
<td style="text-align: left;"><p>The Amazon Resource Name (ARN) of the IAM role that will be attached to compute instances.</p></td>
</tr>
</tbody>
</table>

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Create a cluster named `mycluster`:

``` terminal
$ rosa create cluster --cluster=mycluster
```

Create a cluster with a specific AWS region:

``` terminal
$ rosa create cluster --cluster=mycluster --region=us-east-2
```

Create a cluster with autoscaling enabled on the default worker machine pool:

``` terminal
$ rosa create cluster --cluster=mycluster -region=us-east-1 --enable-autoscaling --min-replicas=2 --max-replicas=5
```

### create idp

Add an identity provider (IDP) to define how users log in to a cluster.



**Syntax**



``` terminal
$ rosa create idp --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option           | Definition                                                                                       |
|------------------|--------------------------------------------------------------------------------------------------|
| --cluster        | Required: The name or ID (string) of the cluster to which the IDP will be added.                 |
| --ca             | The path (string) to the PEM-encoded certificate file to use when making requests to the server. |
| --client-id      | The client ID (string) from the registered application.                                          |
| --client-secret  | The client secret (string) from the registered application.                                      |
| --mapping-method | Specifies how new identities (string) are mapped to users when they log in. Default: `claim`     |
| --name           | The name (string) for the identity provider.                                                     |
| --type           | The type (string) of identity provider. Options: `github`, `gitlab`, `google`, `ldap`, `openid`  |

Arguments

| Option          | Definition                                                                                                                                                          |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --hostname      | The optional domain (string) to use with a hosted instance of GitHub Enterprise.                                                                                    |
| --organizations | Specifies the organizations for login access. Only users that are members of at least one of the listed organizations (string) are allowed to log in.               |
| --teams         | Specifies the teams for login access. Only users that are members of at least one of the listed teams (string) are allowed to log in. The format is `<org>/<team>`. |

GitHub arguments

| Option     | Definition                                                                |
|------------|---------------------------------------------------------------------------|
| --host-url | The host URL (string) of a GitLab provider. Default: `https://gitlab.com` |

GitLab arguments

| Option          | Definition                                        |
|-----------------|---------------------------------------------------|
| --hosted-domain | Restricts users to a Google Apps domain (string). |

Google arguments

| Option                | Definition                                                                                            |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| --bind-dn             | The domain name (string) to bind with during the search phase.                                        |
| --bind-password       | The password (string) to bind with during the search phase.                                           |
| --email-attributes    | The list (string) of attributes whose values should be used as the email address.                     |
| --id-attributes       | The list (string) of attributes whose values should be used as the user ID. Default: `dn`             |
| --insecure            | Does not make TLS connections to the server.                                                          |
| --name-attributes     | The list (string) of attributes whose values should be used as the display name. Default: `cn`        |
| --url                 | An RFC 2255 URL (string) which specifies the LDAP search parameters to use.                           |
| --username-attributes | The list (string) of attributes whose values should be used as the preferred username. Default: `uid` |

LDAP arguments

| Option            | Definition                                                                                                                                         |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| --email-claims    | The list (string) of claims to use as the email address.                                                                                           |
| --extra-scopes    | The list (string) of scopes to request, in addition to the `openid` scope, during the authorization token request.                                 |
| --issuer-url      | The URL (string) that the OpenID provider asserts as the issuer identifier. It must use the HTTPS scheme with no URL query parameters or fragment. |
| --name-claims     | The list (string) of claims to use as the display name.                                                                                            |
| --username-claims | The list (string) of claims to use as the preferred username when provisioning a user.                                                             |

OpenID arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Add a GitHub identity provider to a cluster named `mycluster`:

``` terminal
$ rosa create idp --type=github --cluster=mycluster
```

Add an identity provider following interactive prompts:

``` terminal
$ rosa create idp --cluster=mycluster --interactive
```

### create ingress

Add an ingress endpoint to enable API access to the cluster.



**Syntax**



``` terminal
$ rosa create ingress --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option        | Definition                                                                                                                                                            |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --cluster     | Required: The name or ID (string) of the cluster to which the ingress will be added.                                                                                  |
| --label-match | The label match (string) for ingress. The format must be a comma-delimited list of key=value pairs. If no label is specified, all routes are exposed on both routers. |
| --private     | Restricts application route to direct, private connectivity.                                                                                                          |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Add an internal ingress to a cluster named `mycluster`:

``` terminal
$ rosa create ingress --private --cluster=mycluster
```

Add a public ingress to a cluster named `mycluster`:

``` terminal
$ rosa create ingress --cluster=mycluster
```

Add an ingress with a route selector label match:s

``` terminal
$ rosa create ingress --cluster=mycluster --label-match=foo=bar,bar=baz
```

### create machinepool

Add a machine pool to an existing cluster.



**Syntax**



``` terminal
$ rosa create machinepool --cluster=<cluster_name> | <cluster_id> --replicas=<number> --name=<machinepool_name> [arguments]
```

| Option               | Definition                                                                                                                                                                                                                                  |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --cluster            | Required: The name or ID (string) of the cluster to which the machine pool will be added.                                                                                                                                                   |
| --enable-autoscaling | Enable or disable autoscaling of compute nodes. To enable autoscaling, use this argument with the `--min-replicas` and `--max-replicas` arguments. To disable autoscaling, use `--enable-autoscaling=false` with the `--replicas` argument. |
| --instance-type      | The instance type (string) that should be used. Default: `m5.xlarge`                                                                                                                                                                        |
| --labels             | The labels (string) for the machine pool. The format must be a comma-delimited list of key=value pairs. This list overwrites any modifications made to node labels on an ongoing basis.                                                     |
| --max-replicas       | Specifies the maximum number of compute nodes when enabling autoscaling.                                                                                                                                                                    |
| --min-replicas       | Specifies the minimum number of compute nodes when enabling autoscaling.                                                                                                                                                                    |
| --name               | Required: The name (string) for the machine pool.                                                                                                                                                                                           |
| --replicas           | Required when autoscaling is not configured. The number (integer) of machines for this machine pool.                                                                                                                                        |
| --taints             | Taints for the machine pool. This string value should be formatted as a comma-separated list of `key=value:ScheduleType`. This list will overwrite any modifications made to Node taints on an ongoing basis.                               |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Interactively add a machine pool to a cluster named `mycluster`:

``` terminal
$ rosa create machinepool --cluster=mycluster --interactive
```

Add a machine pool that is named `mp-1` to a cluster with autoscaling enabled:

``` terminal
$ rosa create machinepool --cluster=mycluster --enable-autoscaling --min-replicas=2 --max-replicas=5 --name=mp-1
```

Add a machine pool that is named `mp-1` with 3 replicas of `m5.xlarge` to a cluster:

``` terminal
$ rosa create machinepool --cluster=mycluster --replicas=3 --instance-type=m5.xlarge --name=mp-1
```

Add a machine pool with labels to a cluster:

``` terminal
$ rosa create machinepool --cluster=mycluster --replicas=2 --instance-type=r5.2xlarge --labels=foo=bar,bar=baz --name=mp-1
```

### create ocm-role

Create the required ocm-role resources for your cluster.



**Syntax**



``` terminal
$ rosa create ocm-role [flags]
```

<table>
<caption>Flags</caption>
<colgroup>
<col style="width: 30%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Option</th>
<th style="text-align: left;">Definition</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>--admin</p></td>
<td style="text-align: left;"><p>Enable admin capabilities for the role.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--debug</p></td>
<td style="text-align: left;"><p>Enable debug mode.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>-i, --interactive</p></td>
<td style="text-align: left;"><p>Enable interactive mode.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>-m, --mode string</p></td>
<td style="text-align: left;"><p>How to perform the operation. Valid options are:</p>
<ul>
<li><p><code>auto</code>: Resource changes will be automatic applied using the current AWS account</p></li>
<li><p><code>manual</code>: Commands necessary to modify AWS resources will be output to be run manually</p></li>
</ul></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--path string</p></td>
<td style="text-align: left;"><p>The ARN path for the OCM role and policies.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--permissions-boundary string</p></td>
<td style="text-align: left;"><p>The ARN of the policy that is used to set the permissions boundary for the OCM role.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--prefix string</p></td>
<td style="text-align: left;"><p>User-defined prefix for all generated AWS resources. The default is <code>ManagedOpenShift</code>.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--profile string</p></td>
<td style="text-align: left;"><p>Use a specific AWS profile from your credential file.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>-y, --yes</p></td>
<td style="text-align: left;"><p>Automatically answer yes to confirm operation.</p></td>
</tr>
</tbody>
</table>

Flags

For more information about the OCM role created with the `rosa create ocm-role` command, see *Account-wide IAM role and policy reference*.

### create user-role

Create the required user-role resources for your cluster.



**Syntax**



``` terminal
$ rosa create user-role [flags]
```

<table>
<caption>Flags</caption>
<colgroup>
<col style="width: 30%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Option</th>
<th style="text-align: left;">Definition</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>--debug</p></td>
<td style="text-align: left;"><p>Enable debug mode.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>-i, --interactive</p></td>
<td style="text-align: left;"><p>Enable interactive mode.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>-m, --mode string</p></td>
<td style="text-align: left;"><p>How to perform the operation. Valid options are:</p>
<ul>
<li><p><code>auto</code>: Resource changes will be automatic applied using the current AWS account</p></li>
<li><p><code>manual</code>: Commands necessary to modify AWS resources will be output to be run manually</p></li>
</ul></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--path string</p></td>
<td style="text-align: left;"><p>The ARN path for the user role and policies.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--permissions-boundary string</p></td>
<td style="text-align: left;"><p>The ARN of the policy that is used to set the permissions boundary for the user role.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>--prefix string</p></td>
<td style="text-align: left;"><p>User-defined prefix for all generated AWS resources The default is <code>ManagedOpenShift</code>.</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>--profile string</p></td>
<td style="text-align: left;"><p>Use a specific AWS profile from your credential file.</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>-y, --yes</p></td>
<td style="text-align: left;"><p>Automatically answer yes to confirm operation.</p></td>
</tr>
</tbody>
</table>

Flags

For more information about the user role created with the `rosa create user-role` command, see *Understanding AWS account association*.

## Additional resources

-   See [Account-wide IAM role and policy reference](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/introduction_to_rosa/#rosa-sts-account-wide-roles-and-policies_rosa-sts-about-iam-resources) for a list of IAM roles needed for cluster creation.

-   See [Understanding AWS account association](https://access.redhat.com/documentation/en-us/red_hat_openshift_service_on_aws/4/html-single/installing_accessing_and_deleting_rosa_clusters/#rosa-sts-understanding-aws-account-association_rosa-sts-creating-a-cluster-with-customizations) for more information about the OCM role and user role.

## Edit objects

This section describes the `edit` commands for clusters and resources.

### edit cluster

Allows edits to an existing cluster.



**Syntax**



``` terminal
$ rosa edit cluster --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                        |
|-----------|-------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to edit.         |
| --private | Restricts a primary API endpoint to direct, private connectivity. |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Edit a cluster named `mycluster` to make it private.

``` terminal
$ rosa edit cluster --cluster=mycluster --private
```

Edit all cluster options interactively on a cluster named `mycluster`.

``` terminal
$ rosa edit cluster --cluster=mycluster --interactive
```

### edit ingress

Edits the additional non-default application router for a cluster.



**Syntax**



``` terminal
$ rosa edit ingress --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option        | Definition                                                                                                                                                            |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --cluster     | Required: The name or ID (string) of the cluster to which the ingress will be added.                                                                                  |
| --label-match | The label match (string) for ingress. The format must be a comma-delimited list of key=value pairs. If no label is specified, all routes are exposed on both routers. |
| --private     | Restricts the application route to direct, private connectivity.                                                                                                      |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Make an additional ingress with the ID `a1b2` as a private connection on a cluster named `mycluster`.

``` terminal
$ rosa edit ingress --private --cluster=mycluster a1b2
```

Update the router selectors for the additional ingress with the ID `a1b2` on a cluster named `mycluster`.

``` terminal
$ rosa edit ingress --label-match=foo=bar --cluster=mycluster a1b2
```

Update the default ingress using the sub-domain identifier `apps` on a cluster named `mycluster`.

``` terminal
$ rosa edit ingress --private=false --cluster=mycluster apps
```

### edit machinepool

Allows edits to the machine pool in a cluster.



**Syntax**



``` terminal
$ rosa edit machinepool --cluster=<cluster_name> | <cluster_id> <machinepool_ID> [arguments]
```

| Option               | Definition                                                                                                                                                                                                                                                                                                                                                                 |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --cluster            | Required: The name or ID (string) of the cluster to edit on which the additional machine pool will be edited.                                                                                                                                                                                                                                                              |
| --enable-autoscaling | Enable or disable autoscaling of compute nodes. To enable autoscaling, use this argument with the `--min-replicas` and `--max-replicas` arguments. To disable autoscaling, use `--enable-autoscaling=false` with the `--replicas` argument.                                                                                                                                |
| --labels             | The labels (string) for the machine pool. The format must be a comma-delimited list of key=value pairs. Editing this value only affects newly created nodes of the machine pool, which are created by increasing the node number, and does not affect the existing nodes. This list overwrites any modifications made to node labels on an ongoing basis.                  |
| --max-replicas       | Specifies the maximum number of compute nodes when enabling autoscaling.                                                                                                                                                                                                                                                                                                   |
| --min-replicas       | Specifies the minimum number of compute nodes when enabling autoscaling.                                                                                                                                                                                                                                                                                                   |
| --replicas           | Required when autoscaling is not configured. The number (integer) of machines for this machine pool.                                                                                                                                                                                                                                                                       |
| --taints             | Taints for the machine pool. This string value should be formatted as a comma-separated list of `key=value:ScheduleType`. Editing this value only affect newly created nodes of the machine pool, which are created by increasing the node number, and does not affect the existing nodes. This list overwrites any modifications made to Node taints on an ongoing basis. |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Set 4 replicas on a machine pool named `mp1` on a cluster named `mycluster`.

``` terminal
$ rosa edit machinepool --cluster=mycluster --replicas=4 --name=mp1
```

Enable autoscaling on a machine pool named `mp1` on a cluster named `mycluster`.

``` terminal
$ rosa edit machinepool --cluster-name=mycluster --enable-autoscaling --min-replicas=3 --max-replicas=5 --name=mp1
```

Disable autoscaling on a machine pool named `mp1` on a cluster named `mycluster`.

``` terminal
$ rosa edit machinepool --cluster-name=mycluster  --enable-autoscaling=false --replicas=3 --name=mp1
```

Modify the autoscaling range on a machine pool named `mp1` on a cluster named `mycluster`.

``` terminal
$ rosa edit machinepool --max-replicas=9 --cluster=mycluster --name=mp1
```

## Delete objects

This section describes the `delete` commands for clusters and resources.

### delete admin

Deletes a cluster administrator from a specified cluster.



**Syntax**



``` terminal
$ rosa delete admin --cluster=<cluster_name> | <cluster_id>
```

| Option    | Definition                                                                              |
|-----------|-----------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to add to the identity provider (IDP). |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Delete a cluster administrator from a cluster named `mycluster`.

``` terminal
$ rosa delete admin --cluster=mycluster
```

### delete cluster

Deletes a cluster.



**Syntax**



``` terminal
$ rosa delete cluster --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                  |
|-----------|-------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to delete. |
| --watch   | Watches the cluster uninstallation logs.                    |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |
| --yes         | Automatically answers `yes` to confirm the operation.         |

Optional arguments inherited from parent commands



**Examples**



Delete a cluster named `mycluster`.

``` terminal
$ rosa delete cluster --cluster=mycluster
```

### delete idp

Deletes a specific identity provider (IDP) from a cluster.



**Syntax**



``` terminal
$ rosa delete idp --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                           |
|-----------|--------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster from which the IDP will be deleted. |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |
| --yes         | Automatically answers `yes` to confirm the operation.         |

Optional arguments inherited from parent commands



**Example**



Delete an identity provider named `github` from a cluster named `mycluster`.

``` terminal
$ rosa delete idp github --cluster=mycluster
```

### delete ingress

Deletes a non-default application router (ingress) from a cluster.



**Syntax**



``` terminal
$ rosa delete ingress --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                               |
|-----------|------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster from which the ingress will be deleted. |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |
| --yes         | Automatically answers `yes` to confirm the operation.         |

Optional arguments inherited from parent commands



**Examples**



Delete an ingress with the ID `a1b2` from a cluster named `mycluster`.

``` terminal
$ rosa delete ingress --cluster=mycluster a1b2
```

Delete a secondary ingress with the subdomain name `apps2` from a cluster named `mycluster`.

``` terminal
$ rosa delete ingress --cluster=mycluster apps2
```

### delete machinepool

Deletes a machine pool from a cluster.



**Syntax**



``` terminal
$ rosa delete machinepool --cluster=<cluster_name> | <cluster_id> <machine_pool_id>
```

| Option    | Definition                                                                                   |
|-----------|----------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the machine pool will be deleted from. |

Arguments

| Option        | Definition                                                    |
|---------------|---------------------------------------------------------------|
| --help        | Shows help for this command.                                  |
| --debug       | Enables debug mode.                                           |
| --interactive | Enables interactive mode.                                     |
| --profile     | Specifies an AWS profile (string) from your credentials file. |
| --v \<level>  | The log level for V logs.                                     |
| --yes         | Automatically answers `yes` to confirm the operation.         |

Optional arguments inherited from parent commands



**Example**



Delete the machine pool with the ID `mp-1` from a cluster named `mycluster`.

``` terminal
$ rosa delete machinepool --cluster=mycluster mp-1
```

## Install and uninstall add-ons

This section describes how to install and uninstall Red Hat managed service add-ons to a cluster.

### install addon

Installs a managed service add-on on a cluster.



**Syntax**



``` terminal
$ rosa install addon --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                           |
|-----------|--------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster where the add-on will be installed. |

Arguments

| Option    | Definition                                                       |
|-----------|------------------------------------------------------------------|
| --help    | Shows help for this command.                                     |
| --debug   | Enables debug mode.                                              |
| --profile | Uses a specific AWS profile (string) from your credentials file. |
| --v level | Log level for V logs.                                            |
| --yes     | Automatically answers `yes` to confirm the operation.            |

Optional arguments inherited from parent commands



**Example**



Add the `codeready-workspaces` add-on installation to a cluster named `mycluster`.

``` terminal
$ rosa install addon --cluster=mycluster codeready-workspaces
```



After installing Red Hat CodeReady Workspace, it can be deployed to any namespace except `openshift-workspaces`. For more information, see [Installing the Red Hat CodeReady Workspaces Operator](https://access.redhat.com/documentation/en-us/red_hat_codeready_workspaces/2.10/html/installation_guide/installing-codeready-workspaces_crw#creating-a-project-in-openshift-web-console_crw).



### uninstall addon

Uninstalls a managed service add-on from a cluster.



**Syntax**



``` terminal
$ rosa uninstall addon --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                                 |
|-----------|--------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the add-on will be uninstalled from. |

Arguments

| Option    | Definition                                                       |
|-----------|------------------------------------------------------------------|
| --help    | Shows help for this command.                                     |
| --debug   | Enables debug mode.                                              |
| --profile | Uses a specific AWS profile (string) from your credentials file. |
| --v level | Log level for V logs.                                            |
| --yes     | Automatically answers `yes` to confirm the operation.            |

Optional arguments inherited from parent commands



**Example**



Remove the `codeready-workspaces` add-on installation from a cluster named `mycluster`.

``` terminal
$ rosa uninstall addon --cluster=mycluster codeready-workspaces
```

## List and describe objects

This section describes the `list` and `describe` commands for clusters and resources.

### list addon

List the managed service add-on installations.



**Syntax**



``` terminal
$ rosa list addons --cluster=<cluster_name> | <cluster_id>
```

| Option    | Definition                                                                |
|-----------|---------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to list the add-ons for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands

### list clusters

List all of your clusters.



**Syntax**



``` terminal
$ rosa list clusters [arguments]
```

| Option  | Definition                                                  |
|---------|-------------------------------------------------------------|
| --count | The number (integer) of clusters to display. Default: `100` |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands

### list idps

List all of the identity providers (IDPs) for a cluster.



**Syntax**



``` terminal
$ rosa list idps --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                         |
|-----------|------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the IDPs will be listed for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all identity providers (IDPs) for a cluster named `mycluster`:

``` terminal
$ rosa list idps --cluster=mycluster
```

### list ingresses

List all of the API and ingress endpoints for a cluster.



**Syntax**



``` terminal
$ rosa list ingresses --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                         |
|-----------|------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the IDPs will be listed for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all API and ingress endpoints for a cluster named `mycluster`:

``` terminal
$ rosa list ingresses --cluster=mycluster
```

### list instance-types

List all of the available instance types for use with Red Hat OpenShift Service on AWS. Availability is based on the account’s AWS quota.



**Syntax**



``` terminal
$ rosa list instance-types [arguments]
```

| Option    | Definition                                                    |
|-----------|---------------------------------------------------------------|
| --help    | Shows help for this command.                                  |
| --debug   | Enables debug mode.                                           |
| --output  | The output format. Allowed formats are `json` or `yaml`.      |
| --profile | Specifies an AWS profile (string) from your credentials file. |

Optional arguments inherited from parent commands



**Example**



List all instance types:

``` terminal
$ rosa list instance-types
```

### list machinepools

List the machine pools configured on a cluster.



**Syntax**



``` terminal
$ rosa list machinepools --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                                  |
|-----------|---------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the machine pools will be listed for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all of the machine pools on a cluster named `mycluster`:

``` terminal
$ rosa list machinepools --cluster=mycluster
```

### list regions

List all of the available regions for the current AWS account.



**Syntax**



``` terminal
$ rosa list regions [arguments]
```

| Option     | Definition                                                          |
|------------|---------------------------------------------------------------------|
| --multi-az | Lists regions that provide support for multiple availability zones. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all of the available regions:

``` terminal
$ rosa list regions
```

### list upgrades

List all available and scheduled cluster version upgrades.



**Syntax**



``` terminal
$ rosa list upgrades --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                                       |
|-----------|--------------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the available upgrades will be listed for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all of the available upgrades for a cluster named `mycluster`:

``` terminal
$ rosa list upgrades --cluster=mycluster
```

### list users

List the cluster administrator and dedicated administrator users for a specified cluster.



**Syntax**



``` terminal
$ rosa list users --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                                           |
|-----------|------------------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the cluster administrators will be listed for. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all of the cluster administrators and dedicated administrators for a cluster named `mycluster`:

``` terminal
$ rosa list users --cluster=mycluster
```

### list versions

List all of the OpenShift versions that are available for creating a cluster.



**Syntax**



``` terminal
$ rosa list versions [arguments]
```

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



List all of the OpenShift Container Platform versions:

``` terminal
$ rosa list versions
```

### describe admin

Show the details of a specified `cluster-admin` user and a command to log in to the cluster.



**Syntax**



``` terminal
$ rosa describe admin --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                           |
|-----------|--------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to which the cluster-admin belongs. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Describe the `cluster-admin` user for a cluster named `mycluster`:

``` terminal
$ rosa describe admin --cluster=mycluster
```

### describe addon

Show the details of a managed service add-on.



**Syntax**



``` terminal
$ rosa describe addon <addon_id> | <addon_name> [arguments]
```

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Describe an add-on named `codeready-workspaces`:

``` terminal
$ rosa describe addon codeready-workspaces
```

### describe cluster

Shows the details for a cluster.



**Syntax**



``` terminal
$ rosa describe cluster --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                        |
|-----------|---------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster. |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Describe a cluster named `mycluster`:

``` terminal
$ rosa describe cluster --cluster=mycluster
```

## Upgrade and delete upgrade for clusters

This section describes the `upgrade` command usage for clusters.

### upgrade cluster

Schedule a cluster upgrade.



**Syntax**



``` terminal
$ rosa upgrade cluster --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option                    | Definition                                                                                                                                                                                                                                                                                        |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --cluster                 | Required: The name or ID (string) of the cluster that the upgrade will be scheduled for.                                                                                                                                                                                                          |
| --interactive             | Enables interactive mode.                                                                                                                                                                                                                                                                         |
| --version                 | The version (string) of OpenShift Container Platform that the cluster will be upgraded to.                                                                                                                                                                                                        |
| --schedule-date           | The next date (string) when the upgrade will run at the specified time. Format: `yyyy-mm-dd`                                                                                                                                                                                                      |
| --schedule-time           | The next time the upgrade will run on the specified date. Format: `HH:mm`                                                                                                                                                                                                                         |
| --node-drain-grace-period | Sets a grace period (string) for how long the pod disruption budget-protected workloads are respected during upgrades. After this grace period, any workloads protected by pod disruption budgets that have not been successfully drained from a node will be forcibly evicted. Default: `1 hour` |

Arguments

| Option | Definition                   |
|--------|------------------------------|
| --help | Shows help for this command. |

Optional arguments inherited from parent commands



**Examples**



Interactively schedule an upgrade on a cluster named `mycluster`:

``` terminal
$ rosa upgrade cluster --cluster=mycluster --interactive
```

Schedule a cluster upgrade within the hour on a cluster named `mycluster`:

``` terminal
$ rosa upgrade cluster --cluster=mycluster --version 4.5.20
```

### delete upgrade

Cancel a scheduled cluster upgrade:



**Syntax**



``` terminal
$ rosa delete upgrade --cluster=<cluster_name> | <cluster_id>
```

| Option    | Definition                                                                               |
|-----------|------------------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster that the upgrade will be cancelled for. |

Arguments

| Option    | Definition                                            |
|-----------|-------------------------------------------------------|
| --help    | Shows help for this command.                          |
| --debug   | Enables debug mode.                                   |
| --v level | Log level for V logs.                                 |
| --yes     | Automatically answers `yes` to confirm the operation. |

Optional arguments inherited from parent commands

# Checking account and version information with the rosa cli

## Checking account and version information with the rosa CLI

Use the following commands to check your account and version information.

### whoami

Display information about your AWS and Red Hat accounts.



**Syntax**



``` terminal
$ rosa whoami [arguments]
```

| Option    | Definition                                                    |
|-----------|---------------------------------------------------------------|
| --help    | Shows help for this command.                                  |
| --debug   | Enables debug mode.                                           |
| --profile | Specifies an AWS profile (string) from your credentials file. |
| --v level | Log level for V logs.                                         |

Optional arguments inherited from parent commands



**Example**



``` terminal
$ rosa whoami
```

### version

Display the version of your `rosa` CLI.



**Syntax**



``` terminal
$ rosa version [arguments]
```

| Option    | Definition                                                    |
|-----------|---------------------------------------------------------------|
| --help    | Shows help for this command.                                  |
| --debug   | Enables debug mode.                                           |
| --profile | Specifies an AWS profile (string) from your credentials file. |
| --v level | Log level for V logs.                                         |

Optional arguments inherited from parent commands



**Example**



``` terminal
$ rosa version
```

# Checking logs with the rosa CLI

## Checking logs with the rosa CLI

Use the following commands to check your install and uninstall logs.

### logs install

Show the cluster install logs.



**Syntax**



``` terminal
$ rosa logs install --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                    |
|-----------|-------------------------------------------------------------------------------|
| --cluster | Required: The name or ID (string) of the cluster to get logs for.             |
| --tail    | The number (integer) of lines to get from the end of the log. Default: `2000` |
| --watch   | Watches for changes after getting the logs.                                   |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Examples**



Show the last 100 install log lines for a cluster named `mycluster`:

``` terminal
$ rosa logs install mycluster --tail=100
```

Show the install logs for a cluster named `mycluster`:

``` terminal
$ rosa logs install --cluster=mycluster
```

### logs uninstall

Show the cluster uninstall logs.



**Syntax**



``` terminal
$ rosa logs uninstall --cluster=<cluster_name> | <cluster_id> [arguments]
```

| Option    | Definition                                                                    |
|-----------|-------------------------------------------------------------------------------|
| --cluster | The name or ID (string) of the cluster to get logs for.                       |
| --tail    | The number (integer) of lines to get from the end of the log. Default: `2000` |
| --watch   | Watches for changes after getting the logs.                                   |

Arguments

| Option       | Definition                                                    |
|--------------|---------------------------------------------------------------|
| --help       | Shows help for this command.                                  |
| --debug      | Enables debug mode.                                           |
| --profile    | Specifies an AWS profile (string) from your credentials file. |
| --v \<level> | The log level for V logs.                                     |

Optional arguments inherited from parent commands



**Example**



Show the last 100 uninstall logs for a cluster named `mycluster`:

``` terminal
$ rosa logs uninstall --cluster=mycluster --tail=100
```

# Backing up applications

You can employ OpenShift API for Data Protection (OADP) with Red Hat OpenShift Service on AWS (ROSA) clusters to backup and restore application data. A ROSA deployment of OpenShift is configured specifically for AWS services.

## Installing OADP on Red Hat OpenShift Service on AWS with AWS STS

AWS Security Token Service (AWS STS) is a global web service that provides short-term credentials for IAM or federated users. Red Hat OpenShift Service on AWS (ROSA) with STS is the recommended credential mode for ROSA clusters. This document describes how to install OpenShift API for Data Protection (OADP) on (ROSA) with AWS STS.



Restic is not supported in the OADP on ROSA with AWS STS environment. Ensure the Restic service is disabled. Use native snapshots to backup volumes. See *Known Issues* for more information.



-   A ROSA OpenShift Cluster with the required access and tokens.

-   [A default Secret](https://docs.openshift.com/container-platform/4.12/backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.html#oadp-creating-default-secret_installing-oadp-aws), if your backup and snapshot locations use the same credentials, or if you do not require a snapshot location.

1.  Create an Openshift secret from your AWS token file by entering the following commands:

    1.  Create the credentials file:

        ``` terminal
        $ cat <<EOF > ${SCRATCH}/credentials
        [default]
        role_arn = ${ROLE_ARN}
        web_identity_token_file = /var/run/secrets/openshift/serviceaccount/token
        EOF
        ```

    2.  Create the OpenShift secret:

        ``` terminal
        $ oc -n openshift-adp create secret generic cloud-credentials \
          --from-file=${SCRATCH}/credentials
        ```

2.  Install the OADP Operator.

    1.  In the Red Hat OpenShift Service on AWS web console, navigate to Operators **→** OperatorHub.

    2.  Search for the OADP Operator, then click **Install**.

3.  Create AWS cloud storage using your AWS credentials:

    ``` terminal
    $ cat << EOF | oc create -f -
    apiVersion: oadp.openshift.io/v1alpha1
    kind: CloudStorage
    metadata:
      name: ${CLUSTER_NAME}-oadp
      namespace: openshift-adp
    spec:
      creationSecret:
        key: credentials
        name: cloud-credentials
      enableSharedConfig: true
      name: ${CLUSTER_NAME}-oadp
      provider: aws
      region: $REGION
    EOF
    ```

4.  Create the `DataProtectionApplication resource`, which is used to configure the connection to the storage where the backups and volume snapshots will be stored:

    ``` terminal
    $ cat << EOF | oc create -f -
    apiVersion: oadp.openshift.io/v1alpha1
    kind: DataProtectionApplication
    metadata:
      name: ${CLUSTER_NAME}-dpa
      namespace: openshift-adp
    spec:
      backupLocations:
      - bucket:
          cloudStorageRef:
            name: ${CLUSTER_NAME}-oadp
          credential:
            key: credentials
            name: cloud-credentials
          default: true
      configuration:
        velero:
          defaultPlugins:
          - openshift
          - aws
          restic:
            enable: false
      volumeSnapshots:
      - velero:
          config:
            credentialsFile: /tmp/credentials/openshift-adp/cloud-credentials-credentials
            enableSharedConfig: "true"
            region: ${REGION}
          provider: aws
    EOF
    ```

    

    The `enable` parameter of `restic` is set to `false` in this configuration because OADP does not support Restic in ROSA environments.

    

    You are now ready to backup and restore OpenShift applications, as described in the [OADP documentation](https://docs.openshift.com/container-platform/4.11/backup_and_restore/application_backup_and_restore/backing_up_and_restoring/backing-up-applications.html).

### Known Issues

-   [CloudStorage: openshift-adp-controller-manager crashloop seg fault with Restic enabled](https://issues.redhat.com/browse/OADP-1054)

-   [Cloudstorage API: CSI Backup of an app with internal images partially fails with plugin panicked error](https://issues.redhat.com/browse/OADP-1057)

-   (Affects OADP 1.1.x\_ only): [CloudStorage: bucket is removed on CS CR delete, although it doesn’t have "oadp.openshift.io/cloudstorage-delete": "true"](https://issues.redhat.com/browse/OADP-1055)

<!-- -->

-   [Understanding ROSA with STS](https://docs.openshift.com/rosa/rosa_architecture/rosa-understanding.html)

-   [Getting started with ROSA STS](https://docs.openshift.com/rosa/rosa_getting_started/rosa-sts-getting-started-workflow.html)

-   [Creating a ROSA cluster with STS](https://docs.openshift.com/rosa/rosa_install_access_delete_clusters/rosa-sts-creating-a-cluster-quickly.html)

-   [About installing OADP](https://docs.openshift.com/container-platform/4.12/backup_and_restore/application_backup_and_restore/installing/about-installing-oadp.html)

-   [Configuring CSI volumes](https://docs.openshift.com/container-platform/4.12/storage/container_storage_interface/persistent-storage-csi.html)

-   [ROSA storage options](https://docs.openshift.com/rosa/rosa_architecture/rosa_policy_service_definition/rosa-service-definition.html#rosa-sdpolicy-storage_rosa-service-definition)

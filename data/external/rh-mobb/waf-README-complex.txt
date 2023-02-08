This is a POC of ROSA with a AWS WAF service

  Non working (yet) instructions for using STS to manage the creds for ALB

See https://issues.redhat.com/browse/CTONET-858 for a similar request

Here’s a good overview of AWS LB types and what they support

Problem Statement

1.  Customer requires WAF (Web Application Firewall) in front of their workloads running on OpenShift (ROSA)

2.  Customer does not want WAF running on OpenShift to ensure that OCP resources do not experience Denial of Service through handling the WAF

Proposed Solution

  Loosely based off EKS instructions here - https://aws.amazon.com/premiumsupport/knowledge-center/eks-alb-ingress-aws-waf/

1.  Deploy secondary Ingress solution (+TLS +DNS) that uses an AWS ALB

2.  Configure TLS + DNS for that Ingress

    1.  Lets Encrypt + WildCard DNS

Deployment

AWS Load Balancer Controller

AWS Load Balancer controller manages the following AWS resources

Application Load Balancers to satisfy Kubernetes ingress objects Network Load Balancers in IP mode to satisfy Kubernetes service objects of type LoadBalancer with NLB IP mode annotation

Configure STS

1.  Make sure your cluster has the pod identity webhook

        kubectl get mutatingwebhookconfigurations.admissionregistration.k8s.io pod-identity-webhook

2.  Create AWS Policy and Service Account

        POLICY_ARN=$(aws iam create-policy --policy-name "AWSLoadBalancerControllerIAMPolicy" --policy-document file://iam-policy.json --query Policy.Arn --output text)
        echo $POLICY_ARN

3.  Create service account

      Note I had issues with the policy, and for now just gave this user admin creds. Need to revisit and figure out.

        SA_ARN=$(aws iam create-user --user-name aws-lb-controller --permissions-boundary=$POLICY_ARN --query User.Arn --output text)

4.  Create access key

        ACCESS_KEY=$(aws iam create-access-key --user-name aws-lb-controller)

5.  Attach policy to user

    ```bash

6.  Paste the AccessKeyId and SecretAccessKey into values.yaml

7.  tag your public subnet with ``

8.  Create a namespace for the controller

        kubectl create ns aws-load-balancer-controller

    <!–

9.  Create a service account for the controller

        cat << EOF | kubectl apply -f -
        apiVersion: v1
        kind: ServiceAccount
        metadata:
         annotations:
        sts.amazonaws.com/role-arn: "${IAM_ARN}"
        eks.amazonaws.com/role-arn: "${IAM_ARN}"
        eks.amazonaws.com/audience: sts.amazonaws.com
         name: aws-load-balancer-controller
         namespace: aws-load-balancer-controller
        EOF

    –>

10. Apply CRDs

        kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

11. Add the helm repo and install the controller (install helm3 if not already)

        helm repo add eks https://aws.github.io/eks-charts
        helm install -n aws-load-balancer-controller \
          aws-load-balancer-controller eks/aws-load-balancer-controller \
          --values=./helm/values.yaml --create-namespace

Deploy Sample Application

    oc new-project demo
    oc new-app https://github.com/sclorg/django-ex.git
    kubectl -n demo patch service django-ex -p '{"spec":{"type":"NodePort"}}'

    kubectl apply -f ingress.yaml

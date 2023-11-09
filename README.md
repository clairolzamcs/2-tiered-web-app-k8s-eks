# 2-tiered-web-app-k8s-eks
Deployment of 2-tiered web application to managed K8s cluster on Amazon EKS, with pod auto-scaling and deployment automation.

# Implementation
1.	In cloud9:
    a.	alias tf=terraform
    b.	alias k=kubectl
    c.	alias kgp=”kubectl get pods”
2.	Change value in ~/.aws/credentials
3.	Prepared application files
4.	Build and push docker images for both db and app
    a.	To login to docker:
        i.	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 009147451403.dkr.ecr.us-east-1.amazonaws.com
    b.	In the directory where the db dockerfile is: 
        i.	docker build -t 009147451403.dkr.ecr.us-east-1.amazonaws.com/prod-db:test .
        ii.	docker push 009147451403.dkr.ecr.us-east-1.amazonaws.com/prod-db:test 
    c.	In the directory where the app dockerfile is: 
        i.	docker build -t 009147451403.dkr.ecr.us-east-1.amazonaws.com/prod-app:test .
        ii.	docker push 009147451403.dkr.ecr.us-east-1.amazonaws.com/prod-app:test 
5.	Prepared manifests
6.	In the terraform directory, apply terraform to:
        a.	Create ECR
        b.	Create S3 bucket
7.	Manually upload images in the format bg1.jpg, bg2.jpg, etc.
8.	Set S3 bucket to become publicly accessible. Edit block public access and edit the bucket permissions. Add below:
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::group8-website-assets/*"
                }
            ]
        }
9.	Create EKS cluster
        a.	eksctl create cluster -f eks_config.yaml
        b.	Once cluster is created, enable EBS CSI addon in AWS console
10.	Create the final namespace
        a.	k create ns final
11.	Applied db manifests in the following order:
        a.	Secret
        b.	PVC
        c.	Deployment
        d.	Service
12.	Applied app manifests in the following order:
        a.	Service account
        b.	Cluster role
        c.	Cluster role binding
        d.	Configmap
        e.	Deployment
        f.	Service
13.	Test by accessing the load balancer DNS + “:81” in the browser

# Problems:
1.	Got an error after applying db deployment manifest:
        a.	Issue: Error from server (BadRequest): container "db-deployment" in pod "db-deployment-5568f56664-g52vw" is waiting to start: CreateContainerConfigError
        b.	Solution: I forgot to apply the secret first. After creating the secret, pods became running
2.	Got an error after applying app deployment manifest:
        a.	Issue: Error from server (BadRequest): container "app-deployment" in pod "app-deployment-cddbd47dd-9xgvl" is waiting to start: PodInitializing
            i.	Status is Init:CrashLoopBackOff
            ii.	Went inside the container to check logs: `kubectl logs <pod-name> -c download-image` where i found the error:
fatal error: An error occurred (InvalidIdentityToken) when calling the AssumeRoleWithWebIdentity operation: No OpenIDConnect provider found in your account for https://oidc.eks.us-east-1.amazonaws.com/id/7347C60B0C6EFE32110FBA17B4A737D7
        b.	Solution: 
            i.	I went inside the container to look at the init container logs where i found:
            fatal error: An error occurred (InvalidIdentityToken) when calling the AssumeRoleWithWebIdentity operation: No OpenIDConnect provider found in your account for https://oidc.eks.us-east-1.amazonaws.com/id/7347C60B0C6EFE32110FBA17B4A737D7
            ii.	Followed steps here: https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
            Via eksctl: Error: creating OIDC provider: operation error IAM: CreateOpenIDConnectProvider, https response error StatusCode: 403, RequestID: 4a1082c6-649d-4db0-8f5a-956e042f9fec, api error AccessDenied: User: arn:aws:sts::009147451403:assumed-role/voclabs/user1865679=clairolzamsalazar@gmail.com is not authorized to perform: iam:CreateOpenIDConnectProvider on resource: arn:aws:iam::009147451403:oidc-provider/oidc.eks.us-east-1.amazonaws.com because no identity-based policy allows the iam:CreateOpenIDConnectProvider action
            
   Via AWS console:
             ![image](https://github.com/clairolzamcs/2-tiered-web-app-k8s-eks/assets/84026627/8736c33c-899e-4192-97d6-e5700809e37c)

 

    iii.	Since I was prohibited to do this, I cannot use a service account. Therefore, I have decided to just expose my S3 publicly so that I won’t need OIDC.
    iv.	It worked flawlessly and the init container was able to download the image from S3 bucket and place it in the target destination.
3.	Cannot access
        a.	Solution: add all in security group
4.	Image is not being loaded in the application. 
        a.	Issue: GET /tmp/background.jpg HTTP/1.1" 404
        b.	Solution: Flask has a different way to get the file so I had to insert 	`static_url_path='/static’` in the app.py and in the html templates, used `url_for`.


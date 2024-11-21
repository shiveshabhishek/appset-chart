PURPOSE:  
This chart creates an argocd applicationset that uses rolling sync ( aka progressive sync ) to deploy in user defined stages to user defined environments

prerequisites:  
see https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/Progressive-Syncs/  

steps:    
 1. Use example-values.yaml as a starting point and copy it to another file, do not change the example-values.yaml file  
 2. edit the copy file with your own values  
 3. commit and push the changes  
 4. copy the parent-app-template.yaml to another file, edit the name and the add the values file you created in previous step    
   
 5.   run  
kubectl -n argocd apply -f parent-app-<copied>-file.yaml 


USE CASES:    
 dimensions:   
   source types: plain yamls in git, helm in git, helm in nongit, kustomize in git (will be ready later)  
   source numbers: single source now, multiple sources ( will be ready later)  
   number of environments: 2 ( dev and prod) ,3 ( dev qa and prod) ,4 ( dev qa uat and prod ),5 etc  
   number of clusters:  1 (different namespaces), same as number of environments, and everywhere in between  
   number of stages: equal to number of environments, less than number of environments ( example people might want to deploy to qa and uat at the same time, after deploying to dev, but before deploying to prod )  
   promotion types: manual approval, automated approval
   promotion technology: kubernetes jobs, argo events, argo workflows, git PRs, jira tickets

  
 ma-manual approval    
 wf-argo workflow used for manual approval  
 job-k8s jpn used for manual approval  
 pr- k8sjob checks if pr is merged for manual approval  

 py-plain yaml  
 en-environments  
 cl-clusters  
 sg-stages  
 hg- helm in git  
  
[various possible stage of deployments to environments to clusters, namespaces ](Deployment-Stages-to-environments.pdf)  
   
tested the following
  
py-en2-cl1-sg2-values.yaml  (plain yaml, environments 2, clusters 1, stages 2)  
py-en3-cl1-sg3-values.yaml  (plain yaml, environments 3, clusters 1, stages 3)  
py-en3-cl3-sg3-values.yaml  (plain yaml, environments 3, clusters 3, stages 3)  
py-en4-cl4-sg3-values.yaml  (plain yaml, environments 4, clusters 4, stages 3)  
py-en5-cl5-sg3-values.yaml  (plain yaml, environments 5, clusters 5, stages 3)  
  
testhelm-appset-values.yaml (helm in git, environments 3, clusters 1, stages 3)    
hg-en5-cl3-sg4-values.yaml (helm in git, environments 5, clusters 3, stages 4)    
there were issues when the rollingsync application label match was changed, stage three and four failed to sync, fixed when parent application and applicationset were deleted and recreated  

ma-wf-py-en2-cl1-sg3-values.yaml (manual approval with argo workflow, plain yaml, environments 2, clusters 1, stages 3) 
   
ma-job-py-en2-cl1-sg3-values.yaml (manual approval with k8s job, plain yaml, environments 2, clusters 1, stages 3)   
  
  
ma-pr-py-en2-cl1-sg3-values.yaml (manual approval with k8s job that checks if pr is merged, plain yaml, environments 2, clusters 1, stages 3)
     
to be done  
     
hng- helm not in git      
ae - argo events    
jt - jira tickets  
  
kz - Kustomize  
msc - multi source  

HOW TO USE THE UI ?

step 1. in a browser open the url https://appset-ui.devops.opsmx.org/ , use opsmxuser opsmxadmin123456 
step 2. fill up the form using one of the examples in the base folder, just change the name , a file with the <name>-values.yaml will be committed to this repo, in branch moreadv   
step 3. login to https://argocd.jpmc.opsmx.net/ and check to see if the application parent-<name> is created, under which appset with name <name> is created  
step 4. check to see if the child apps are created and are progressively synced  




Problem Statement: Classify the tag based on the inputs provided.

> > Source: **S3-bucket**<br>
> Source Filetype: **XML**

# Workflow 
![img.png](venv/img.png)

*[Workflow created on Whimsical](www.whimsical.com)

## Steps
1. Create Repository using boilerplate template
2. Create environment
3. Pipeline Steps
>+ Data Fetching
>+ Data Preparation
>+ Feature Creation
>+ Model Training
>+ Model Evaluation
4. [CI/CD pipeline setup](studio.iterative.ai)
>+ Add a view 
>+ configure git settings on iterative.ai
>+ Link project
5. Start Experimenting:
>+ Change params.yaml configs 
>+ run dvc repro -f 
>+ git add . && git commit -m "experiment ##"
>+ git push
>+ check in iterative.ai for new commit id and scores



DVC Commands Used:
```commandline
dvc init
dvc repro
dvc repro -f << to run complete pipeline from start
dvc dag
```

Git Commands Used:
```commandline
git init
git status
git checkout -b branchname
git clone repo_link
git pull 
git push
```

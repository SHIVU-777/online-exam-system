# Online Exam System (24MIS0004)

Three versions of one Flask app, each built by its own Jenkins pipeline, containerized, pushed to DockerHub and deployed to Kubernetes.

| Version | Feature | Port |
|---|---|---|
| v1 | MCQ Quiz – conduct a simple test | http://localhost:8081 |
| v2 | Auto Score – marks calculated automatically | http://localhost:8082 |
| v3 | Result – final score, percentage, grade, pass/fail, answer review | http://localhost:8083 |

## Structure
```
online-exam/
  v1/ app.py  requirements.txt  Dockerfile  Jenkinsfile  test_app.py
  v2/ ...
  v3/ ...
  k8s/ v1.yaml  v2.yaml  v3.yaml
```

## Prerequisites
VS Code, Python 3.12, Git, Docker Desktop with **Kubernetes enabled**, Jenkins (with Git, Pipeline and Credentials plugins), GitHub and DockerHub accounts.

## Step 1 – Open in VS Code and run locally
```
cd online-exam
code .
cd v1
pip install -r requirements.txt pytest
python -m pytest -q
python app.py        # http://localhost:5000
```
Repeat for v2 and v3.

## Step 2 – Push to GitHub (separate branches + commits)
Create an empty repo `online-exam-system` on GitHub, then:
```
git init
git branch -M main
git remote add origin https://github.com/SHIVU-777/online-exam-system.git

# v1
git checkout -b v1
git add v1 k8s .gitignore README.md
git commit -m "v1: MCQ quiz"
git push -u origin v1

# v2
git checkout -b v2
git add v2
git commit -m "v2: auto score"
git push -u origin v2

# v3
git checkout -b v3
git add v3
git commit -m "v3: result page"
git push -u origin v3

git checkout main && git merge v3 && git push -u origin main
```
(Each branch needs its Jenkinsfile and k8s files; v2 and v3 branch from the previous one so they inherit them.)

## Step 3 – Jenkins credentials
Manage Jenkins → Credentials → Global → Add → *Username with password*: DockerHub username/password (or access token), **ID = `dockerhub-creds`**.
Jenkins machine must have `python`, `docker` and `kubectl` on PATH, and Jenkins' user must be able to run docker.

## Step 4 – Create three Jenkins pipelines
For each of v1, v2, v3: New Item → Pipeline → *Pipeline script from SCM* → Git:
- Repository: `https://github.com/SHIVU-777/online-exam-system.git`
- Branch: `*/v1` (then `*/v2`, `*/v3`)
- Script Path: `v1/Jenkinsfile` (then `v2/Jenkinsfile`, `v3/Jenkinsfile`)

Click **Build Now**. Each pipeline runs: Checkout → Test → Docker Build (tag `v1`/`v2`/`v3`) → Push to DockerHub → Deploy to Kubernetes.
(If Jenkins runs on Linux, replace `bat` with `sh` and `%VAR%` with `$VAR` in the Jenkinsfiles.)

## Step 5 – Manual Docker commands (alternative / verification)
```
cd v1
docker build -t shivanesh77/online-exam:v1 .
docker login
docker push shivanesh77/online-exam:v1
```
Same for v2 and v3. Check at https://hub.docker.com/r/shivanesh77/online-exam/tags

## Step 6 – Deploy to Kubernetes (3 deployments / 3 services)
```
kubectl apply -f k8s/v1.yaml
kubectl apply -f k8s/v2.yaml
kubectl apply -f k8s/v3.yaml
kubectl get deployments
kubectl get svc
```
With Docker Desktop Kubernetes the LoadBalancer services bind to localhost:
- http://localhost:8081 (v1)
- http://localhost:8082 (v2)
- http://localhost:8083 (v3)

**If localhost does not respond** (Minikube/kind), use port-forward in three terminals:
```
kubectl port-forward svc/exam-v1-svc 8081:8081
kubectl port-forward svc/exam-v2-svc 8082:8082
kubectl port-forward svc/exam-v3-svc 8083:8083
```

## Cleanup
```
kubectl delete -f k8s/
```

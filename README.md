# Practice DevOps App

## Goal -
A deliberately minimal Flask App, built as a vehicle to practice and demonstrate use of Docker, Kubernetes, Git Branching, and CI/CD - the app was made using ClaudeCode and it's functionality is intentionally trivial.
 
## Status - 
App has been fully Dockerized, deployed to a local Kubernetes cluster (Deployment,Service, ConfigMap, health probes), with automated CI/CD workflow via GitHub Actions, this builds image and pushes to Docker Hub on every push. Self-healing and scaling tested and confirmed to be working.

## Tech stack
| Layer | Choice |
|-------|--------|
| Backend | Python (Flask) |
| Frontend | HTML/CSS/JS (inline) |
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube, local) |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |

## Dockerizing
Wrote a Dockerfile from scratch (base image: python:3.14-slim, matching the local Python version). Built and ran the image locally, confirmed working via the homepage, live tip button, and health endpoint.

Key decisions:
- Copied requirements.txt separately, before the rest of the code, to take advantage of Docker's build caching — dependency installation only reruns when requirements.txt itself changes, not on every code edit.
- Used `imagePullPolicy: Never` later in Kubernetes since the image is loaded directly into Minikube rather than pushed to a registry.

## Kubernetes Deployment
Deployed the Dockerized app to a local Minikube cluster.

- Deployment: 3 replicas, with liveness and readiness probes (HTTP GET on `/`) built in from the start.
- Service: NodePort type, exposing the app for local browser access outside the cluster.
- ConfigMap: moved the hardcoded list of tips out of the application code into a ConfigMap, read via an environment variable at runtime — avoids needing to rebuild the image just to change display content.
- Secrets: not used in this project, since the app has no sensitive configuration (API keys, credentials) to manage.

Problems hit:
- The auto-generated service.yaml's selector incorrectly matched the Service's own name rather than the pods' actual label — had to manually correct it to `app: practice-devops-app`.
- After adding the ConfigMap and updating app.py to read from it, the running pods still used the old hardcoded version until the Docker image was rebuilt and reloaded into Minikube.

Tested and confirmed:
- Self-healing: deleted a pod manually, confirmed Kubernetes automatically created a replacement.
- Scaling: scaled replicas up (3→5) and down (5→2), confirmed pod count adjusted correctly both directions.

## CI/CD
Built a GitHub Actions workflow (`.github/workflows/docker-build.yml`) that automatically builds and pushes the Docker image to Docker Hub on every push to `main`.

- Started from GitHub's own suggested starter template, extended it from CI-only (build/verify) to full CI/CD (build + push) using `docker/login-action` and `docker/build-push-action`
- Docker Hub credentials stored securely via GitHub Secrets, never exposed in the workflow file itself

Problems hit (a real multi-step debugging chain):
1. Push rejected initially - the GitHub Personal Access Token needed an additional `workflow` scope to modify files under `.github/workflows/`
2. A leftover placeholder value in the image tag caused an "invalid reference format" error
3. The Docker Hub access token was generated with read-only permissions - needed Read & Write to actually push
4. The target Docker Hub repository didn't exist yet - had to create it manually
5. The final, root cause: the workflow's `tags:` field had accidentally used the GitHub username instead of the actual Docker Hub username - two different platforms, two different credentials, easy to conflate

## What I'd do differently / next steps
- Extend CD further to automatically deploy to a live cluster (not done here, since Minikube is local-only and unreachable from GitHub's servers) - would require a cloud-hosted cluster like AWS EKS
- Add a dedicated readiness check separate from the homepage route
- Use fine-grained Personal Access Tokens instead of classic ones, for tighter scoped permissions

## How to run it

Build and run locally with Docker:
```bash
docker build -t practice-devops-app .
docker run -p 5000:5000 practice-devops-app
```

Deploy to a local Kubernetes cluster (Minikube):
```bash
minikube start --driver=docker
minikube image load practice-devops-app
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
minikube service practice-devops-app-service --url
```

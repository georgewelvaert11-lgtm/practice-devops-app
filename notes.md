## GitHub Setup
- Initialized local Git repo (git init) in practice-devops-app
- Created .gitignore before first commit (excluding __pycache__, *.pyc, venv, .env)
- First commit: initial working Flask app (homepage, live tip button, health endpoint)
- Created new empty repo on GitHub, connected via git remote add origin, pushed with git push -u origin main
- Learned the distinction between local Git tracking (git init, commits stored in .git) and GitHub (remote hosting) - they're separate until explicitly connected and pushed
- Used feature branches for each phase (dockerize, k8s-deploy, add-ci) - committed locally on each branch, then merged into main and pushed from main, rather than pushing feature branches directly

## Dockerizing
- Checked local Python version, existing requirements.txt (Flask, gunicorn, anthropic, python-dotenv already listed from earlier work)
- Wrote Dockerfile from scratch (base image: python:3.14-slim, matching local Python version)
- Split COPY into two steps (requirements.txt first, then rest of code) to take advantage of Docker's build caching - dependency installs only rerun when requirements.txt itself changes, not on every code edit
- Built image (docker build -t practice-devops-app .), ran container (docker run -p 5000:5000 practice-devops-app)
- Confirmed working via homepage, live tip button, and health endpoint
- Committed Dockerfile + notes on the dockerize branch, merged into main, pushed to GitHub

## Kubernetes Deployment
- Wrote deployment.yaml (used kubectl create --dry-run to generate a starting template, corrected image name, added imagePullPolicy: Never, ports, liveness/readiness probes)
- Wrote service.yaml (used kubectl create --dry-run, had to fix selector - auto-generated version incorrectly matched the service's own name instead of the pod label)
- Both applied successfully, then i confirmed that the app was reachable via minikube service --url

## ConfigMap
- Created ConfigMap object
- Moved hardcoded TIPS list out of app.py into a ConfigMap (practice-devops-config)
- Used | as delimiter to store multiple tips as one string, split back into a list in app.py
- Referenced via envFrom.configMapRef in deployment.yaml
- Required rebuilding the Docker image (due to the fact that app.py changed) and reloading into Minikube before the change took effect

## Testing
- Self-healing: deleted a pod, confirmed Kubernetes automatically created a replacement
- Scaling: scaled replicas 3 → 5 → 2, confirmed pod count adjusted correctly both directions

## GitHub Actions CI/CD
- Started from GitHub's own suggested starter template ("Build a Docker image to deploy, run, or push to a registry"), found under the repo's Actions tab
- Template only covered CI (build-and-verify) - had to add CD manually:
  - Replaced the placeholder image name/timestamp tag with an actual fixed tag
  - Added a Docker Hub login step (docker/login-action), using GitHub Secrets for credentials
  - Replaced the plain `docker build` run command with docker/build-push-action, which handles both building and pushing in one step
  - Added push: true and the full tags: (username/repo:tag) needed to actually publish to Docker Hub
- Problems hit, in order:
  1. Push rejected - PAT needed 'workflow' scope added
  2. Invalid tag - left a placeholder value in tags: instead of a real one
  3. Insufficient token scopes - Docker Hub token was read-only, needed Read & Write
  4. Docker Hub repo didn't exist yet - had to create it manually first
  5. Wrong username in tags: - had accidentally used GitHub username instead of actual Docker Hub username
- Workflow now runs successfully on every push, confirmed image appears on Docker Hub

## Note on branch discipline
- Planned to use a separate feature branch for each phase (dockerize, k8s-deploy, add-ci), merging into main once each was working, this was followed correctly for the Dockerizing phase (see "Merge branch 'dockerize'" in commit history). For the Kubernetes and CI/CD phases, work ended up committed directly to main rather than on their own branches, branch discipline slipped partway through the project. The work itself is unaffected (all commits are still clearly labeled and readable in order), but the intended branch-per-phase workflow wasn't fully maintained throughout.

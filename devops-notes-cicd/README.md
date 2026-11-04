# DevOps Notes — Django + Docker + Jenkins + AWS EC2

A small notes app for a hands-on CI/CD lab. Jenkins checks out the repo, builds a Docker image, runs Django tests, deploys with Docker Compose, and verifies the health endpoint.

## Features
- Create, edit, and delete notes
- SQLite database stored in a named Docker volume
- Django automated tests
- Docker Compose health check
- Jenkins pipeline: checkout, build, test, deploy, verify

## Run locally or on the EC2 agent
Requirements: Docker Engine and Docker Compose plugin.

```bash
docker compose up -d --build
```

Open `http://localhost:8000`. Check with `curl http://localhost:8000/health/` and `docker compose ps`.

Stop without deleting notes: `docker compose down`.
Delete the database too: `docker compose down -v` (destructive).

## Push to GitHub
Create an empty GitHub repository, then run from this folder:

```bash
git init
git add .
git commit -m "Initial DevOps Notes application"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/devops-notes-cicd.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

## Jenkins setup
1. Ensure the **AGENT** labelled `dragon` has `git`, Docker Engine, Docker Compose plugin, and `curl`.
2. Ensure the Jenkins agent OS user can access Docker. On Ubuntu, an administrator can run `sudo usermod -aG docker jenkins` if the service user is `jenkins`; use the actual service account otherwise, then restart/re-login the agent. Docker group access is effectively root access; grant it only to trusted users.
3. In Jenkins, create/open a Pipeline job and choose **Pipeline script from SCM**.
4. SCM: Git. Repository URL: `https://github.com/YOUR_GITHUB_USERNAME/devops-notes-cicd.git`; branch `*/main`; Script Path `Jenkinsfile`.
5. Save and click **Build Now**. The Jenkinsfile uses `agent { label 'dragon' }`; change that label if your agent label differs.

If the job currently uses an inline Pipeline script, switch its Definition to **Pipeline script from SCM** so Jenkins loads the repository's Jenkinsfile.

## Open on AWS
Allow inbound TCP port `8000` in the EC2 AGENT security group, preferably only from your own public IP for this lab. Visit `http://YOUR_AGENT_PUBLIC_IP:8000`.

## Lab/security notes
This is a learning/demo setup. It uses Django's development server and `DEBUG=True`; do not expose it as a production service. For production, use Gunicorn or another production WSGI server, `DEBUG=False`, a strong secret from Jenkins credentials or a secret manager, restricted `ALLOWED_HOSTS`, HTTPS, and a production database. Never commit real secrets. The named `notes_data` volume preserves notes across container replacements. The pipeline does not delete images or volumes.

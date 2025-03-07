README: Exercise 1: Deploy FastAPI + PostgreSQL + pgAdmin on Minikube

Prerequisites

Ensure you have the following installed:

Docker

Kubectl

Minikube

Helm

Git

1️⃣ Clone the Repository

git clone https://github.com/ozzyaluyi/task-1-backend.git
cd into the cloned repository folder in this instance it will be `task-1-backend/backend`

2️⃣ Start Minikube

minikube start --driver=docker

3️⃣ Secret Required
To get KUBE_CONFIG:
cat ~/.kube/config | base64 -w 0
Copy the output and store it in GitHub Secrets as KUBE_CONFIG.

3️⃣ Build and Push Docker Image

docker build -t 2470/home_task:latest ./backend
docker push 2470/home_task:latest

4️⃣ Deploy with Helm

helm upgrade --install my-release ./helm-chart

5️⃣ Check Deployment Status after 50 seconds 

kubectl get pods

Ensure all pods are in a Running state.

6️⃣ Forward Ports for Local Access

kubectl port-forward svc/my-release-fastapi-app-backend 8080:8000 &
kubectl port-forward svc/my-release-fastapi-app-pgadmin 5050:80 &

7️⃣ Access the Services

FastAPI Backend: 
    * curl http://localhost:8080/health Expected Response:{"status": "ok"}
    * curl http://localhost:8080/readiness  Expected Response: {"status": "ready"}
    * curl -X POST "http://localhost:8080/populate?count=5"  Expected Response:{"message": "5 users inserted"}

pgAdmin: http://localhost:5050

8️⃣ Retrieve Database Credentials

Credentials are stored in the .env file inside the /backend directory.

cat backend/.env

9️⃣ Stop Minikube (when done)

minikube stop

🎯 Summary

This guide will help you deploy the FastAPI backend, PostgreSQL database, and pgAdmin UI in a Minikube Kubernetes cluster using Helm.

For issues, raise an Issue in the repository!


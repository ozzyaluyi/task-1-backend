# README: Exercise 1: Deploy FastAPI + PostgreSQL + pgAdmin on Minikube

## **Prerequisites**

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Git](https://git-scm.com/)

## **1️⃣ Clone the Repository**

```sh
git https://github.com/ozzyaluyi/task-1-backend.git 
cd task-1-backend/backend
```

## **2️⃣ Start Minikube**

```sh
minikube start --driver=docker
```

## **3️⃣ Build and Push Docker Image**

```sh
docker build -t 2470/home_task:latest ./backend
docker push 2470/home_task:latest
```

## **4️⃣ Deploy with Helm**

```sh
helm upgrade --install my-release ./helm-chart
```

## **5️⃣ Check Deployment Status after 50 seconds**

```sh
kubectl get pods
```

Ensure all pods are in a `Running` state.

## **6️⃣ Forward Ports for Local Access**

```sh
kubectl port-forward svc/my-release-fastapi-app-backend 8080:8000 &
kubectl port-forward svc/my-release-fastapi-app-pgadmin 5050:80 &
```

## **7️⃣ Access the Services**

- **FastAPI Backend:** [http://localhost:8080](http://localhost:8080)
  - curl http://localhost:8080/health Expected Response:{"status": "ok"}
  - curl http://localhost:8080/readiness Expected Response:{"status":ready"}
  - curl -X POST "http://localhost:8080/populate?count=5" Expected Response: {"message": "5 users inserted"}
  - curl http://localhost:8080/users Expected Response: {"users": []}
  - curl -X DELETE "http://localhost:8080/delete?count=5" Expected Response: {"message": "5 users deleted"}

- **pgAdmin:** [http://localhost:5050](http://localhost:5050)

## **8️⃣ Retrieve Database Credentials**

Credentials are stored in the `.env` file inside the `/backend` directory.

```sh
cat backend/.env
```

## **9️⃣ Stop Minikube (when done)**

```sh
minikube stop
```

---

## **Summary**

This guide helps deploy a **FastAPI backend**, **PostgreSQL database**, and **pgAdmin UI** in a **Minikube Kubernetes cluster** using **Helm**.

For issues, raise an **Issue** in the repository!


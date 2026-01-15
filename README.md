# 🚀 Projet DevOps : Containerisation & Orchestration Kubernetes

## 📋 Description

Ce projet valide les compétences DevOps fondamentales :
- Développement d'une API
- Containerisation avec Docker
- Déploiement et orchestration avec Kubernetes (Minikube)

L'application est une API Python (Flask) qui renvoie un message JSON et un statut de santé.  
Elle est déployée via une stratégie de **Rolling Update**.

---

## 📂 Structure du Projet

DevOps_Project/
├── app.py # Code source de l'API Flask
├── Dockerfile # Instructions pour construire l'image
├── requirements.txt # Liste des dépendances Python
├── k8s/
│ └── deployment.yaml # Configuration Kubernetes (Deployment + Service NodePort)
└── README.md # Documentation du projet


---

## 🛠️ Installation et Démarrage

### 1️⃣ Prérequis

Assurez-vous d’avoir installé et lancé :

- Docker Desktop
- Minikube
- Kubectl
- Git

---

##  Option A : Lancement rapide avec Docker 

### Étape 1 : Récupérer l’image depuis Docker Hub


docker pull mohamedalichibani0110/devops-project:latest
## Étape 2 : Lancer le conteneur

docker run -p 5000:5000 mohamedalichibani0110/devops-project:latest

## Étape 3 : Accéder à l'application
Ouvrez votre navigateur à l'adresse :

http://localhost:5000
## Option B : Déploiement Kubernetes avec Minikube

## Étape 1 : Démarrer le cluster local
Assurez-vous que Docker Desktop est lancé, puis exécutez :

minikube start

## Étape 2 : Appliquer la configuration Kubernetes
Cette commande crée le Deployment (application) et le Service (exposition réseau).

kubectl apply -f k8s/deployment.yaml

## Étape 3 : Vérifier le déploiement
Vérifiez que les pods sont en statut Running :

kubectl get pods

## Étape 4 : Accéder à l'application
Minikube expose le service via un tunnel :

minikube service devops-backend-service --url
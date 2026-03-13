# Skynet Ops Audit Service

## Project Overview

**skynet-ops-audit-service** is a lightweight cloud-deployed audit event service built to demonstrate practical **Cloud Operations (CloudOps)** practices.

The service exposes a REST API that allows systems to send operational or audit events, stores those events, and allows retrieval for analysis or monitoring.

This project focuses not only on application functionality but also on **operational readiness**, including:

* Infrastructure as Code (Terraform)
* Containerized deployment (Docker)
* Cloud monitoring and observability
* Alerting and operational runbooks
* Cost awareness and security considerations

---

# Architecture

                          User / Client
                               │
                               ▼
                           Internet
                               │
                               ▼
                       Security Group
                 (Allow ports: 22, 3000)
                               │
                               ▼
                 AWS EC2 Instance (t2.micro)
           Infrastructure Provisioned by Terraform
                               │
                               ▼
                        Docker Container
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
      Flask Audit Service API        SQLite Database
           (REST API)                 (events.db)
                │
                │ Stores and retrieves audit events
                │
                ▼

──────────────────────── Monitoring & Observability ────────────────────────

                 EC2 Instance
                       │
                       ▼
                CloudWatch Logs
                       │
                       ▼
               CloudWatch Alarm
                 (CPU > 80%)
                       │
                       ▼
                   Amazon SNS
                       │
                       ▼
             Email Notification Alerts

### Architecture Components

| Component              | Description                            |
| ---------------------- | -------------------------------------- |
| **User / Client**      | Sends audit events to the API          |
| **AWS EC2 (t2.micro)** | Hosts the containerized service        |
| **Docker Container**   | Runs the Flask audit event API         |
| **Flask Application**  | Processes and stores audit events      |
| **SQLite Database**    | Lightweight persistent event storage   |
| **CloudWatch Logs**    | Collects instance system logs          |
| **CloudWatch Alarm**   | Monitors CPU usage                     |
| **Amazon SNS**         | Sends email alerts when alarms trigger |

---

# Key Features

* REST API for receiving and retrieving audit events
* Containerized deployment using Docker
* Infrastructure provisioning using Terraform
* AWS EC2 cloud deployment
* Observability using CloudWatch Logs
* Monitoring using CloudWatch Alarms
* Email alerting using Amazon SNS
* Operational documentation and runbooks

---

# API Endpoints

| Method | Endpoint  | Description            |
| ------ | --------- | ---------------------- |
| GET    | `/health` | Health check endpoint  |
| POST   | `/events` | Submit an audit event  |
| GET    | `/events` | Retrieve stored events |

---

# Sample Event Payload

```json
{
  "type": "login_attempt",
  "tenantId": "tenant-001",
  "severity": "warning",
  "message": "Multiple failed login attempts detected",
  "source": "auth-service"
}
```

---

# Deployment

Infrastructure is provisioned using **Terraform**.

### Step 1 — Navigate to Terraform Directory

```
cd terraform
```

### Step 2 — Initialize Terraform

```
terraform init
```

### Step 3 — Deploy Infrastructure

```
terraform apply
```

Terraform automatically performs the following:

* Creates an EC2 instance
* Configures security groups
* Installs Docker
* Clones the repository
* Builds and runs the containerized application

---

# Accessing the Service

After deployment retrieve the public IP:

```
terraform output
```

Then access the API:

```
http://<PUBLIC_IP>:3000/health
```

---

# Monitoring and Observability

The system uses **AWS CloudWatch** for operational monitoring.

### Logging

CloudWatch Logs collect:

* EC2 system logs
* Application runtime logs

### Monitoring

CloudWatch monitors EC2 metrics including:

* CPU Utilization

### Alerting

If CPU usage exceeds **80%**, a CloudWatch alarm triggers an **SNS notification**, sending an email alert.

---

# Documentation

Detailed operational documentation is available in the `docs` directory.

| Document                     | Description                                              |
| ---------------------------- | -------------------------------------------------------- |
| `cost-optimization.md`       | Analysis of infrastructure cost decisions                |
| `security-considerations.md` | Security design and best practices                       |
| `operational-runbook.md`     | Procedures for operating and troubleshooting the service |

---

# Repository Structure

```
skynet-ops-audit-service
│
├── service
│   └── app.py
│
├── terraform
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── docs
│   ├── architecture-diagram.png
│   ├── cost-optimization.md
│   ├── security-considerations.md
│   └── operational-runbook.md
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Future Improvements

Potential production improvements include:

* Application Load Balancer
* Auto Scaling Group
* Managed database (Amazon RDS)
* Container orchestration using Amazon ECS or Kubernetes
* CI/CD pipeline integration

---

# Author

**Akhilesh Jagadale**

Cloud & DevOps enthusiast focused on building scalable, observable cloud systems.

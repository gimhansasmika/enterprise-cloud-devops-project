

\# Enterprise Cloud Infrastructure \& DevOps Automation



A practical AWS cloud infrastructure project demonstrating

cloud networking, Linux administration, Docker, FastAPI,

PostgreSQL, API security, Terraform, and GitHub Actions.



\## Technologies



\- AWS VPC, EC2, Security Groups

\- Ubuntu Linux

\- Docker and Nginx

\- Python FastAPI

\- PostgreSQL

\- Terraform

\- GitHub Actions



\## Architecture



Browser → Nginx → FastAPI → PostgreSQL



The application uses Docker networking to keep the backend

and database ports unpublished.



\## Features



\- Custom containerized web frontend

\- Nginx reverse proxy

\- FastAPI REST API with CRUD operations

\- PostgreSQL persistent storage

\- API key authentication

\- Network access restrictions

\- Terraform read-only VPC inspection

\- Automated Docker image builds using GitHub Actions



\## Security



Secrets and private keys are excluded from version control.



Asset API access is restricted at the Nginx layer.

HTTPS and additional production hardening remain future work.



\## Terraform



The Terraform configuration reads an existing AWS VPC

using a data source. It does not provision the infrastructure.



\## Project Status



Portfolio lab under development.




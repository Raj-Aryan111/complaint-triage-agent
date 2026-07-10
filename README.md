# NovaMart Complaint Triage Agent

An AI-powered customer complaint resolution system that automates complaint analysis, policy retrieval, historical case retrieval, compliance validation, and resolution generation using LangGraph, Retrieval-Augmented Generation (RAG), and FastAPI.

The project simulates an enterprise-grade customer support workflow for an e-commerce platform by combining LLM reasoning with company policies and historical complaint data.

---

## Overview

NovaMart Complaint Triage Agent is designed to streamline customer support operations by automatically:

- Understanding customer complaints
- Classifying complaint category and severity
- Retrieving relevant company policies
- Retrieving similar historical complaint resolutions
- Generating policy-compliant AI recommendations
- Validating responses through compliance checks
- Supporting human approval and escalation workflows

The system includes both customer-facing and support-agent dashboards.

---


# Problem Statement

Modern e-commerce platforms receive thousands of customer complaints every day. Traditional complaint handling often suffers from:

- Long response times due to manual review.
- Inconsistent resolutions across different support agents.
- Difficulty locating relevant company policies.
- Lack of utilization of historical complaint resolutions.
- Compliance risks caused by policy violations.
- High workload on human support teams.
- Delayed escalation of high-priority cases.
- Limited transparency into the reasoning behind AI-generated decisions.

These challenges increase operational costs while reducing customer satisfaction.

---

# Solution

NovaMart Complaint Triage Agent automates the complete complaint resolution workflow using AI, Retrieval-Augmented Generation (RAG), and LangGraph.

Instead of relying solely on an LLM, the system combines:

- Customer order information
- Company policy documents
- Historical complaint resolutions
- Compliance validation
- Workflow-based decision making

to generate accurate, explainable, and policy-compliant resolutions.

---

# How This Project Solves Real Business Problems

| Business Challenge | Solution |
|--------------------|----------|
| Manual complaint analysis | Automatically classifies complaints using AI. |
| Slow policy lookup | Retrieves the most relevant policy sections using ChromaDB. |
| Inconsistent resolutions | Generates standardized responses based on company policies and previous cases. |
| Compliance violations | Validates every recommendation through a dedicated compliance node before sending it. |
| High support workload | Automates routine complaints while escalating only complex cases to human agents. |

---

# Key Features

- AI-powered complaint classification
- Retrieval-Augmented Generation (RAG)
- Policy-aware response generation
- Historical case retrieval
- Compliance validation
- Multi-step LangGraph workflow
- Human approval workflow
- Customer dashboard
- Agent dashboard
- Dockerized deployment

---

# Advanced Features

Unlike a simple chatbot, this project includes several enterprise-grade capabilities:

### Multi-Step Agentic Workflow

Uses LangGraph to orchestrate independent workflow nodes including classification, retrieval, generation, compliance validation, revision, escalation, and response delivery.

### Retrieval-Augmented Generation (RAG)

The LLM never answers from memory alone. Every recommendation is grounded using:

- Company policy manuals
- Compliance rulebooks
- Historical complaint resolutions

stored inside ChromaDB.

### Human-in-the-Loop

High-risk or low-confidence cases are automatically routed for manual approval instead of being sent directly to customers.

### Compliance Engine

Every AI recommendation is validated before delivery to ensure:

- Refund limits are respected
- Confidence threshold is satisfied
- Escalation rules are enforced
- Company policies are followed

### Explainable AI

Instead of returning only a final decision, the system provides:

- AI reasoning
- Policy references
- Similar historical cases
- Workflow execution trace

making every recommendation transparent and auditable.

### Enterprise Dashboard

The support dashboard provides:

- Customer profile
- Order details
- Complaint analysis
- AI recommendation
- Policy references
- Historical cases
- Compliance result
- Approval/Escalation actions

allowing agents to make informed decisions quickly.

### End-to-End Workflow Automation

The complaint lifecycle is fully automated from:

Customer Complaint

↓

Order Retrieval

↓

Complaint Classification

↓

Policy Retrieval

↓

Historical Case Retrieval

↓

AI Recommendation

↓

Compliance Validation

↓

Approval / Revision / Escalation

↓

Customer Resolution

reducing manual intervention while maintaining policy compliance.

---

## Features

- AI-powered complaint classification
- Retrieval-Augmented Generation (RAG)
- Policy-based resolution generation
- Historical case retrieval using ChromaDB
- LangGraph multi-step workflow orchestration
- Compliance validation
- Human-in-the-loop approval workflow
- Customer dashboard
- Internal agent dashboard
- FastAPI REST API
- Dockerized deployment

---

## Architecture

```
                    Customer Complaint
                           │
                           ▼
                    FastAPI Backend
                           │
                 LangGraph Workflow
                           │
      ┌──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼
 Order Lookup   Policy Retrieval  Historical Cases
      │              │              │
      └──────────────┴──────────────┘
                     ▼
            AI Response Generation
                     ▼
           Compliance Verification
                     ▼
        Approve │ Revise │ Escalate
                     ▼
          Customer & Agent Response
```

---

## Tech Stack

### Backend

- Python 3.11
- FastAPI
- LangGraph
- LangChain
- ChromaDB
- SQLAlchemy
- SQLite

### AI

- Google Gemini
- HuggingFace Embeddings
- BAAI/bge-small-en-v1.5
- Retrieval-Augmented Generation (RAG)

### Frontend

- Streamlit

### Deployment

- Docker
- Docker Compose

---

## Project Structure

```
complaint-triage-agent/

├── data/
│   ├── complaints/
│   ├── orders/
│   ├── policies/
│   └── precedents/
│
├── frontend/
│   ├── customer_app.py
│   └── agent_dashboard.py
│
├── src/
│   ├── classification/
│   ├── config/
│   ├── db/
│   ├── generation/
│   ├── graph/
│   ├── nodes/
│   ├── rag/
│   └── schemas/
│
├── scripts/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── api.py
└── README.md
```

---

## Workflow

1. Customer submits complaint
2. Order information is retrieved
3. Complaint is classified
4. Company policies are retrieved using RAG
5. Similar historical complaints are retrieved
6. Gemini generates a proposed resolution
7. Compliance checks validate the recommendation
8. Workflow decides whether to:
   - Send response
   - Revise response
   - Escalate to a human agent

---

## REST API

### Customer

```
POST /complaint
```

Processes customer complaints and returns the generated resolution.

---

### Agent

```
POST /agent/complaint
```

Returns:

- Customer details
- Order information
- Complaint classification
- AI recommendation
- Compliance results
- Policy references
- Historical cases
- Workflow execution trace

---

### Agent Actions

```
POST /agent/approve
```

Approve complaint resolution.

```
POST /agent/escalate
```

Escalate complaint for manual review.

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/Raj-Aryan111/complaint-triage-agent.git

cd complaint-triage-agent
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
LLM_PROVIDER=gemini
```

---

### Run Backend

```bash
uvicorn api:app --reload
```

---

### Customer Dashboard

```bash
streamlit run frontend/customer_app.py
```

---

### Agent Dashboard

```bash
streamlit run frontend/agent_dashboard.py
```

---

## Docker

Build and start all services.

```bash
docker compose up --build
```

Services

Backend

```
http://localhost:8000
```

Customer Dashboard

```
http://localhost:8501
```

Agent Dashboard

```
http://localhost:8502
```

---

## Sample Complaint

Order ID

```
OD562837684
```

Complaint

```
My product arrived damaged and I would like a replacement.
```

---

## Future Improvements

- JWT Authentication
- Multi-agent architecture
- Asynchronous workflow execution
- PostgreSQL integration
- Redis caching
- Human feedback learning
- Admin analytics dashboard
- Kubernetes deployment
- CI/CD pipeline
- Monitoring and observability

---

## License

This project is licensed under the MIT License.

---

## Author

**Raj Aryan**

GitHub:
https://github.com/Raj-Aryan111
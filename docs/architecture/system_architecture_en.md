# System Architecture

## 1. Overview

The Enterprise AI Technical Support Platform is an AI-powered technical support system designed to assist customers, support engineers, and administrators throughout the technical support lifecycle.

The platform integrates:

* AI-powered knowledge-based question answering
* Retrieval-Augmented Generation (RAG)
* Intelligent ticket management
* AI-assisted ticket analysis and assignment
* Knowledge base management
* Engineer workspace
* Analytics and reporting
* Role-based access control

The system is designed as a modular full-stack application, with a React frontend, FastAPI backend, AI service layer, and persistent data storage.

---

## 2. Architecture Overview

The system is organised into five major layers:

```text
┌────────────────────────────────────────────────────────────┐
│                  Presentation Layer                        │
│                                                            │
│              React + TypeScript Frontend                   │
│                                                            │
│    Customer UI │ Engineer UI │ Admin Dashboard             │
└───────────────────────────┬────────────────────────────────┘
                            │ HTTPS / REST API
                            ▼
┌────────────────────────────────────────────────────────────┐
│                       API Layer                            │
│                                                            │
│                         FastAPI                            │
│                                                            │
│ Auth │ Chat │ Tickets │ Knowledge │ Users │ Analytics      │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                  Application Layer                         │
│                                                            │
│ User Service        Ticket Service                         │
│ AI Assistant        Knowledge Service                      │
│ AI Ticket Assistant Analytics Service                      │
└───────────────┬───────────────────────────┬────────────────┘
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌────────────────────────────┐
│         AI Layer          │   │         Data Layer          │
│                           │   │                            │
│ Query Processing          │   │ PostgreSQL                 │
│ Hybrid Retrieval          │   │ Redis                      │
│ Reranking                 │   │ Vector Database            │
│ Confidence Evaluation     │   │ Knowledge Documents        │
│ Prompt Management         │   │                            │
│ LLM Integration           │   │                            │
└──────────────┬────────────┘   └────────────────────────────┘
               │
               ▼
        External LLM API
        Qwen / OpenAI
```

---

## 3. Presentation Layer

The presentation layer provides interfaces for different types of users.

The frontend will be implemented using React and TypeScript.

### 3.1 Customer Interface

Customers can:

* Submit questions to the AI assistant
* View AI-generated answers
* Create technical support tickets
* View their tickets
* Track ticket status
* Communicate with support engineers
* Confirm ticket resolution
* Submit satisfaction feedback

### 3.2 Engineer Interface

Support engineers can:

* View assigned tickets
* View ticket details
* Update ticket status
* Communicate with customers
* View related knowledge-base articles
* View similar historical tickets
* Use AI-generated response suggestions
* Resolve tickets

### 3.3 Administrator Interface

Administrators can:

* Manage users
* Manage engineers
* Manage tickets
* Manage knowledge-base content
* View system statistics
* Monitor support performance
* Configure system settings

---

## 4. API Layer

The API layer provides communication between the frontend and backend services.

FastAPI will be used to expose RESTful APIs.

The API will be organised into several functional areas:

```text
/api
│
├── /auth
├── /chat
├── /tickets
├── /knowledge
├── /users
└── /analytics
```

Examples:

```text
POST   /api/auth/login

POST   /api/chat

POST   /api/tickets
GET    /api/tickets
GET    /api/tickets/{ticket_id}
PATCH  /api/tickets/{ticket_id}

POST   /api/knowledge/upload
GET    /api/knowledge

GET    /api/analytics/overview
```

The API layer is responsible for:

* Request validation
* Authentication and authorisation
* Routing requests to application services
* Returning structured responses
* Handling API-level errors

Business logic should not be placed directly inside API route handlers.

---

## 5. Application Layer

The application layer contains the main business logic of the platform.

The system will be divided into independent services/modules.

### 5.1 User Service

Responsible for:

* User registration
* Authentication
* User profiles
* Role management
* Access control

Supported roles:

```text
Customer
Engineer
Admin
```

### 5.2 Ticket Service

Responsible for the ticket lifecycle:

```text
New
 ↓
Assigned
 ↓
Processing
 ↓
Resolved
 ↓
Closed
```

The Ticket Service manages:

* Ticket creation
* Ticket assignment
* Ticket status
* Ticket comments
* Ticket history
* Customer confirmation
* Satisfaction feedback

### 5.3 AI Assistant Service

Responsible for customer-facing AI question answering.

It coordinates:

```text
Query Processing
        ↓
Retrieval
        ↓
Reranking
        ↓
Confidence Evaluation
        ↓
LLM Generation
        ↓
Response
```

### 5.4 AI Ticket Assistant

Provides AI capabilities inside the ticket workflow.

Potential responsibilities include:

* Issue classification
* Product identification
* Priority estimation
* Suggested engineer assignment
* Similar-ticket retrieval
* Knowledge-base recommendation
* Response generation
* Ticket summarisation

### 5.5 Knowledge Service

Responsible for managing the knowledge base.

It will support:

* Knowledge document upload
* Document processing
* Text chunking
* Embedding generation
* Vector indexing
* Knowledge search
* Knowledge updates
* Knowledge deletion

### 5.6 Analytics Service

Responsible for collecting and aggregating support metrics.

Potential metrics include:

* Number of tickets
* Average response time
* Average resolution time
* AI resolution rate
* Frequently reported problems
* Engineer workload
* Customer satisfaction
* Knowledge-base retrieval performance

---

## 6. AI Layer

The AI layer is the core intelligence layer of the platform.

It is designed to be independent from the API and user-interface layers so that AI components can be modified without changing the overall application architecture.

### 6.1 Query Processing

The system processes the user's query before retrieval.

Potential processing includes:

* Query normalisation
* Query rewriting
* Conversation context integration

Example:

```text
Original:

"ERP登录不了怎么办？"

        ↓

Processed Query:

"ERP system login failure troubleshooting"
```

### 6.2 Hybrid Retrieval

The retrieval system will combine semantic and lexical retrieval.

```text
                     User Query
                         │
                ┌────────┴────────┐
                ▼                 ▼
             BM25            Vector Search
                │                 │
                └────────┬────────┘
                         ▼
                      Fusion
                         │
                         ▼
                     Reranker
                         │
                         ▼
                  Top-K Documents
```

Vector retrieval is useful for semantic similarity, while BM25 can improve retrieval for exact keywords, product names, error codes, and other specific terminology.

### 6.3 Reranking

Retrieved documents will be reranked using a cross-encoder.

The existing prototype uses:

```text
BAAI/bge-reranker-base
```

The reranker will select the most relevant documents before they are passed to the LLM.

### 6.4 Confidence Evaluation

The system will evaluate whether the retrieved information is sufficiently relevant.

```text
              Retrieval
                  │
                  ▼
             Confidence
              /       \
           High       Low
            │          │
            ▼          ▼
         Answer     Ticket Flow
```

The purpose is to reduce unsupported answers and provide a controlled transition from AI self-service to human support.

The exact confidence threshold will be determined experimentally during the evaluation phase rather than being arbitrarily fixed during initial design.

### 6.5 LLM Integration

The platform will use an external Large Language Model through an abstraction layer.

Conceptually:

```text
LLMService
   │
   ├── Qwen
   ├── OpenAI
   └── Other compatible models
```

This allows the underlying model provider to be changed without modifying the rest of the application.

---

## 7. Data Layer

The platform will use different storage technologies according to the type of data being stored.

### 7.1 PostgreSQL

PostgreSQL will store structured business data.

Examples include:

```text
User
Ticket
Comment
Assignment
Category
Satisfaction
KnowledgeDocument
```

PostgreSQL is the primary source of truth for business transactions.

### 7.2 Redis

Redis will be used for data requiring fast access.

Potential uses include:

* Conversation memory
* Session data
* Caching
* Rate limiting

### 7.3 Vector Database

A vector database will store embeddings for semantic knowledge retrieval.

The initial implementation will continue using Chroma.

The knowledge ingestion process will follow:

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Index
```

The vector database is responsible for semantic retrieval rather than storing the primary business data of the platform.

---

## 8. External AI Services

The AI layer communicates with external LLM providers.

The initial implementation can continue using Qwen through the existing API provider.

The application should isolate provider-specific code inside the LLM integration layer.

This prevents the rest of the application from becoming tightly coupled to a specific model provider.

---

## 9. Core AI Support Workflow

The main customer-support workflow is:

```text
Customer
   │
   ▼
AI Assistant
   │
   ▼
Query Processing
   │
   ▼
Hybrid Retrieval
   │
   ▼
Reranking
   │
   ▼
Confidence Evaluation
   │
   ├─────────────── High ───────────────┐
   │                                    │
   ▼                                    ▼
Generate Answer                    Return Answer
   │
   │
   └──────────── Low ───────────────┐
                                    ▼
                              Create Ticket
                                    │
                                    ▼
                           AI Ticket Analysis
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                Category        Priority        Assignment
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                           Engineer Workspace
                                    │
                                    ▼
                              AI Copilot
                                    │
                                    ▼
                              Resolution
                                    │
                                    ▼
                           Knowledge Update
                                    │
                                    ▼
                               Analytics
```

This workflow connects the existing AI customer-service assistant with the broader technical-support platform.

---

## 10. Architectural Principles

The system will follow the following principles.

### 10.1 Separation of Concerns

Frontend, API, business logic, AI services, and data storage should have clearly defined responsibilities.

### 10.2 Modularity

AI components should be replaceable without requiring major changes to the ticket-management system.

### 10.3 AI as a Service Capability

AI should support multiple business workflows rather than exist only as a standalone chatbot.

### 10.4 Human-in-the-Loop

The system should not attempt to automate every support decision.

Low-confidence questions and AI-generated recommendations should be able to transition to human engineers.

### 10.5 Evaluation-Driven Development

AI components should be evaluated using a dedicated evaluation dataset and measurable metrics.

Changes to retrieval, reranking, prompting, or models should be compared against previous versions.

### 10.6 Provider Independence

The application should avoid tightly coupling business logic to a specific LLM provider.

### 10.7 Security

Sensitive information such as API keys, passwords, and environment-specific configuration must not be committed to the repository.

---

## 11. Initial Technology Stack

| Layer               | Technology                |
| ------------------- | ------------------------- |
| Frontend            | React + TypeScript        |
| Backend             | Python + FastAPI          |
| Relational Database | PostgreSQL                |
| Cache / Memory      | Redis                     |
| Vector Database     | Chroma                    |
| Retrieval           | BM25 + Vector Search      |
| Reranking           | BGE Cross-Encoder         |
| LLM                 | Qwen / compatible LLM API |
| Containerisation    | Docker + Docker Compose   |
| Version Control     | Git + GitHub              |

Technology choices may be revised during implementation if benchmarking or architectural requirements justify the change.

---

## 12. Current Prototype vs Target Architecture

The existing prototype already provides several components of the target AI pipeline:

```text
Existing Prototype
─────────────────────────────

Excel Knowledge Base
        ↓
Document Processing
        ↓
Embedding
        ↓
Chroma
        ↓
Vector Retrieval
        ↓
Keyword Filtering
        ↓
BGE Reranker
        ↓
Top Documents
        ↓
Qwen
        ↓
FastAPI
        ↓
HTML Frontend
```

The target architecture expands this into:

```text
Target Platform
────────────────────────────────────

React Frontend
        ↓
FastAPI API Layer
        ↓
Application Services
        │
        ├── AI Assistant
        │       ↓
        │   Hybrid Retrieval
        │       ↓
        │   Reranking
        │       ↓
        │   Confidence
        │
        ├── Ticket Management
        │
        ├── AI Ticket Assistant
        │
        ├── Knowledge Management
        │
        └── Analytics
                │
                ▼
       PostgreSQL / Redis / Vector DB
```

The existing prototype will therefore be **refactored and integrated**, rather than discarded and rewritten from scratch.

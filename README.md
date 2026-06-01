# Job Finder AI

Job Finder AI is an AI-powered job search assistant built with LangGraph, LangChain, and OpenRouter.

The assistant interacts naturally with users, identifies their job search intent, extracts relevant information such as desired role and preferences, searches for available opportunities, and generates conversational responses based on the results.

The project follows an agent-based architecture using LangGraph, where each node is responsible for a specific task in the workflow.

---

# Features

- Natural language interaction
- Job intent detection using LLMs
- Structured information extraction
- Job search automation
- Dynamic response generation
- LangGraph workflow orchestration
- LangSmith observability and tracing
- OpenRouter integration
- Modular and scalable architecture

---

# Architecture

```text
User
  │
  ▼
Identify Intent
  │
  ▼
Search Jobs
  │
  ▼
Generate Response
  │
  ▼
User
```

---

# Project Structure

```text
src/
│
├── config/
│   └── model_config.py
│
├── graph/
│   │
│   ├── graph.py
│   │
│   ├── nodes/
│   │   ├── identifyJobs.py
│   │   ├── searchJobs.py
│   │   └── generateResponse.py
│   │
│   └── prompts/
│       ├── identifyIntent.py
│       └── generateResponse.py
│
├── services/
│   └── openRouter.py
│
└── utils/
```

---

# Workflow

## 1. Intent Identification

The assistant analyzes the user's message and extracts information such as:

- Role
- Location
- Seniority
- Company preferences
- Remote preferences

Example:

```text
I am looking for a remote Machine Learning Engineer position.
```

Structured output:

```json
{
  "intent": "job_search",
  "role": "Machine Learning Engineer",
  "location": null,
  "seniority": null,
  "company": null,
  "remote": true
}
```

---

## 2. Job Search

After identifying the role, the system searches for matching opportunities.

The search layer can be connected to:

- Custom APIs
- Company career pages
- Job boards
- Internal databases

---

## 3. Response Generation

The assistant generates conversational responses based on:

- User intent
- Search results
- Previous conversation context

Example:

```text
I found three Machine Learning Engineer opportunities that may fit your profile.

One is at Nubank focusing on recommendation systems, another at Spotify working with personalization models, and a third at Airbnb focused on ranking and search relevance.

Would you like more details about any of these?
```

---

# Technologies

- Python 3.12+
- LangGraph
- LangChain
- OpenRouter
- Pydantic
- LangSmith
- Dotenv

---

# Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_api_key

LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=job-finder-ai
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd job-finder-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip install -e .
```

---

# Running Locally

Start LangGraph:

```bash
langgraph dev
```

If blocking operations are still being migrated to async execution:

```bash
langgraph dev --allow-blocking
```

---

# LangSmith

To enable observability:

```env
LANGSMITH_API_KEY=your_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=job-finder-ai
```

LangSmith provides:

- Graph execution traces
- Node-level monitoring
- Prompt debugging
- Response inspection
- Agent evaluation

---

# Future Improvements

- Persistent conversation memory
- SQLite/PostgreSQL integration
- User profile storage
- Multi-turn job search refinement
- Resume analysis
- Application tracking
- Company recommendations
- Job ranking system
- Vector database integration
- RAG-based company information retrieval

---

# Example Conversation

User:

```text
I'm looking for Data Scientist positions.
```

Assistant:

```text
Great. Are you looking for remote opportunities, a specific location, or a particular company?
```

User:

```text
Remote positions.
```

Assistant:

```text
I found several remote Data Scientist opportunities. Some are focused on experimentation and analytics, while others involve machine learning and predictive modeling.

Would you like me to show the details?
```

---

# License

This project is available under the MIT License.
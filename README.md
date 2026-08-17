# AI Transformation Strategy Intelligence

## 1. Project Overview

AI Transformation Strategy Intelligence is an enterprise AI application that converts an organisation's business situation and external research into structured transformation intelligence.

The application follows this transformation flow:

Business Situation
→ External Change
→ Strategic Issues
→ Transformation Opportunities
→ Priorities
→ Initiatives
→ Outcomes

The application also provides an interactive interrogation feature that allows users to ask questions about the generated strategy intelligence.

---

## 2. Problem Statement

Organisations often have business challenges, operational data and external market information, but converting this information into prioritised transformation actions can be difficult.

This application addresses that problem by combining:

- Organisation-specific business information
- External research
- AI-powered analysis
- Persistent database storage
- Interactive strategy interrogation

---

## 3. Example Case

The application was demonstrated using:

**Organisation:** FreshMart Retail Pvt Ltd

**Industry:** Retail

**Business situation:**

Physical store sales are declining, inventory costs are increasing, and customers increasingly prefer digital shopping.

**Business objectives:**

- Increase revenue
- Reduce inventory costs
- Improve customer experience

**Available technology/data:**

- POS sales data
- Inventory system
- Customer loyalty data
- E-commerce website

---

## 4. Key Features

### Organisation Management

Users can enter:

- Organisation name
- Industry
- Business situation
- Business objectives
- Current technology/data
- Optional organisation documents

The information is stored persistently in SQLite.

### External Research

The application uses the Tavily API to retrieve external research relevant to the organisation's industry and transformation situation.

Research records contain:

- Title
- Summary
- Source URL

### AI Strategy Intelligence

Google Gemini analyses the organisation information and supplied research.

The AI produces:

- Strategic diagnosis
- Strategic issues
- Evidence
- Transformation opportunities
- Priorities
- Initiatives
- Expected outcomes

### Interrogate Findings

Users can ask questions about the generated strategy intelligence.

The application uses the generated intelligence as the basis for answering questions.

---

## 5. Architecture

The application consists of the following layers:

```text
                         USER
                           |
                           v
                  +-----------------+
                  | Streamlit UI    |
                  |    app.py       |
                  +--------+--------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
      Organisation      Research     Interrogate
         Module          Module        Findings
             |             |             |
             |             v             |
             |          Tavily           |
             |             |             |
             +-------------+-------------+
                           |
                           v
                  +-----------------+
                  |    AI Engine    |
                  |   Gemini API    |
                  +--------+--------+
                           |
                           v
                Strategy Intelligence
                           |
                           v
                  +-----------------+
                  | SQLite Database |
                  |   strategy.db   |
                  +-----------------+

```

## 6. Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| AI Model | Google Gemini API |
| External Research | Tavily API |
| Database | SQLite |
| Document Processing | Python document processing libraries |
| Configuration | Environment variables / `.env` |
| Development Environment | VS Code |

## 7. Project Structure

```text
AI_TRANSFORMATION_STRATEGY/
│
├── app.py
├── README.md
├── ARCHITECTURE.md
├── TESTING.md
├── requirements.txt
├── .env.example
├── freshmart_company.txt
│
├── services/
│   ├── ai_engine.py
│   ├── db.py
│   ├── documents.py
│   └── research.py
│
└── data/
    └── strategy.db
```

## 8. Data Flow

```text
Organisation Information
          |
          v
      SQLite
          |
          v
   External Research
       using Tavily
          |
          v
     Evidence Set
          |
          v
     Gemini AI Engine
          |
          v
 Strategy Intelligence
          |
          +----> Diagnosis
          |
          +----> Strategic Issues
          |
          +----> Opportunities
          |
          +----> Priorities
          |
          +----> Initiatives
          |
          +----> Outcomes
          |
          v
   Interrogate Findings
```

## 9. Installation

### Step 1: Create and activate the virtual environment

```text
python -m venv .venv
```

Activate it:

```text
.venv\Scripts\activate
```

### Step 2: Install dependencies

```text
pip install -r requirements.txt
```

### Step 3: Configure environment variables

Create a `.env` file in the project root.

Add:

```text
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_available_gemini_model
TAVILY_API_KEY=your_tavily_api_key
```

Do **not** submit your real API keys.

## 10. Run the Application

From the project directory:

```text
streamlit run app.py
```

The Streamlit application will open in the browser.

## 11. Application Workflow

### Step 1 — Organisation

Enter and save organisation information.

### Step 2 — Research

Enter a research query related to the organisation's industry and transformation situation.

The application retrieves external research through Tavily.

### Step 3 — Strategy Intelligence

The application combines stored organisation information and research and sends the information to Gemini for analysis.

### Step 4 — Interrogate Findings

Ask questions about the generated transformation intelligence.

## 12. Persistence

SQLite is used as the application's persistent storage layer.

The database stores organisation and research records.

The application was tested by restarting the application and confirming that previously stored information remained available.

## 13. Evidence and Traceability

External research is stored with its source URL.

The AI instructions require the model to use only the supplied organisation information and research and not fabricate external facts, citations, statistics or URLs.

This allows strategy recommendations to be connected to the organisation data and research supplied to the application.

## 14. Testing

Testing details are documented in:

`TESTING.md`

The application has been tested for:

- Organisation storage
- External research retrieval
- AI strategy generation
- Interrogate Findings
- Data persistence
- Multiple organisation processing
- Application startup

## 15. Security

API keys are stored using environment variables.

The following files must **not** be submitted:

```text
.env
.envapikey.txt
```

## 16. Submission Notes

The application uses external free-tier/API services and open-source Python libraries.

No paid software licence is required to demonstrate the application.

The application contains:

- Frontend
- Backend
- Persistent storage
- External research integration
- AI model integration
- Multiple-record processing
- Interactive user functionality
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit UI    │
                  │    app.py       │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      Organisation      Research     Interrogate
         Module          Module        Findings
             │             │             │
             │             ▼             │
             │        Tavily API         │
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  ┌─────────────────┐
                  │  AI Engine      │
                  │ ai_engine.py    │
                  │    Gemini       │
                  └────────┬────────┘
                           │
                           ▼
                  Strategy Intelligence
                           │
                           ▼
                  ┌─────────────────┐
                  │ SQLite Database │
                  │ strategy.db     │
                  └─────────────────┘
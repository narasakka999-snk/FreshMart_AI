import sqlite3
import json
from pathlib import Path


DB_PATH = Path("data/strategy.db")


def conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    c = conn()
    cur = c.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS organisations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        industry TEXT,
        business_context TEXT
    );

    CREATE TABLE IF NOT EXISTS research (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organisation_id INTEGER,
        title TEXT,
        summary TEXT,
        url TEXT,
        FOREIGN KEY (organisation_id) REFERENCES organisations(id)
    );

    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organisation_id INTEGER UNIQUE,
        analysis_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organisation_id) REFERENCES organisations(id)
    );
    """)

    c.commit()
    c.close()


def save_organisation(name, industry, business_context):
    c = conn()
    cur = c.cursor()

    cur.execute(
        "INSERT INTO organisations(name, industry, business_context) VALUES (?, ?, ?)",
        (name, industry, business_context)
    )

    c.commit()
    oid = cur.lastrowid
    c.close()

    return oid


def save_research(organisation_id, item):
    c = conn()

    c.execute(
        """
        INSERT INTO research(
            organisation_id,
            title,
            summary,
            url
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            organisation_id,
            item.get("title", ""),
            item.get("summary", ""),
            item.get("url", "")
        )
    )

    c.commit()
    c.close()


def get_all_research(organisation_id):
    c = conn()

    rows = c.execute(
        """
        SELECT title, summary, url
        FROM research
        WHERE organisation_id=?
        """,
        (organisation_id,)
    ).fetchall()

    c.close()

    return [
        {
            "title": r[0],
            "summary": r[1],
            "url": r[2]
        }
        for r in rows
    ]


def get_organisation(organisation_id):
    c = conn()

    row = c.execute(
        """
        SELECT name, industry, business_context
        FROM organisations
        WHERE id=?
        """,
        (organisation_id,)
    ).fetchone()

    c.close()

    if not row:
        return {}

    return {
        "name": row[0],
        "industry": row[1],
        "business_context": row[2]
    }


def save_analysis(organisation_id, analysis):
    """
    Save the AI-generated strategy intelligence for an organisation.

    JSON is used so the complete analysis structure can be restored
    exactly when the application is restarted.
    """

    c = conn()

    analysis_json = json.dumps(analysis, ensure_ascii=False)

    c.execute(
        """
        INSERT INTO analyses(
            organisation_id,
            analysis_json
        )
        VALUES (?, ?)
        ON CONFLICT(organisation_id)
        DO UPDATE SET
            analysis_json=excluded.analysis_json,
            created_at=CURRENT_TIMESTAMP
        """,
        (
            organisation_id,
            analysis_json
        )
    )

    c.commit()
    c.close()


def get_analysis(organisation_id):
    """
    Retrieve the most recently saved AI strategy intelligence.
    """

    c = conn()

    row = c.execute(
        """
        SELECT analysis_json
        FROM analyses
        WHERE organisation_id=?
        """,
        (organisation_id,)
    ).fetchone()

    c.close()

    if not row:
        return None

    return json.loads(row[0])
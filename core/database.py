import sqlite3


class Database:
    def __init__(self, db_path: str = "seven.db"):
        self.db_path = db_path
        self._init()

    def _init(self):
        with sqlite3.connect(self.db_path) as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS content_plan (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    date       TEXT NOT NULL,
                    content    TEXT NOT NULL,
                    type       TEXT DEFAULT 'tweet',
                    status     TEXT DEFAULT 'planned',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS ideas (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    idea     TEXT NOT NULL,
                    topic    TEXT DEFAULT '',
                    used     INTEGER DEFAULT 0,
                    saved_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS analyses (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    tweet       TEXT NOT NULL,
                    analysis    TEXT NOT NULL,
                    score       INTEGER DEFAULT 0,
                    analyzed_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def add_to_plan(self, date, content, content_type='tweet'):
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                "INSERT INTO content_plan (date,content,type) VALUES (?,?,?)",
                (date, content, content_type)
            )

    def get_plan(self, days=14):
        with sqlite3.connect(self.db_path) as c:
            return c.execute("""
                SELECT date,content,type,status FROM content_plan
                WHERE date >= date('now') ORDER BY date ASC LIMIT ?
            """, (days * 3,)).fetchall()

    def save_idea(self, idea, topic=''):
        with sqlite3.connect(self.db_path) as c:
            c.execute("INSERT INTO ideas (idea,topic) VALUES (?,?)", (idea, topic))

    def save_analysis(self, tweet, analysis, score=0):
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                "INSERT INTO analyses (tweet,analysis,score) VALUES (?,?,?)",
                (tweet, analysis, score)
            )

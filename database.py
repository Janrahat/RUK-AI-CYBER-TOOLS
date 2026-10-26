"""SQLite storage for generated links and consent-based analytics."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

@contextmanager
def connect(db_path):
    path = Path(db_path)
    if str(path) != ":memory:": path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path)); conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally: conn.close()

def init_db(db_path):
    with connect(db_path) as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS links (id TEXT PRIMARY KEY, destination TEXT NOT NULL, campaign TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL, expires_at TEXT); CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, link_id TEXT NOT NULL, clicked_at TEXT NOT NULL, consented INTEGER NOT NULL DEFAULT 0, referrer_host TEXT, FOREIGN KEY(link_id) REFERENCES links(id) ON DELETE CASCADE);''')

def now_iso(): return datetime.now(timezone.utc).isoformat(timespec="seconds")
def create_link(db_path, link_id, destination, campaign="", expires_at=None):
    with connect(db_path) as c: c.execute("INSERT INTO links(id,destination,campaign,created_at,expires_at) VALUES(?,?,?,?,?)", (link_id,destination,campaign[:120],now_iso(),expires_at))
def get_link(db_path, link_id):
    with connect(db_path) as c:
        row=c.execute("SELECT * FROM links WHERE id=?",(link_id,)).fetchone(); return dict(row) if row else None
def record_event(db_path, link_id, consented=False, referrer_host=None):
    with connect(db_path) as c: c.execute("INSERT INTO events(link_id,clicked_at,consented,referrer_host) VALUES(?,?,?,?)",(link_id,now_iso(),int(bool(consented)),referrer_host if consented else None))
def dashboard_rows(db_path):
    with connect(db_path) as c:
        rows=c.execute('''SELECT l.id,l.destination,l.campaign,l.created_at,l.expires_at,COUNT(e.id) AS total_clicks,SUM(CASE WHEN e.consented=1 THEN 1 ELSE 0 END) AS consented_clicks FROM links l LEFT JOIN events e ON e.link_id=l.id GROUP BY l.id ORDER BY l.created_at DESC''').fetchall(); return [dict(r) for r in rows]
def delete_all(db_path):
    with connect(db_path) as c: c.execute("DELETE FROM events"); c.execute("DELETE FROM links")
def delete_expired_events(db_path, retention_days):
    with connect(db_path) as c: c.execute("DELETE FROM events WHERE clicked_at < datetime('now', ?)",(f'-{int(retention_days)} days',))

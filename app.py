"""RUK AI CYBER TOOLS: consent-based link analytics dashboard."""
import secrets
from datetime import datetime, timezone
from urllib.parse import urlparse
from flask import Flask, abort, flash, redirect, render_template, request, url_for
import config, database
from modules.security import normalize_url
app=Flask(__name__); app.secret_key=config.SECRET_KEY; DB=config.DATABASE; database.init_db(DB)
def valid_destination(value):
    url=normalize_url(value); parsed=urlparse(url)
    if parsed.hostname in ("localhost","127.0.0.1","0.0.0.0","::1"): raise ValueError("Localhost destinations are not accepted for public links.")
    return url
@app.get("/")
def index():
    rows=database.dashboard_rows(DB); base=config.PUBLIC_BASE_URL or request.url_root.rstrip("/"); return render_template("index.html",rows=rows,base=base)
@app.post("/links")
def create():
    try:
        destination=valid_destination(request.form.get("destination","")); campaign=request.form.get("campaign","").strip()[:120]; link_id=secrets.token_urlsafe(7).replace('-','').replace('_','')[:10]
        database.create_link(DB,link_id,destination,campaign); flash("Link created. Visitors will see a privacy notice before optional analytics.","success")
    except ValueError as exc: flash(str(exc),"error")
    return redirect(url_for("index"))
@app.get("/l/<link_id>")
def landing(link_id):
    row=database.get_link(DB,link_id)
    if not row: abort(404)
    if row.get("expires_at"):
        try:
            if datetime.fromisoformat(row["expires_at"]) < datetime.now(timezone.utc): abort(410)
        except ValueError: pass
    return render_template("consent.html",link=row)
@app.post("/l/<link_id>/continue")
def continue_link(link_id):
    row=database.get_link(DB,link_id)
    if not row: abort(404)
    consent=request.form.get("analytics_consent")=="yes"; referrer_host=None
    if consent:
        ref=request.referrer or ""; referrer_host=urlparse(ref).hostname if ref else None
    database.record_event(DB,link_id,consented=consent,referrer_host=referrer_host); return redirect(row["destination"],code=302)
@app.post("/delete-all")
def clear_data():
    if request.remote_addr not in ("127.0.0.1","::1"): abort(403)
    database.delete_all(DB); flash("All links and analytics were deleted.","success"); return redirect(url_for("index"))
@app.get("/health")
def health(): return {"status":"ok","app":"RUK AI CYBER TOOLS"}
if __name__=="__main__": app.run(host=config.HOST,port=config.PORT,debug=False)

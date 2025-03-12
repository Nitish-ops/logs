from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import threading
from scheduler_logs.database import get_db, Log
from scheduler_logs.scheduler_service import setup_scheduler, run_scheduler

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():

    setup_scheduler()
    threading.Thread(target=run_scheduler, daemon=True).start()


@app.get("/logs", response_class=HTMLResponse)
def read_logs(request: Request, db: Session = Depends(get_db)):
    """API endpoint to retrieve and display the latest logs in HTML table with missing entry check."""
    logs = db.query(Log).order_by(Log.timestamp.desc()).limit(6).all()

    # Basic missing entry check (improve this as needed)
    entry_count = sum(1 for log in logs if log.log_type == "entry")
    exit_count = sum(1 for log in logs if log.log_type == "exit")

    missing_note = None
    if entry_count != exit_count:
        missing_note = "Warning: Possible missing entry or exit events!"

    return templates.TemplateResponse(
        "logs.html", {"request": request, "logs": logs, "missing_note": missing_note}
    )

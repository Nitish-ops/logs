import schedule
import time
import logging
import random  # Import random
from sqlalchemy.orm import Session
from scheduler_logs.database import get_db, Log, SessionLocal
from typing import Generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_logs():

    log_types = ["entry", "exit"]
    logs = []
    for i in range(random.randint(1, 5)):  # Create more logs
        log_type = random.choice(log_types) # Randomly assign entry/exit
        logs.append(f"Log entry {i}: This is a sample {log_type} log message at {time.strftime('%Y-%m-%d %H:%M:%S')},{log_type}")
    return logs


def store_logs_in_db():
    """Gets the logs and stores them in the database using SQLAlchemy."""
    logs = get_logs()
    if not logs:
        logging.info("No logs to store.")
        return

    db_session: Session = SessionLocal()
    try:
        for log_message in logs:
            parts = log_message.split(',')
            message = parts[0]
            log_type = parts[1]
            new_log = Log(log_message=message, log_type=log_type)
            db_session.add(new_log)
        db_session.commit()
        logging.info(f"Stored {len(logs)} logs in the database.")

    except Exception as e:
        logging.error(f"Error storing logs in database: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def run_scheduler():
    """Runs the schedule loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)


def setup_scheduler():
    """Configures and starts the scheduler."""
    schedule.every(2).minutes.do(store_logs_in_db)
    logging.info("Log storage scheduled every 2 minutes.")
from app import create_app
from app import db

from app.models import Task

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Task": Task
    }

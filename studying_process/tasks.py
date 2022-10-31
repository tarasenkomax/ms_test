from settings.celery import app


@app.task
def create_report():
    pass

from settings.celery import app
from studying_process.utils.excel_creator import ExcelFile


@app.task
def create_report():
    """ Создание .xlsx отчета администратора """
    excel = ExcelFile()
    excel.add_direction_of_training().add_groups().save_file()

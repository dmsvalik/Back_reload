from celery.app import shared_task

from app.file.methods.task_methods import TaskFile


@shared_task
def task_moving_files(relative_path: str, file_ids: list[int]) -> None:
    """
    Таска перемещает файлы из папки хранения временных файлов в папку объекта
    к которому привязан файл.
    @param relative_path:
    @param file_ids:
    @return:
    """
    files = TaskFile()
    files.moving_files_to_cloud(relative_path, file_ids)
    files.moving_file_to_server(relative_path, file_ids)

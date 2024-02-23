from celery.app import shared_task

from app.file.methods.task_methods import TaskFile
from app.file.models import IpFileModel


@shared_task
def task_moving_files(
    relative_path: str, file_ids: list[int], user_id: int
) -> None:
    """
    Таска перемещает файлы из папки хранения временных файлов в папку объекта
    к которому привязан файл.
    @param relative_path:
    @param file_ids:
    @param user_id:
    @return:
    """
    files = TaskFile(user_id)
    files.moving_files_to_cloud(relative_path, file_ids)
    files.moving_file_to_server(relative_path, file_ids)
    IpFileModel.objects.filter(file__id__in=file_ids).delete()


@shared_task
def task_delete_file(
    file_path: str, preview_path: str, user_id: int = None
) -> None:
    """
    Таска удаляет файлы с сервера и облака.
    @param file_path:
    @param preview_path:
    @param user_id:
    @return:
    """
    file = TaskFile(user_id)
    file.delete_file_from_server(preview_path)
    file.delete_file_from_cloud(file_path)

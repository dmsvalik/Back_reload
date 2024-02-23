from django.db.models.signals import post_save, pre_delete

from app.file.models import FileModel, FileToDelete


def delete_files(sender, instance, **kwargs):
    """Создание сигнала для удаления файла с сервера и облака."""
    FileToDelete.objects.create(
        file_path=instance.file_path, preview_path=instance.preview_path
    )


pre_delete.connect(delete_files, sender=FileModel)


def delete_if_empty(sender, instance, **kwargs):
    if instance.file_path == "" and instance.preview_path == "":
        instance.delete()


post_save.connect(delete_if_empty, sender=FileToDelete)

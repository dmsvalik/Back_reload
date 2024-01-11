class ErrorMessages:
    USER_NOT_FOUNDED = "Пользователь не найден."
    MAX_QUOTA_ERROR = "Пожалуйста освободите место удалив ненужные файлы."
    TOTAL_TRAFFIC_ERROR = (
        f"Доступный трафик закончился. Подождите следующего "
        f"месяца или свяжитесь с администратором."
    )
    UPLOADED_FILE_FIELD_ERROR = "Поле 'upload_file' не может быть пустым."
    UNSUPPORTED_FILE = "Недопустимый тип файла: {}."
    ORDER_LIMIT_ERROR = (
        f"Достигнут лимит количества заказов. Максимальное "
        f"количество - " + "{}."
    )

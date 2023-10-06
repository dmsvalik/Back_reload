from main_page.models import UserQuota


def recalculate_quota(user_account, cloud_size, server_size):
    """Пересчитываем квоту пользователя."""
    user_quota = UserQuota.objects.get(user=user_account)
    current_cloud_size = user_quota.total_cloud_size
    current_server_size = user_quota.total_server_size

    new_total_cloud_size = current_cloud_size + cloud_size
    new_total_server_size = current_server_size + server_size

    if new_total_cloud_size < 0:
        new_total_cloud_size = 0
    if new_total_server_size < 0:
        new_total_server_size = 0

    return UserQuota.objects.filter(user=user_account).update(
        total_cloud_size=new_total_cloud_size,
        total_server_size=new_total_server_size
    )

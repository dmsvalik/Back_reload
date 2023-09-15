from django.db import models
from main_page.models import UserAccount

class UserQuota(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    quota_cloud_size = models.PositiveIntegerField(default=0)
    total_server_size = models.PositiveIntegerField(default=0) 
    total_traffic = models.PositiveIntegerField(default=1000)  

    def reset_traffic(self):
        self.total_traffic = 0
        self.save()
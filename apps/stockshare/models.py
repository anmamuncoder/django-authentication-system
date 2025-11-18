from django.db import models
from apps.users.models import User
import uuid
# Create your models here. 

class ShareWith(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='shared_connections')
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='connected_with')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'shared_user')

    def __str__(self):
        return f"{self.owner.username} - {self.shared_user.username}"

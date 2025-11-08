from django.db import models
# Create your models here.
from .constants import SELECT_PRIORITY
from apps.users.models import User
import uuid

# --------------------------
# Base Model
# --------------------------
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# --------------------------
# Category Model
# --------------------------
class Category(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='categories',null=True)
    name = models.CharField(max_length=25,help_text='write category name here.')

    @property
    def inventory_count(self):
        return self.inventories.count() 
    
    def __str__(self):
        return self.name

# --------------------------
# Inventory Model
# --------------------------
class Inventory(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='inventories',null=True)
    name = models.CharField(max_length=150,help_text='write inventory name here.')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='inventories')
    priority = models.CharField(max_length=25,choices=SELECT_PRIORITY)
    date = models.DateField(auto_now_add=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.number} {self.name} - {self.priority}"


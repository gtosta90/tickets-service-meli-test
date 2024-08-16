import datetime
from uuid import uuid4
from django.db import models


class Category(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    name=models.CharField(max_length=100)
    display_name=models.CharField(max_length=50)
    relationship_id=models.CharField(max_length=40)
    created_at=models.DateTimeField(default=datetime.datetime.now)
    updated_at=models.DateTimeField(null=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table = "category"

    def __str__(self) -> str:
        return self.name
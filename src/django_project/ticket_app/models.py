import datetime
from uuid import uuid4
from django.db import models



class Ticket(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    title=models.CharField(max_length=100)
    user_create=models.IntegerField()
    category=models.UUIDField()
    subcategory=models.UUIDField(default=None, null=True)
    severity=models.IntegerField()
    description=models.CharField(max_length=1024)
    created_at=models.DateTimeField(default=datetime.datetime.now)
    updated_at=models.DateTimeField(null=True)
    user_assigned=models.IntegerField(null=True)
    status=models.CharField(max_length=40)
    
    class Meta:
        db_table = "tickets"

    def __str__(self) -> str:
        return self.title
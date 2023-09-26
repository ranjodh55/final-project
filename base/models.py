from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
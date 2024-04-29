from django.db import models

# Create your models here.


class RequestLog(models.Model):
    request_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
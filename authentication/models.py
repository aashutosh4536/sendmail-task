from django.db import models
from time import time

# Create your models here.
class Register(models.Model):
    user_email = models.EmailField(max_length=255   )
    
    def __str__(self):
        return self.user_email


class Response(models.Model):
    email = models.CharField(max_length=250)
    response = models.CharField(max_length=250)
    updated_on = models.IntegerField(editable=False,null=True,blank=True)
    created_on = models.IntegerField(editable=False,null=True,blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email',]),
            models.Index(fields=['updated_on',]),
            models.Index(fields=['created_on',]),
    ]

    def __str__(self):
        return str(f'{self.email}, {self.response}, {self.created_on}')
    
    def save(self,*args, **kwargs):
        if self.id is None:
            ct = int(time())
            self.created_on = ct
            self.updated_on = ct
        else:
            ct = int(time())
            self.updated_on = ct
        super().save(*args, **kwargs)
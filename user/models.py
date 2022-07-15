from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)

    def __str__(self):
        return self.user.username

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

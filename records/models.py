from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class FamilyModel(models.Model):
    name = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"{self.name} family in {self.zip_code}"

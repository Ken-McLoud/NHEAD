from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class FamilyModel(models.Model):
    name = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"{self.name} family in {self.zip_code}"


class KidModel(models.Model):
    family = models.ForeignKey(FamilyModel, on_delete=CASCADE)
    birth_year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    def __str__(self):
        yr = datetime.date.today().year - self.birth_year
        return f"{yr}yr old child in {self.family.name} family"

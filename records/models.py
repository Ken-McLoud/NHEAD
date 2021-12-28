from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class FamilyModel(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
    )
    zip_code = models.CharField(
        max_length=5,
        null=False,
    )
    user = models.ForeignKey(User, on_delete=PROTECT, null=False)

    def __str__(self):
        return f"{self.name} family in {self.zip_code}"


class KidModel(models.Model):
    genders = (("boy", "Boy"), ("girl", "Girl"))
    family = models.ForeignKey(FamilyModel, on_delete=PROTECT, null=False)
    birth_year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        null=False,
    )
    gender = models.CharField(max_length=10, choices=genders, null=True)

    @property
    def age(self):
        return datetime.date.today().year - self.birth_year

    def __str__(self):
        return f"{self.age}yr old child in {self.family.name} family"

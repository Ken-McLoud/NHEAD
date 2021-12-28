from django.contrib import admin
from .models import FamilyModel, KidModel

# Register your models here.
admin.site.register(FamilyModel)
admin.site.register(KidModel)

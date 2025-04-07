from django.contrib import admin # type: ignore
from .models import Dish

# Register your models here.
admin.site.register(Dish)
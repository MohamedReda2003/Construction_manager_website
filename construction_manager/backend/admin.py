from django.contrib import admin

# Register your models here.
from .models import ConstructionSite, Material

admin.site.register(ConstructionSite)
admin.site.register(Material)

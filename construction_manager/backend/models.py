from django.db import models

# Create your models here.
class ConstructionSite(models.Model):
    name = models.CharField(max_length=255)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    unit_price = models.FloatField()
    total_price = models.FloatField()
    n_bc = models.CharField(max_length=255)
    n_bl = models.CharField(max_length=255)
    entry_date = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=255)
    site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.description} in {self.site}"
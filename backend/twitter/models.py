from django.db import models


class Polygon(models.Model):
    name = models.CharField(unique=True, max_length=50)
    content = models.TextField()
    region = models.TextField()

    class Meta:
        managed = False
        db_table = 'polygon'

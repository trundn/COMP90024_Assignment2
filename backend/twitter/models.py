from django.db import models


class Polygon(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    region = models.TextField()

    class Meta:
        managed = False
        db_table = 'polygon'

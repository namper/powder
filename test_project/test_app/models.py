from django.db import models


class Simple(models.Model):
    """Simple model"""
    name = models.CharField(max_length=3)


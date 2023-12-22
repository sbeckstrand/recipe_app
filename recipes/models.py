# recipes/models.py

from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.JSONField()
    instructions = models.JSONField()
    information = models.JSONField()
    servings = models.TextField(null=True)
    prep_time = models.TextField(null=True)
    cook_time = models.TextField(null=True)
    cals_per_serving = models.IntegerField(null=True)
    source = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

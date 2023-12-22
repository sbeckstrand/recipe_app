# Generated by Django 4.2.7 on 2023-12-21 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_ingredients_alter_recipe_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cook_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='information',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='prep_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
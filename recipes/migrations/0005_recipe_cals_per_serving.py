# Generated by Django 4.2.7 on 2023-12-21 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_cook_time_alter_recipe_prep_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cals_per_serving',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

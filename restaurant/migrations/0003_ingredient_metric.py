# Generated by Django 4.1.4 on 2023-01-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_rename_ingredients_ingredient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='metric',
            field=models.CharField(choices=[('G', 'g'), ('ML', 'ml'), ('UNITS', 'units')], default='G', max_length=6),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-28 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('quantity_available', models.FloatField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeRequirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_needed', models.FloatField()),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.ingredients')),
                ('menu_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menuitems')),
            ],
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_purchase', models.DateTimeField()),
                ('bill', models.FloatField()),
                ('menu_item_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.menuitems')),
            ],
            options={
                'ordering': ['time_of_purchase'],
            },
        ),
    ]

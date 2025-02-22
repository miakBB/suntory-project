# Generated by Django 5.1.5 on 2025-02-01 18:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('volume', models.FloatField()),
                ('unit', models.FloatField()),
                ('kcal', models.FloatField()),
                ('caffeine', models.FloatField()),
                ('salt', models.FloatField()),
                ('sugars', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DrinkCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumed_at', models.DateTimeField()),
                ('quantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.drink')),
            ],
        ),
        migrations.AddField(
            model_name='drink',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.drinkcategory'),
        ),
    ]

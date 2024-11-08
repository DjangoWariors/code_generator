# Generated by Django 5.1.3 on 2024-11-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(blank=True, db_index=True, max_length=255, unique=True)),
                ('brand', models.CharField(max_length=20)),
            ],
        ),
    ]
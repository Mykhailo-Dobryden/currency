# Generated by Django 4.2.7 on 2023-12-05 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0009_alter_rate_currency_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestResponseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('path', models.CharField(max_length=255)),
                ('request_method', models.CharField(max_length=10)),
                ('time', models.DecimalField(decimal_places=7, max_digits=10)),
            ],
        ),
    ]

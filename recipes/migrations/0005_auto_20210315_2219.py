# Generated by Django 3.1.6 on 2021-03-15 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210313_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(help_text='Название ингредиента', max_length=200, unique=True, verbose_name='Название'),
        ),
    ]
# Generated by Django 3.1.6 on 2021-02-24 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_delete_favouriterecipe'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchases', '0002_purchaselist_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPurchaseList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.OneToOneField(help_text='Автор нового списка покупок', on_delete=django.db.models.deletion.CASCADE, related_name='new_purchase_list', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Новый список покупок',
                'verbose_name_plural': 'Новые списки покупок',
            },
        ),
        migrations.CreateModel(
            name='RecipeInNewPurchaseList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(help_text='Количество порций рецепта в новом списке покупок', verbose_name='Количество')),
                ('new_purchase_list', models.ForeignKey(help_text='Новый список покупок, в котором представлен рецепт', on_delete=django.db.models.deletion.CASCADE, to='purchases.newpurchaselist', verbose_name='Новый список покупок')),
                ('recipe', models.ForeignKey(help_text='Рецепт, представленный в новом списке покупок', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Рецепт в новом списке покупок',
                'verbose_name_plural': 'Рецепты в новых списках покупок',
            },
        ),
        migrations.AddField(
            model_name='newpurchaselist',
            name='recipes',
            field=models.ManyToManyField(help_text='Рецепты, представленные в новом списке покупок', related_name='new_purchase_lists', through='purchases.RecipeInNewPurchaseList', to='recipes.Recipe', verbose_name='Рецепты'),
        ),
        migrations.AddConstraint(
            model_name='recipeinnewpurchaselist',
            constraint=models.UniqueConstraint(fields=('new_purchase_list', 'recipe'), name='unique_new_purchase_list_recipe'),
        ),
    ]
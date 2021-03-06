# Generated by Django 3.1.6 on 2021-03-11 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_auto_20210310_2307'),
        ('users', '0003_auto_20210307_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeInPurchaseList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт, представленный в списке покупок пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='purchase_lists', to='recipes.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(help_text='Пользователь, который добавил рецепт в список покупок', on_delete=django.db.models.deletion.CASCADE, related_name='recipes_in_purchase_list', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рецепт в списке покупок',
                'verbose_name_plural': 'Рецепты в списках покупок',
            },
        ),
        migrations.AddConstraint(
            model_name='recipeinpurchaselist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_in_purchase_list'),
        ),
    ]

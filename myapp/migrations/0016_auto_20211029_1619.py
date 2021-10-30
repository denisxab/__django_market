# Generated by Django 3.2.8 on 2021-10-29 16:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20211029_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(db_column='Цена', help_text='Цена', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]
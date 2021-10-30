# Generated by Django 3.2.8 on 2021-10-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_product_name_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='data_create',
            field=models.DateField(auto_now_add=True, db_column='Дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='data_update',
            field=models.DateTimeField(auto_now=True, db_column='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='details_description',
            field=models.TextField(db_column='Полное описание', help_text='Полное описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_product',
            field=models.CharField(db_column='Имя товара', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='shot_description',
            field=models.CharField(db_column='Краткое описание', help_text='Краткое описание', max_length=200),
        ),
    ]

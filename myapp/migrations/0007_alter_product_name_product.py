# Generated by Django 3.2.8 on 2021-10-25 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_product_name_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name_product',
            field=models.CharField(db_column='Имя товара', max_length=200, verbose_name='Имя товара'),
        ),
    ]

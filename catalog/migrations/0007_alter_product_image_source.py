# Generated by Django 3.2.6 on 2021-11-08 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_product_image_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_source',
            field=models.CharField(blank=True, default='Nothing', max_length=600),
            preserve_default=False,
        ),
    ]
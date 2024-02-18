# Generated by Django 5.0.1 on 2024-02-18 19:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="createdAt",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.CharField(
                blank=True, default="Sample Product Brand", max_length=200, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                blank=True, default="Sample Product Category", max_length=200, null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                blank=True, default="Sample Product Description", null=True
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, default="/sample.jpg", null=True, upload_to=""
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                blank=True, default="Sample Product Name", max_length=200, null=True
            ),
        ),
    ]
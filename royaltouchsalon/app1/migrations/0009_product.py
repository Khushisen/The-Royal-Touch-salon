# Generated by Django 5.1.1 on 2024-11-15 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0008_remove_cart_product_remove_cart_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
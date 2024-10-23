# Generated by Django 5.0 on 2024-10-23 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pos", "0003_alter_sales_date"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OtherProducts",
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
                ("quantity", models.IntegerField()),
                ("price", models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name="sales",
            name="amount_bought",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="sales",
            name="amount_paid",
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name="OtherSales",
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
                ("customer", models.CharField(max_length=20)),
                ("phone", models.CharField(max_length=15)),
                ("amount_bought", models.FloatField()),
                ("amount_paid", models.FloatField()),
                ("payment_option", models.CharField(max_length=20)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pos.otherproducts",
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
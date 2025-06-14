# Generated by Django 5.2.1 on 2025-06-12 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageCategory",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "order",
                    models.IntegerField(
                        default=0, help_text="Order in TOC (lower = first)"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Page Categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.AlterModelOptions(
            name="page",
            options={"ordering": ["category__order", "toc_order", "title"]},
        ),
        migrations.AddField(
            model_name="page",
            name="show_in_toc",
            field=models.BooleanField(
                default=True, help_text="Show this page in the TOC"
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="toc_order",
            field=models.IntegerField(
                default=0, help_text="Order within category (lower = first)"
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="Category for TOC organization",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.pagecategory",
            ),
        ),
    ]

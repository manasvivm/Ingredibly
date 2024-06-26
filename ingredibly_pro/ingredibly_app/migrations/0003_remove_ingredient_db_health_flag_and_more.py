# Generated by Django 4.1.7 on 2023-02-26 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredibly_app', '0002_ingredient_db'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient_db',
            name='health_flag',
        ),
        migrations.AddField(
            model_name='ingredient_db',
            name='ingredient_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredient_db',
            name='allergen_flag',
            field=models.CharField(max_length=200),
        ),
    ]

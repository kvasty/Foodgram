# Generated by Django 4.2.2 on 2023-07-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_first_name_follow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
    ]

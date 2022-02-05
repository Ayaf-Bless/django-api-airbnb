# Generated by Django 4.0.2 on 2022-02-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_auto_20191216_0937'),
        ('users', '0003_alter_user_favs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(blank=True, null=True, related_name='favs', to='rooms.Room'),
        ),
    ]

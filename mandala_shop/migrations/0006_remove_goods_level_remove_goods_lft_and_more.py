# Generated by Django 4.0.5 on 2022-06-25 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mandala_shop', '0005_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='level',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='tree_id',
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandala_shop', '0004_remove_goods_parent_goods_ingredients_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150)),
                ('ingredients', models.ManyToManyField(blank=True, to='mandala_shop.test')),
            ],
        ),
    ]

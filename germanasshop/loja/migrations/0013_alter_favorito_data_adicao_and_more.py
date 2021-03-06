# Generated by Django 4.0.2 on 2022-03-30 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0012_alter_favorito_data_adicao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorito',
            name='data_adicao',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 28, 57, 904173), verbose_name='Data da Adição na lista'),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='id_favorito',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 28, 57, 903176), verbose_name='Data Pergunta'),
        ),
    ]

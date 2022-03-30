# Generated by Django 4.0.2 on 2022-03-30 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0013_alter_favorito_data_adicao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorito',
            name='data_adicao',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 30, 50, 836293), verbose_name='Data da Adição na lista'),
        ),
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 30, 50, 836293), verbose_name='Data Pergunta'),
        ),
    ]
# Generated by Django 4.0.3 on 2022-04-01 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0021_compras_alter_favorito_data_adicao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorito',
            name='data_adicao',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 16, 34, 16, 69602), verbose_name='Data da Adição na lista'),
        ),
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 16, 34, 16, 69602), verbose_name='Data Pergunta'),
        ),
        migrations.DeleteModel(
            name='CompraProduto',
        ),
        migrations.DeleteModel(
            name='Compras',
        ),
    ]
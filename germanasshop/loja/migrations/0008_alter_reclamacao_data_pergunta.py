# Generated by Django 4.0.3 on 2022-04-01 00:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0007_alter_reclamacao_data_pergunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 31, 21, 2, 5, 675147), verbose_name='Data Pergunta'),
        ),
    ]

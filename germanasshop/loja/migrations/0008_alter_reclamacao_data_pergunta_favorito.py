# Generated by Django 4.0.2 on 2022-03-30 12:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_usuario'),
        ('loja', '0007_alter_reclamacao_data_pergunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 18, 14, 342292), verbose_name='Data Pergunta'),
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id_favorito', models.CharField(default='<django.db.models.fields.related.ForeignKey><django.db.models.fields.related.ForeignKey>', max_length=100, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.produto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.usuario')),
            ],
        ),
    ]

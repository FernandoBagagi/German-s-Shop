# Generated by Django 4.0.2 on 2022-03-30 12:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_usuario'),
        ('loja', '0015_alter_reclamacao_data_pergunta_delete_favorito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamacao',
            name='data_pergunta',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 32, 18, 340046), verbose_name='Data Pergunta'),
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_adicao', models.DateTimeField(default=datetime.datetime(2022, 3, 30, 9, 32, 18, 341043), verbose_name='Data da Adição na lista')),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.produto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.usuario')),
            ],
        ),
    ]
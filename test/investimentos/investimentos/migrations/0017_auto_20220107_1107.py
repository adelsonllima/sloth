# Generated by Django 3.2.8 on 2022-01-07 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0016_auto_20220106_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pergunta',
            name='pre_requisito',
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='resposta_pre_requisito',
        ),
    ]

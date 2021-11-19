# Generated by Django 3.2.8 on 2021-11-17 11:50

from django.db import migrations, models
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0016_remove_ciclo_prioridades'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='finalizada',
            field=models.BooleanField(default=False, verbose_name='Finalizada'),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='teto',
            field=sloth.db.models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Limite de Investimento (R$)'),
        ),
    ]

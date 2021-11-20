# Generated by Django 3.2.8 on 2021-11-20 06:09

from django.db import migrations, models
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0019_auto_20211119_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='unidades_beneficiadas',
            field=models.ManyToManyField(blank=True, help_text='Não informar caso todas as unidades sejam beneficiadas.', to='investimentos.Campus', verbose_name='Unidades Beneficiadas'),
        ),
        migrations.AlterField(
            model_name='ciclo',
            name='teto',
            field=sloth.db.models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Limite de Investimento por Instituição (R$)'),
        ),
        migrations.AlterField(
            model_name='demanda',
            name='valor',
            field=sloth.db.models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Valor a Empenhar no Exercício (R$)'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='tipo_resposta',
            field=models.IntegerField(choices=[[1, 'Texto Curto'], [2, 'Texto Longo'], [3, 'Valor Monetário'], [4, 'Número Inteiro'], [5, 'Data'], [6, 'Sim/Não'], [7, 'Arquivo'], [8, 'Múltiplas Escolhas']], verbose_name='Tipo de Resposta'),
        ),
    ]

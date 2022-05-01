# Generated by Django 4.0.4 on 2022-05-01 18:15

from django.db import migrations
import sloth.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('simulado', '0008_agendamento_alter_pergunta_resposta_simulado_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agendamento',
            options={'verbose_name': 'Agendamento', 'verbose_name_plural': 'Agendamentos'},
        ),
        migrations.AlterModelOptions(
            name='simulado',
            options={'verbose_name': 'Simulado', 'verbose_name_plural': 'Simulado'},
        ),
        migrations.AlterField(
            model_name='resposta',
            name='resposta',
            field=sloth.db.models.CharField(max_length=255, null=True, verbose_name='Resposta'),
        ),
    ]

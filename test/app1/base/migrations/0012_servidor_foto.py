# Generated by Django 3.2.8 on 2021-11-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_setor_substitutos_eventuais'),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos', verbose_name='Foto'),
        ),
    ]

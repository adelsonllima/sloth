# Generated by Django 3.2.8 on 2021-11-05 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dms2', '0003_auto_20211105_0630'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='scope_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='role',
            name='scope_key',
            field=models.CharField(max_length=50, null=True, verbose_name='Escopo'),
        ),
    ]

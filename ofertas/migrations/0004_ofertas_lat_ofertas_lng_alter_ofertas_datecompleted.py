# Generated by Django 4.2.4 on 2023-11-01 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0003_ofertas_datecompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertas',
            name='lat',
            field=models.FloatField(default=0.0, verbose_name='Latitud'),
        ),
        migrations.AddField(
            model_name='ofertas',
            name='lng',
            field=models.FloatField(default=0.0, verbose_name='Longitud'),
        ),
        migrations.AlterField(
            model_name='ofertas',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0004_alter_ofertas_datecompleted_alter_ofertas_id_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rating',
        ),
        migrations.AddField(
            model_name='rating',
            name='improvement_suggestions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='overall_experience',
            field=models.PositiveIntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='would_use_again',
            field=models.CharField(default=2, max_length=3),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-05 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_remove_participants_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresult',
            name='industry',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

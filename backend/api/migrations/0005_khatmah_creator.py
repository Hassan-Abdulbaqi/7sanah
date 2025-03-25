# Generated by Django 4.2.20 on 2025-03-25 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_khatmah_khatmah_type_surahassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='khatmah',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_khatmahs', to='api.participant'),
        ),
    ]

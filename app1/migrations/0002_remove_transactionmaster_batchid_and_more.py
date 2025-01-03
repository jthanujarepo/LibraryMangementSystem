# Generated by Django 5.0.6 on 2024-12-08 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionmaster',
            name='batchID',
        ),
        migrations.AddField(
            model_name='transactionmaster',
            name='batchId',
            field=models.CharField(choices=[(' ', 'Select_Batch'), ('2020-2022', '2020-2022'), ('2021-2023', '2021-2023'), ('2022-2024', '2022-2024'), ('2023-2025', '2023-2025'), ('2024-2025', '2024-2025'), ('2025-2027', '2025-2027'), ('2026-2028', '2026-2028'), ('2027-2029', '2027-2029'), ('2028-2030', '2028-2030')], default=' ', max_length=10, unique=True),
        ),
    ]
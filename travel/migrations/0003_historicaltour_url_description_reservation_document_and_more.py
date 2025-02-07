# Generated by Django 4.2.16 on 2025-01-19 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_alter_reservation_date_reservation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltour',
            name='url_description',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на описание тура'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='reservation_documents/', verbose_name='Документ бронирования'),
        ),
        migrations.AddField(
            model_name='tour',
            name='url_description',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на описание тура'),
        ),
    ]

# Generated by Django 4.2.16 on 2025-01-20 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_remove_historicaltour_url_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
        migrations.AlterModelOptions(
            name='historicaltour',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Тур', 'verbose_name_plural': 'historical Туры'},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'verbose_name': 'Бронирование', 'verbose_name_plural': 'Бронирования'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Акция', 'verbose_name_plural': 'Акции'},
        ),
        migrations.AlterModelOptions(
            name='tour',
            options={'ordering': ['date_departure'], 'verbose_name': 'Тур', 'verbose_name_plural': 'Туры'},
        ),
        migrations.AlterModelOptions(
            name='travelhistory',
            options={'verbose_name': 'История путешествий', 'verbose_name_plural': 'Истории путешествий'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-01-20', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(related_name='favorited_by', through='travel.Favorite', to='travel.tour', verbose_name='Избранные туры'),
        ),
    ]

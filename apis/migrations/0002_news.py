# Generated by Django 3.0.8 on 2021-02-27 17:03

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headline', models.CharField(max_length=500)),
                ('description', ckeditor.fields.RichTextField()),
                ('views', models.IntegerField(default=0)),
                ('sub_category', models.CharField(choices=[('National', 'National'), ('International', 'International')], default='National', max_length=20)),
                ('image', models.ImageField(upload_to='website/news')),
                ('credit', models.CharField(blank=True, max_length=30, null=True)),
                ('posted_date', models.DateField(default=django.utils.timezone.now)),
                ('time_to_read', models.IntegerField(default=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='apis.Category')),
            ],
        ),
    ]

# Generated by Django 3.0.8 on 2021-04-28 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_polloptions_votingpoll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='ads')),
                ('page', models.CharField(choices=[('Header', 'Header'), ('Side Bar', 'Side Bar')], default='Home Page', max_length=20)),
                ('location', models.CharField(choices=[('H-970*90', 'H-970*90'), ('S-150*150', 'S-150*150')], max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('url_link', models.CharField(default='#', max_length=1000)),
            ],
        ),
    ]

# Generated by Django 3.1.5 on 2021-04-14 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210414_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.IntegerField()),
                ('subject', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=30)),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-14 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_text', models.TextField(blank=True, null=True)),
                ('n_players', models.IntegerField(verbose_name='number of players')),
                ('duration', models.IntegerField()),
                ('difficulty', models.CharField(choices=[(1, 'Very Easy'), (2, 'Easy'), (3, 'Normal'), (4, 'Hard'), (5, 'Very Hard')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('publisher', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
                ('category', models.ManyToManyField(to='game.category')),
                ('description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.description')),
            ],
        ),
    ]

# Generated by Django 2.2.16 on 2022-07-27 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenresTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Genres')),
            ],
        ),
        migrations.RemoveField(
            model_name='categories',
            name='category',
        ),
        migrations.AddField(
            model_name='categories',
            name='name',
            field=models.CharField(default='name to enter', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categories',
            name='slug',
            field=models.SlugField(default='1', unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('year', models.IntegerField()),
                ('description', models.TextField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='titles', to='reviews.Categories')),
                ('genres', models.ManyToManyField(through='reviews.GenresTitle', to='reviews.Genres')),
            ],
        ),
        migrations.AddField(
            model_name='genrestitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Titles'),
        ),
    ]

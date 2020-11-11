# Generated by Django 3.1.2 on 2020-11-03 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='content',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=240)),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='liked_blogs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

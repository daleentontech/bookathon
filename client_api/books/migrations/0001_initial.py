# Generated by Django 3.0.2 on 2022-02-09 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('fiction', 'fiction'), ('technology', 'technology'), ('science', 'science'), ('other', 'other')], max_length=20)),
                ('publisher', models.CharField(max_length=255)),
                ('is_borrowed', models.BooleanField(default=False)),
                ('days_to_borrow', models.PositiveIntegerField(default=0)),
                ('borrowed_on', models.DateTimeField(blank=True, null=True)),
                ('available_on', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

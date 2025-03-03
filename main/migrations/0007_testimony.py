# Generated by Django 4.2.9 on 2024-01-22 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_delete_testimony'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('video', models.FileField(upload_to='media/image/')),
                ('picture', models.FileField(upload_to='media/picture/')),
                ('student_name', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
    ]

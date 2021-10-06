# Generated by Django 3.2.6 on 2021-10-27 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('uploaded_file', models.FileField(upload_to='uploads/')),
                ('thumbnail_image', models.ImageField(default='default.jpg', upload_to='thumbnail_images')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_type', models.IntegerField(choices=[(1, 'Ebook'), (2, 'Video'), (3, 'Music'), (4, 'Image'), (0, 'Other')], default=0)),
                ('is_private', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('comment_date_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='posts.post')),
            ],
        ),
    ]

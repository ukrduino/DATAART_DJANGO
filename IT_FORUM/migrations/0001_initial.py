# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_FORUM.Category')),
            ],
            options={
                'verbose_name_plural': 'Thread categories',
                'db_table': 'category',
                'verbose_name': 'Thread category',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_author', models.CharField(blank=True, max_length=250, verbose_name='Your name')),
                ('reply_author_email', models.EmailField(blank=True, max_length=254, verbose_name='Your e-mail')),
                ('reply_text', models.TextField(verbose_name='Reply text')),
                ('reply_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('reply_to_reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies_to_this', to='IT_FORUM.Reply')),
            ],
            options={
                'verbose_name_plural': 'Replies',
                'db_table': 'reply',
                'verbose_name': 'Reply',
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_author', models.CharField(blank=True, max_length=250, verbose_name='Your name')),
                ('thread_author_email', models.EmailField(blank=True, max_length=254, verbose_name='Your e-mail')),
                ('thread_title', models.CharField(max_length=250, unique=True, verbose_name='Thread title')),
                ('thread_text', models.TextField(verbose_name='Thread description')),
                ('thread_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('thread_change_date', models.DateTimeField(auto_now=True, verbose_name='Changed')),
                ('thread_image', models.FileField(default='static/site_images/ImageNot.jpg', max_length=1024, upload_to='')),
                ('thread_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IT_FORUM.Category')),
            ],
            options={
                'verbose_name_plural': 'Threads',
                'db_table': 'thread',
                'verbose_name': 'Thread',
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='reply_to_thread',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_FORUM.Thread'),
        ),
    ]
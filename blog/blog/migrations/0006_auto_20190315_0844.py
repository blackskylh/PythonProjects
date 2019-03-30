# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20150616_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='qq',
        ),
        migrations.RemoveField(
            model_name='user',
            name='url',
        ),
        migrations.AlterField(
            model_name='ad',
            name='callback_url',
            field=models.URLField(verbose_name='回调url', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.CharField(verbose_name='广告描述', max_length=200),
        ),
        migrations.AlterField(
            model_name='ad',
            name='image_url',
            field=models.ImageField(verbose_name='图片路径', upload_to='ad/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='index',
            field=models.IntegerField(verbose_name='排列顺序(从小到大)', default=999),
        ),
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.CharField(verbose_name='广告标题', max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='分类', blank=True, null=True, to='blog.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='click_count',
            field=models.IntegerField(verbose_name='点击次数', default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.CharField(verbose_name='文章描述', max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(verbose_name='是否推荐', default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(verbose_name='标签', to='blog.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(verbose_name='文章标题', max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='index',
            field=models.IntegerField(verbose_name='分类的排序', default=999),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(verbose_name='分类名称', max_length=30),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(verbose_name='文章', blank=True, null=True, to='blog.Article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(verbose_name='父级评论', blank=True, null=True, to='blog.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(verbose_name='用户', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(verbose_name='用户名', max_length=30, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='callback_url',
            field=models.URLField(verbose_name='url地址'),
        ),
        migrations.AlterField(
            model_name='links',
            name='date_publish',
            field=models.DateTimeField(verbose_name='发布时间', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='description',
            field=models.CharField(verbose_name='友情链接描述', max_length=200),
        ),
        migrations.AlterField(
            model_name='links',
            name='index',
            field=models.IntegerField(verbose_name='排列顺序(从小到大)', default=999),
        ),
        migrations.AlterField(
            model_name='links',
            name='title',
            field=models.CharField(verbose_name='标题', max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(verbose_name='标签名称', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(verbose_name='用户头像', max_length=200, blank=True, null=True, default='avatar/default.png', upload_to='avatar/%Y/%m'),
        ),
    ]

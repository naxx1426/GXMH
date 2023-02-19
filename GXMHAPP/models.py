from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class UserInfo(models.Model):
    portrait = models.ImageField(upload_to='portrait', default='portrait.jpg', verbose_name='头像')
    user_name = models.CharField(max_length=32, verbose_name='用户名')
    account = models.CharField(max_length=32, verbose_name='账号', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    region = models.CharField(max_length=32, verbose_name='地区')

    class Meta:
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.account
    # 用户信息


class Mailbox(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='用户')
    mailbox = models.CharField(max_length=32, verbose_name='邮箱')
    class Meta:
        verbose_name_plural = '用户邮箱'

    def __str__(self):
        return self.userinfo.account
    # 用户邮箱


class School(models.Model):
    school = models.CharField(max_length=32, verbose_name='学校')

    class Meta:
        verbose_name_plural = '学校信息'

    def __str__(self):
        return self.school
    # 学校信息


class MH_PersonalDetail(models.Model):
    cover = RichTextUploadingField(verbose_name="封面")
    name = models.CharField(max_length=32, verbose_name='姓名')
    gender = models.CharField(max_length=2, verbose_name='性别', choices=(('1', '男'), ('2', '女')))
    age = models.CharField(max_length=32, verbose_name='年龄')
    region = models.CharField(max_length=32, verbose_name='地区')
    school = models.ForeignKey('School', on_delete=models.CASCADE, verbose_name='学校')
    contact = models.CharField(max_length=32, verbose_name='联系方式')
    introduction = RichTextUploadingField(verbose_name='个人简介')
    user_collection = models.ManyToManyField(UserInfo, related_name='mh_personal_detail')

    class Meta:
        verbose_name_plural = '盲盒信息'

    def __str__(self):
        return "来自" + self.school.school + "的" + self.name
    # 盲盒信息


class Comment(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='昵称')
    mh = models.ForeignKey('MH_PersonalDetail', on_delete=models.CASCADE, verbose_name='盲盒')
    comment = RichTextUploadingField(verbose_name='评论', config_name='comment')

    class Meta:
        verbose_name_plural = '评论'

    def __str__(self):
        return "来自" + self.userinfo.account + "对来自" + self.mh.school.school + "的" + self.mh.name + "的评论"
    # 评论


class Comment_comment(models.Model):
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='昵称')
    post = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name='盲盒评论')
    comment = RichTextUploadingField(verbose_name='评论的评论', config_name='comment')

    class Meta:
        verbose_name_plural = '评论的评论'

    def __str__(self):
        return "来自" + self.userinfo.account + "对来自" + self.post.userinfo.account + "所评论的内容的评论"
    # 评论的评论

from django.contrib import admin
from .models import UserInfo, Mailbox, School, MH_PersonalDetail, Comment, Comment_comment


# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["user_name", "account"]
    list_per_page = 30


class MailboxAdmin(admin.ModelAdmin):
    list_display = ["userinfo", "mailbox"]
    list_per_page = 30


class SchoolAdmin(admin.ModelAdmin):
    list_display = ["school"]
    list_per_page = 30


class MH_PersonalDetailAdmin(admin.ModelAdmin):
    list_display = ["name", "gender", "age", "region", "school"]
    list_per_page = 30


class CommentAdmin(admin.ModelAdmin):
    list_display = ["mh", "userinfo"]
    list_per_page = 30


class Comment_commentAdmin(admin.ModelAdmin):
    list_display = ["post", "userinfo"]
    list_per_page = 30




admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(MH_PersonalDetail, MH_PersonalDetailAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Comment_comment, Comment_commentAdmin)

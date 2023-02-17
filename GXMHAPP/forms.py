from django import forms
from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import MH_PersonalDetail


class MH_PersonalDetail_AdminForm(forms.ModelForm):
    cover = RichTextUploadingFormField(widget=CKEditorUploadingWidget, label="封面", required=True)
    name = forms.CharField(max_length=32, label='姓名', required=True)
    gender = forms.ChoiceField(label='性别', required=True, choices=(('1', '男'), ('2', '女')))
    age = forms.CharField(max_length=32, label='年龄', required=True)
    region = forms.CharField(max_length=32, label='地区', required=True)
    contact = forms.CharField(max_length=32, label='联系方式', required=True)
    introduction = RichTextUploadingFormField(widget=CKEditorUploadingWidget, label='个人简介', required=True,
                                              config_name="default")

    class Meta:
        model = MH_PersonalDetail
        fields = "__all__"

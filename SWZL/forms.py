from django import forms
from django.core.exceptions import ValidationError

from SWZL import models


# 基类
class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# 招领form
class RecruitForm(BaseForm):
    class Meta:
        model = models.Recruit
        exclude = ['status', ]
        widgets = {'lost_time': forms.widgets.SelectDateWidget}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.instance.announcer.name)
        self.fields['announcer'].widget.choices = [(self.instance.announcer.id,self.instance.announcer.name,)]


# 注册form
class RegisterForm(BaseForm):
    confirm_password = forms.CharField(
        label='确认密码:',
        widget=forms.widgets.PasswordInput(),
        error_messages={"required": "请再次填写密码", }
    )

    class Meta:
        model = models.UserProfile
        fields = ['username', 'password', 'confirm_password', 'name']
        widgets = {'password': forms.widgets.PasswordInput}
        labels = {'password': '密码:', }
        error_messages = {'username': {"required": "用户名不能为空", "invalid": "格式错误,请输入邮箱格式", },
                          'password': {"required": "密码不能为空", },
                          'name': {"required": "名字不能为空", },
                          }

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('confirm_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('confirm_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')

import datetime
from django.db import models
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe
from django.urls import reverse

message_status_choices = (('unreviewed', "未审核"),
                          ('finding', "寻找中"),
                          ('found', '已找到'),
                          )
item_type = (
    ('wallet', "钱包"),
    ('key', "钥匙"),
    ('card', "卡类/证照"),
    ('electric', "数码产品"),
    ('bag', "手袋/挎包"),
    ('clothes', "衣服/鞋帽"),
    ('book', "书籍/文件"),
    ('others', "其它"),)


# 寻物信息
class Recruit(models.Model):
    title = models.CharField('信息标题:', max_length=32)
    lost_type = models.CharField('失物类别:', max_length=32, default='choice', choices=item_type)
    pub_time = models.DateTimeField("发布的时间:", auto_now=True
                                    )
    lost_time = models.CharField('丢失时间:', max_length=64)
    lost_place = models.CharField('丢失的地点', max_length=64)
    status = models.CharField('信息的状态:', choices=message_status_choices, default='unreviewed', max_length=32)

    detailed_description = models.TextField('详细描述:', null=True, blank=True)
    item_image = models.ImageField('物品图片:', null=True, blank=True, upload_to='image')
    contact = models.CharField('联系人', null=True, blank=True, max_length=64)
    qq = models.IntegerField('QQ', )
    email = models.EmailField('邮箱')
    address = models.CharField('联系地址', max_length=64)
    announcer = models.ForeignKey(to='UserProfile',default=1,verbose_name='发布者')

    def show_time(self):
        tem_time = datetime.datetime.now() - self.pub_time
        if tem_time.days:
            return '{} 天前'.format(tem_time.days)
        elif tem_time.seconds <= 3600:
            minute = tem_time.seconds // 60
            return '{} 分钟前'.format(minute)
        elif tem_time.seconds > 3600:
            hour = tem_time.seconds // 3600
            return '{} 小时前'.format(hour)


# 招领信息
class Recruitment(models.Model):
    title = models.CharField('信息标题:', max_length=32)
    lost_type = models.CharField('拾取类别:', max_length=32, default='choice', choices=item_type)
    pub_time = models.DateTimeField("发布的时间:", auto_now=True
                                    )
    lost_time = models.CharField('拾取时间:', max_length=64)
    lost_place = models.CharField('拾取的地点', max_length=64)
    status = models.CharField('信息的状态:', choices=message_status_choices, default='unreviewed', max_length=32)
    is_recruitment = models.BooleanField(default=True)
    detailed_description = models.TextField('详细描述:', null=True, blank=True)
    item_image = models.ImageField('物品图片:', null=True, blank=True, upload_to='image')
    contact = models.CharField('联系人', null=True, blank=True, max_length=64)
    qq = models.IntegerField('QQ', )
    email = models.EmailField('邮箱')
    address = models.CharField('联系地址', max_length=64)
    announcer = models.ForeignKey(to='UserProfile',default=1,verbose_name='发布者')

    def show_time(self):
        tem_time = datetime.datetime.now() - self.pub_time
        if tem_time.days:
            return '{} 天前'.format(tem_time.days)
        elif tem_time.seconds <= 3600:
            minute = tem_time.seconds // 60
            return '{} 分钟前'.format(minute)
        elif tem_time.seconds > 3600:
            hour = tem_time.seconds // 3600
            return '{} 小时前'.format(hour)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='用户名:'
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_admin = models.BooleanField(default=False)
    name = models.CharField('名字:', max_length=32)
    mobile = models.CharField('手机:', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('备注:', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always

        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        #     "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        #     "Does the user have permissions to view the app `app_label`?"
        #     Simplest possible answer: Yes, always
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    objects = UserManager()

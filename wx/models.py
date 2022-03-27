from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("lack of userName")
        if not password:
            raise ValueError("lack of password")
        user = self.model(username=username, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)


# 重写User模型，并设为系统默认User模型
class TcUser(AbstractBaseUser, PermissionsMixin):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    is_staff = models.BooleanField(verbose_name="是否是员工", default=False)
    is_superuser = models.BooleanField(verbose_name="是否是超级管理员", default=False)
    USERNAME_FIELD = 'username'
    # PASSWORD_FIELD = 'password'
    objects = UserManager()  # 使用自定义的模板创建方法

    # 后台查看字段信息时，将按下面你的json格式显示
    def to_dict(self):
        return {
            'user_id': self.userId,
            'user_name': self.username,
        }

    def __str__(self):
        return str(self.to_dict())

    class Meta:
        db_table = "userInfo"


class TcCate(models.Model):
    tc_id = models.IntegerField(primary_key=True)  # 后续录入
    tc_parent_id = models.IntegerField(null=True)
    tc_name = models.CharField(max_length=64)

    def to_dict(self):
        return {
            'trash_id': self.tc_id,
            'trash_parent_id': self.tc_parent_id,
            'trash_name': self.tc_name
        }

    def __str__(self):
        return str(self.to_dict())

    class Meta:
        db_table = "trashCate"


class TcSearch(models.Model):
    sea_info = models.CharField(primary_key=True, max_length=255)
    sea_user = models.ForeignKey(TcUser, on_delete=models.CASCADE, null=True)
    sea_cate = models.ForeignKey(TcCate, on_delete=models.CASCADE, null=True)
    sea_time = models.DateTimeField(default=timezone.now)
    sea_way = models.CharField(default='0', max_length=2)

    def to_dict(self):
        return {
            'search_info': self.sea_info,
            'search_user_id': self.sea_user.userId,
            'search_category': self.sea_cate.tc_name,
            'search_time': self.sea_time,
            'way': self.sea_way
        }

    def __str__(self):
        return str(self.to_dict())

    class Meta:
        db_table = "seaInfo"
        ordering = ['-sea_time']

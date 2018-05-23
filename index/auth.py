# -*- coding:utf-8 -*-

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,Group,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise  ValueError("用户名必须是邮箱地址")
        user = self.model(
                email=self.normalize_email(email),
                name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password):
        user = self.create_user(email,
                                password=password,
                                name=name,
                                )

        user.is_superuser = True
        user.save(using=self._db)
        return user


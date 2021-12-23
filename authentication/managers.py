# shop_drf > authentication > managers.py
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    # All user
    def create_user(self, username, email, password=None, **extra_fields):
    
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')
    
        user = self.model(
        username = username,
        # 중복 최소화를 위한 정규화
        email=self.normalize_email(email),
        **extra_fields
        )

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()
        
        return user

    # admin user
    def create_superuser(self, username, email, password, **extra_fields):
        
        if password is None:
            raise TypeError('Superuser must have a password.')
        
        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(username, email, password, **extra_fields)
        # 관리자로 지정
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user

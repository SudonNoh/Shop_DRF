# shop_drf > authentication > models.py
import jwt
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import UserManager
from core.models import TimestampedModel


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(max_length=13) #010-9999-9999
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = [
        'username',
        'phone_number'
    ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
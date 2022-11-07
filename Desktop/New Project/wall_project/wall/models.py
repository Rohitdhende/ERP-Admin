from django.db import models
import os
import sys
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.conf import settings


class RegisterUser(models.Model):
    upload_limit = [
        (102400, '100 MB'),
        (204800, '200 MB'),
        (409600, '400 MB'),
        (614400, '600 MB'),
        (819200, '800 MB'),    
        (1048576, '1GB'),
        (2097152, '2GB'),
        (3145728, '3GB'),
        (4194304, '4GB'),
        (5242880, '5GB'),
    ]
    user_id      = models.CharField(max_length=255,blank=True)
    password     = models.CharField(max_length=255,blank=True)
    email        = models.CharField(max_length=255,blank=True)
    token        = models.CharField(max_length=300,blank =True)
    active_email = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255,blank=True)
    mobile_number = models.IntegerField(blank=True, null=True)
    
    def verify_password(self,password):
        return pbkdf2_sha256.verify(password,self.password)

    def __str__(self):
        return self.user_id
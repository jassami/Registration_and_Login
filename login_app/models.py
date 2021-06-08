from django.db import models
import re
from datetime import datetime, timedelta
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['firstname']= "First name must be at least 2 characters."
        if len(post_data['last_name']) < 2:
            errors['lastname']= "Last name must be at least 2 characters."
        if len(post_data['birthday']) == 0:
            errors['bd']= "Birthday must be mm/dd/yyy."
        if len(post_data['birthday']) != 0:
            if datetime.strptime(post_data['birthday'], "%Y-%m-%d")> datetime.today():
                errors['bd_input']= "Birthday can't be in the future."
            user_bd= datetime.strptime(post_data['birthday'], "%Y-%m-%d")
            x= datetime.now() - timedelta(weeks=52*13)
            if user_bd > x and user_bd < datetime.now():
                errors['bday_input']= "Users under 13 can't register."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address."
        check_email= User.objects.filter(email= post_data['email'])
        if check_email:
            errors['email_input']= "This email address already exists."
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters."
        if post_data['confirm_pw'] != post_data['password']:
            errors['confirm_pw']= "Passwords don't match."
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['log_email'] = "Invalid email address."
            return errors
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters."
        user= User.objects.filter(email=post_data['email'])
        if user:
            user= user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['log_password']= "Incorrect email or password."
        else:
            errors['log_email_password']= "Incorrect email or password."
        return errors


class User(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    birthday= models.DateTimeField()
    email= models.CharField(max_length=100)
    password= models.CharField(max_length=60)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()

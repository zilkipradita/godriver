from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django.utils import timezone

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

class Users_roles(models.Model):
    name = models.CharField(max_length=20, blank=False, default='')

class Users(models.Model):
    username = models.CharField(max_length=20, blank=False, unique=True, default='',
                            validators=[
                                    MinLengthValidator(5),
                                    alphanumeric
                                    ]
    )
    password = models.CharField(max_length=100, blank=False, default='',
                            validators=[
                                    MinLengthValidator(5)
                                    ]
    )
    name = models.CharField(max_length=35, blank=False, default='',
                            validators=[
                                    MinLengthValidator(5)
                                    ]
    )
    telp = models.CharField(max_length=20, blank=False, default='',
                            validators=[
                                    numeric
                                    ]
    )
    email = models.CharField(max_length=30, blank=False, unique=True, default='',
                            validators=[
                                    validate_email
                                    ]
    )
    users_roles=models.ForeignKey(Users_roles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Trips(models.Model):
    destination = models.CharField(max_length=100, blank=False, default='',
                            validators=[
                                    alphanumeric
                                    ]
    )
    location = models.CharField(max_length=100, blank=False, default='',
                            validators=[
                                    alphanumeric
                                    ]
    )
    cost = models.DecimalField(max_digits=19, decimal_places=2, blank=False, default='0')
    status = models.CharField(max_length=20, blank=False, default='available')
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order_trips(models.Model):
    trips = models.ForeignKey(Trips, on_delete=models.CASCADE)
    driver = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

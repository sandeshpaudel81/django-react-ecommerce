from django.db.models.signals import pre_save # pre_save signal executes some code before the object gets saved to the database
from django.contrib.auth.models import User

# function that is executed before the object of User model gets saved to the database
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email

pre_save.connect(updateUser, sender=User)

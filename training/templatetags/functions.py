import re
from django import template
from django.contrib.auth.models import User

register= template.Library()

def getInitials(user_id):
   user = User.object.get(id=user_id)
   initials = user.first_name[0].upper()+user.last_name[0].upper()
   return initials
 
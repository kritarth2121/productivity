from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from blog.models import Team 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    goal=models.CharField(max_length=1000)
    role=models.CharField(max_length=100)
    team=models.ForeignKey(Team,on_delete=models.CASCADE,blank=True, null=True)
    last_time_logout=models.DateTimeField(blank=True, null=True)
    '''def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args,**kwargs):
        super().save( *args,**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    '''


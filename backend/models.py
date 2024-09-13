from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from backend.manager import CustomerUserManager


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class GenderedImageField(models.ImageField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance,add)
        if not value or not hasattr(model_instance,self.attname):

            gender = model_instance.gender if hasattr(model_instance,'gender')else Gender.MALE

            if gender == Gender.MALE:
                value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                 value = 'profile/female_avatar.png'
            else:
                 value = 'profile/default_image.jpg'

        elif model_instance.gender != getattr(model_instance,f"{self.attname}_gender_cache",None):
            gender = model_instance.gender
            if gender == Gender.MALE:
               value = 'profile/male_avatar.png'
            elif gender == Gender.FEMALE:
                value = 'profile/female_avatar.png'
            else:
                value = 'profile/default_image.jpg'
        setattr(model_instance,f"{self.attname}_gender_cache",model_instance.gender)
        return value

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)
    gender = models.CharField(max_length=1,choices=Gender.choices,default=Gender.MALE)
    image = GenderedImageField(upload_to='profile/',blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['gender']
    objects = CustomerUserManager()

    def __str__(self):
        return self.email

class NewsLetterStatus(models.TextChoices):
    SUBSCRIBE = 'SUBSCRIBE', _('SUBSCRIBE')
    UNSUBSCRIBE = 'UNSUBSCRIBE', _('UNSUBSCRIBE')

class NewsLetter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email =models.EmailField(_('email address'), unique=True)
    status= models.CharField(
        max_length=255,
        choices=NewsLetterStatus.choices,
        default=NewsLetterStatus.SUBSCRIBE
    )
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'news_letter'

class LabelStatus(models.TextChoices):
    PROCESSING = 'PROCESSING', _('PROCESSING')
    ACTIVE = 'ACTIVE', _('ACTIVE')
    HIDE = 'HIDE', _('HIDE')

class Label(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255,null=True, blank=True)
    status= models.CharField(
        max_length=255,
        choices=LabelStatus.choices,
        default=LabelStatus.PROCESSING
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'label'
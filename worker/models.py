from Tools.scripts.dutree import display
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.loader import get_template
from django.contrib.admin.decorators import display
from django.urls import reverse

GENDERS = (
        (None, 'Выберите пол'),
        ('M', 'Мужчина'),
        ('F', 'Женщина')
    )


class CustomUser(AbstractUser):
    client_group = Group.objects.get_or_create(name='Заказчик')
    executor_group = Group.objects.get_or_create(name='Исполнитель')
    gender = models.CharField('Пол', max_length=1, choices=GENDERS, default='', blank=True, null=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures/%Y/%m/%d', help_text='150x150px', verbose_name='Ссылка картинки', null=True, max_length=200)

    def __str__(self):
        return self.username

    def admin_image(self):
        if self.profile_picture:
            return u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.profile_picture.url)
        else:
            return '(Нет изображения)'
    admin_image.short_description = 'Картинка'
    admin_image.allow_tags = True

@receiver(pre_delete, sender=CustomUser)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.profile_picture.delete(False)
# Create your models here.

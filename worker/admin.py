from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from worker.models import CustomUser


@admin.register(CustomUser)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_image',)


    def get_image(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src={obj.profile_picture.url} width="100"')
        else:
            return mark_safe('Нет изображения')

    get_image.short_description = "Image"

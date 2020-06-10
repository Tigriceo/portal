from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, verbose_name="Имя пользователя", on_delete=models.CASCADE)
    description = models.TextField("Описание", blank=True, max_length=5000)
    avatar = models.ImageField("Фото", default='nophoto.png', upload_to='profile_photo')
    phone_number = models.CharField("Телефон", max_length=17, blank=True, null=True, unique=True)
    balance = models.FloatField("Баланс", default=0.00)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        # обрезаем фото
        super().save()

        image = Image.open(self.avatar.path)

        if image.height > 64 or image.width > 64:
            resize = (500, 500)
            image.thumbnail(resize)
            image.save(self.avatar.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance, phone_number=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    # def save(self, *args, **kwargs):
#     #     super().save()
#     #
#     #     image = Image.open(self.photo.path)
#     #
#     #     if image.height > 64 or image.width > 64:
#     #         resize = (256, 256)
#     #         image.thumbnail(resize)
#     #         image.save(self.photo.path)
#

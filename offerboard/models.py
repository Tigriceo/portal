from PIL import Image

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from offerboard.gen_slug import gen_slug


class AbstractField(models.Model):
    """Общие - дополнительные поля"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Url-адрес", max_length=100)
    description = models.TextField("Описание", null=True, max_length=5000)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(MPTTModel, AbstractField):
    """Категории"""
    parent = TreeForeignKey("self",
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            verbose_name='Родительская категория',
                            related_name="children")

    def items_count(self):
        """Количество заявок-объявлений в категории"""
        count = Order.objects.filter(category__slug=self.slug).count()
        return count

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    # class MPTTMeta:
    #     order_insertion_by = ['name']


class AbstractDeal(AbstractField):
    """Общие - дополнительные поля"""
    photo = models.ImageField("Фото", default="nophoto.png", upload_to="product_photo")
    price_min = models.DecimalField("Минимальная цена", max_digits=8, decimal_places=2, default=0.00)
    date_publication = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     # обрезаем фото
    #     super().save()
    #
    #     image = Image.open(self.photo.path)
    #
    #     if image.height > 64 or image.width > 64:
    #         resize = (500, 500)
    #         image.thumbnail(resize)
    #         image.save(self.photo.path)


class Order(AbstractDeal):
    """Заявка - объявление"""

    PAYMENT_METHOD_CHOICES = (
        ('for_cash', 'Наличными'),
        ('non_cash', 'Безналичный расчет'),
    )

    price_max = models.DecimalField("Максимальная цена", max_digits=8, decimal_places=2, default=0.00)
    date_validity = models.DateTimeField("Актуально до")
    category = TreeManyToManyField(Category, verbose_name="Категории", blank=True)
    payment_method = models.CharField('Способ оплаты', max_length=50, choices=PAYMENT_METHOD_CHOICES, default='for_cash')
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.CASCADE)
    city = models.CharField("Город", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("order", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # при создании заявки в шаблоне создаем slug
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заявка - объявление"
        verbose_name_plural = "Заявки - объявления"
        ordering = ['-date_publication', ]


class Offer(AbstractDeal):
    """Предложение"""

    STATUS_CHOICES = (
        ('not_choose', 'Не выбрано'),
        ('reject', 'Отклонить'),
        ('approve', 'Одобрить'),
    )

    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE, verbose_name='Заявка',
                              related_name='offers')
    seller = models.ForeignKey(User, default=None, on_delete=models.CASCADE, verbose_name='Продавец')
    status = models.CharField('Статус предложения', max_length=50, choices=STATUS_CHOICES, default='not_choose')
    # welcome = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        ordering = ['-id']

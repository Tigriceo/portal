from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class AbstractField(models.Model):
    """Общие - дополнительные поля"""
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Url-адрес", max_length=100)
    description = models.TextField("Описание", blank=True, null=True, max_length=5000)

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

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    # class MPTTMeta:
    #     order_insertion_by = ['name']


class AbstractDeal(AbstractField):
    """Общие - дополнительные поля"""
    photo = models.ImageField("Фото", default="default.svg", upload_to="product_photo")
    price_min = models.DecimalField("Минимальная цена", max_digits=8, decimal_places=2, default=0.00)
    date_publication = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        abstract = True


class Order(AbstractDeal):
    """Заявка - объявление"""

    PAYMENT_METHOD_CHOICES = (
        ('for_cash', 'Наличными'),
        ('non_cash', 'Безналичный расчет'),
    )

    price_max = models.DecimalField("Максимальная цена", max_digits=8, decimal_places=2, default=0.00)
    date_validity = models.DateTimeField("Актуально до")
    category = models.ManyToManyField(Category, verbose_name="Категории")
    payment_method = models.CharField('Способ оплаты', max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash')
    buyer = models.ForeignKey(User, verbose_name="Покупатель", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("order", kwargs={'pk': self.pk})

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
    status = models.CharField('Статус предложения', max_length=50, choices=STATUS_CHOICES, default='cash')
    # welcome = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        ordering = ['-id']
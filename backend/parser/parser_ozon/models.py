from django.db import models


class Product(models.Model):
    name = models.CharField(
        verbose_name='Заголовок карточки товара',
        max_length=255
    )
    price = models.DecimalField(
        verbose_name='Цена товара',
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(
        verbose_name='Описание товара',
    )
    image_url = models.URLField(
        verbose_name='Ссылка на товар',
    )
    discount = models.CharField(
        verbose_name='Скидка',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.name)

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.contrib.auth.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        blank=True,
        null=True, )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def check_children(self):
        return self.get_children()

    def get_absolute_url_category(self):
        return reverse('subcategory_list', kwargs={"slug": self.slug})

    def get_absolute_url_goods(self):
        return reverse('goods_list', kwargs={"slug": self.slug})


class Weight(models.Model):
    weight = models.PositiveSmallIntegerField()
    type_weight = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.weight} {self.type_weight}'

    class Meta:
        verbose_name = 'Вес'
        verbose_name_plural = 'вес'
        ordering = ['type_weight', 'weight']


class Test(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    ingredients = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.name


class Goods(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='goods',
                                 on_delete=models.SET_NULL,
                                 null=True)
    name = models.CharField(max_length=150, db_index=True, verbose_name='название')
    slug = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='goods/', blank=True, null=True, verbose_name='Картинка')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за минимальную единицу измерения')
    weight = models.ManyToManyField(Weight, verbose_name='Вес/Тара/Обьем')
    ingredients = models.ManyToManyField("self", blank=True, verbose_name='Ингридиенты', )
    hot = models.BooleanField(default=False, verbose_name='Острота')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_price_per_weight(self):
        ready_list_weight = {}
        for i in self.weight.all():
            ready_list_weight[i] = i.weight * self.price
        return ready_list_weight

    def get_absolute_url(self):
        return reverse('goods_detail', kwargs={"category_slug": self.category.slug, "goods_slug": self.slug})


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    detail = models.JSONField(default={}, blank=True)



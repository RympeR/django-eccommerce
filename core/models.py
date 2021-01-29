from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
LABEL_CHOICES = (
    ('Гарячі Роли', 'hot'),
    ('Класичні роли', 'classic'),
    ('Овочеві роли', 'vegetables'),
    ('Суші', 'sushi'),
    ('Спайсі суші', 'sets'),
    ('Сети', 'spice'),
)

class Category(models.Model):
    category_name = models.CharField('Категория', max_length=200)
    label = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_number(self) -> int:
        return self.pk + 1

    def __str__(self) -> str:
        return self.category_name

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" /'.format(self.image.url))
    
    admin_photo.short_description = 'Превью'
    admin_photo.allow_tags = True

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pc = models.ImageField(default='1.jpg', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователя'
    def __str__(self):
        return self.user.username

class SessionOrder(models.Model):
    id = models.AutoField(primary_key=True)
    approved = models.BooleanField(null=True, default=False)
    class Meta:
        verbose_name = 'Номер заказа в сессии'
        verbose_name_plural = 'Номера заказов в сессии'
    def __str__(self):
        return f"{self.pk}"

class OrderItem(models.Model):
    sessionOrder = models.ForeignKey(SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    sessionOrder = models.ForeignKey(SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    name = models.CharField(max_length=50, blank=False, null=True)
    phone_number = models.CharField(max_length=11, blank=False, null=True)
    person_amount = models.IntegerField(blank=False, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    def __str__(self):
        return str(self.sessionOrder)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class Address(models.Model):
    sessionOrder = models.ForeignKey(SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
    def __str__(self):
        return str(self.sessionOrder)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    sessionOrder = models.ForeignKey(SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
    def __str__(self):
        return str(self.sessionOrder)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'
    def __str__(self):
        return f"{self.pk}"
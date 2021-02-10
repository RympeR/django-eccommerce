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
PAYMENT_CHOICES = (
    ('W','WayForPay'),
    ('H','При доставке'),
)


class Category(models.Model):
    category_name = models.CharField('Категория', max_length=200)
    category_eng_name = models.CharField(
        'Категория Eng', max_length=200, null=True, blank=True)
    category_ru_name = models.CharField(
        'Категория Ru', max_length=200, null=True, blank=True)
    
    label = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_number(self) -> int:
        return self.pk + 1

    def __str__(self) -> str:
        return self.category_name


class ItemTag(models.Model):
    item_tag_name = models.CharField('Тэг', max_length=20)
    item_tag_eng_name = models.CharField('Тэг Eng', max_length=20, null=True, blank=True)
    item_tag_ru_name = models.CharField('Тэг Ru', max_length=20, null=True, blank=True)
    display_on_main = models.BooleanField('Отображается на главной')
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.item_tag_name

    def get_absolute_url(self):
        return reverse("core:shop-product", kwargs={
            'slug': self.slug
        })


class Item(models.Model):
    title = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100, null=True, blank=True)
    title_ru = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    slug = models.SlugField()
    description = models.TextField()
    ru_description = models.TextField(null=True, blank=True)
    english_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='photos', blank=True, null=True)
    item_tag = models.ManyToManyField(ItemTag, verbose_name='Тэги товара')

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
    profile_pc = models.ImageField(
        upload_to='photos', default='1.jpg', null=True, blank=True)
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
    sessionOrder = models.ForeignKey(
        SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
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
    sessionOrder = models.ForeignKey(
        SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    name = models.CharField(max_length=50, blank=False, null=True)
    phone_number = models.CharField(max_length=40, blank=False, null=True)
    person_amount = models.IntegerField(blank=False, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField('комментарий', max_length=255,null=True, blank=True)
    being_delivered = models.BooleanField(default=False)
    need_learning_branch = models.BooleanField(default=False)
    dont_recall = models.BooleanField(default=False)
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
            total -= total*(self.coupon.discount_percent / 100)
        return total


class Address(models.Model):
    sessionOrder = models.ForeignKey(
        SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return str(self.sessionOrder)


class Payment(models.Model):
    sessionOrder = models.ForeignKey(
        SessionOrder, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    paytype = models.CharField(choices=PAYMENT_CHOICES, max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return str(self.sessionOrder)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    discount_percent = models.IntegerField()
    amount = models.IntegerField()

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


class MainSlider(models.Model):
    slider_title = models.CharField(
        'Заголовок слайда', max_length=35, default='Изучите наше меню')
    slider_eng_title = models.CharField('Заголовок слайда eng', max_length=35, default='Изучите наше меню', null=True, blank=True)
    slider_ru_title = models.CharField('Заголовок слайда ru', max_length=35, default='Изучите наше меню', null=True, blank=True)
    slider_text = models.CharField('Текст слайда', max_length=50)
    slider_eng_text = models.CharField('Текст слайда eng', max_length=50, null=True, blank=True)
    slider_ru_text = models.CharField('Текст слайда ru', max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='photos', blank=True, null=True)
    button_text = models.CharField(
        'Текст кнопки', blank=True, null=True, max_length=20)
    button_eng_text = models.CharField('Текст кнопки eng', blank=True, null=True, max_length=20)
    button_ru_text = models.CharField('Текст кнопки ru', blank=True, null=True, max_length=20)

    @property
    def short_description(self):
        return truncatechars(self.slider_text, 20)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" /'.format(self.image.url))

    admin_photo.short_description = 'Превью'
    admin_photo.allow_tags = True

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return self.slider_text

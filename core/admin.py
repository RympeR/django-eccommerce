from django.contrib import admin

from .models import (Address, Category, Coupon, Item, ItemTag, MainSlider,
                     Order, OrderItem, Payment, Refund, SessionOrder, SetItem,
                     UserProfile)


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class MainSliderAdmin(admin.ModelAdmin):
    # fields = (
    #     'slider_title',
    #     'slider_text',
    #     'button_text',
    #     'image',
    #     'slider_ru_title',
    #     'slider_ru_text',
    #     'button_ru_text',
    #     'slider_eng_title',
    #     'slider_eng_text',
    #     'button_eng_text',
    # )
    list_display = [
        'admin_photo',
        'slider_title',
        'short_description',

    ]
    list_display_links = [
        'slider_title',
        'short_description',
    ]
    readonly_fields = [
        'admin_photo'
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'address',
        'coupon',
    ]
    list_display_links = [
        'address',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
    ]
    list_filter = ['street_address', 'apartment_address']
    search_fields = ['sessinoOrder', 'street_address', 'apartment_address']


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'admin_photo',
        'title',
        'price',
        'category',
    ]
    list_display_links = [
        'title',
        'category'
    ]
    list_filter = [
        'category'
    ]
    readonly_fields = [
        'admin_photo'
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(MainSlider, MainSliderAdmin)
# admin.site.register(UserProfile)
admin.site.register(SessionOrder)
admin.site.register(ItemTag)
admin.site.register(SetItem)

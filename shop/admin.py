from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Category, SessionOrder

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = [
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'address',
                    'coupon'
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
    fields = (
        'title', 
        'price',
        'discount_price',
        'category',
        'slug',
        'description',
        'image',
    )
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
# admin.site.register(UserProfile)
admin.site.register(SessionOrder)



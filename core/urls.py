from django.urls import path, include
from .views import (
    ItemDetailView, ItemView, checkout,
    view_404,
    itemview,
    add_to_cart,
    OrderSummaryView,
    ShopView,
    remove_from_cart,
    shop_product,
    remove_single_item_from_cart,
    AddCouponView,
    CheckoutView,
    switch_to_Ukraiunian_link,
    switch_to_English_link,
    deliveryAndPayPage,
    switch_to_Russian_link,   
)

app_name = 'core'

urlpatterns = [
    # path('', home_view, name='home-view'),
    path('uk/', switch_to_Ukraiunian_link, name='uk'),
    path('en/', switch_to_English_link, name='en'),
    path('ru/', switch_to_Russian_link, name='ru'),
    path('', itemview, name='menu'),
    path('delivery/', deliveryAndPayPage, name='delivery'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop/<str:slug>', shop_product, name='shop-product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('item/<slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('404/', view_404, name='404-view'),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-summary/', OrderSummaryView, name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add_coupon'),
]

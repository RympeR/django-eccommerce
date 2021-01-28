from django.urls import path, include
from .views import (
    ItemDetailView, ItemView, checkout,
    view_404,
    add_to_cart,
    OrderSummaryView,
    ShopView,
    remove_from_cart,
    remove_single_item_from_cart,
    AddCouponView,
)

app_name = 'core'

urlpatterns = [
    # path('', home_view, name='home-view'),
    path('', ItemView.as_view(), name='menu'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('checkout/', checkout, name='checkout'),
    path('item/<slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('404/', view_404, name='404-view'),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-summary/', OrderSummaryView, name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
]

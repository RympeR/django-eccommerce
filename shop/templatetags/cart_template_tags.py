from django import template
from shop.models import Order, OrderItem, Category, SessionOrder
from django.db.models import Sum



register = template.Library()


@register.filter
def cart_item_count(request):
    if request.session.get('session_id') is not None:
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
            qs = Order.objects.filter(sessionOrder=session_order, ordered=False)
            if qs.exists():
                return qs[0].items.count()
        except:
            return 0
    return 0


@register.filter
def cart_items(request):
    if request.session.get('session_id') is not None:
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
            qs = OrderItem.objects.filter(sessionOrder=session_order, ordered=False)
            if qs.exists():
                return qs
        except:
            return 0
    return 0

@register.filter
def total_order(request):
    if request.session.get('session_id') is not None:
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
            qs = OrderItem.objects.filter(sessionOrder=session_order, ordered=False)
            if qs.exists():
                res = 0
                for item in qs:
                    if item.item.discount_price:
                        res += item.get_total_discount_item_price()
                    else:
                        res += item.get_total_item_price()
                return res
            else:
                return 0

        except Exception as e:
                print(f'\n {e}\n')
                return 0
    return 0

@register.filter
def categories(request):
    qs = Category.objects.all()
    if qs.exists():
        return qs
    return 0
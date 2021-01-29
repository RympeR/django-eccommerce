from django.shortcuts import render
import random
import string
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, SessionOrder

# stripe.api_key = settings.STRIPE_SECRET_KEY 

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def view_404(request):
    return render(request, '404.html')

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")

def item_list(request):
    return render(request, 'menu3.html')
    
# def home_view(request):
#     return render(request, 'index.html')

def checkout(request):
    return render(request, 'checkout.html')

class ShopView(ListView):
    model = Item
    paginate_by=1
    template_name="shop.html"

class ItemView(ListView):
    model = Item
    template_name="menu3.html"

def OrderSummaryView(request):
    if request.method == 'GET':
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
            print(request)
            order = Order.objects.get(sessionOrder=session_order, ordered=False)
            print(order)
            context = {
                'object': order
            }
            return render(request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("/")

# class OrderSummaryView(View):
#     def get(self, *args, **kwargs):
#         try:
#             self.session_order = SessionOrder.objects.get(
#                 pk=self.request.session.get('session_id')
#             )
#             order = Order.objects.get(sessionOrder=self.session_order, ordered=False)
#             context = {
#                 'object': order
#             }
#             return render(self.request, 'cart.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("/")
            
def itemview(request):
    items = Item.objects.all()
    return render(request, "menu3.html", context={
        'items': items,
        
    })
class ItemDetailView(DetailView):
    model = Item
    template_name = "product-single.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.session.get('session_id') is not None:
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
        except Exception:
            session_order = SessionOrder.objects.create()
    else:
        session_order = SessionOrder.objects.create()
    request.session['session_id'] = session_order.pk
    order_item, created = OrderItem.objects.get_or_create(
        sessionOrder=session_order,
        ordered=False,
        item=item
    )


    order_qs = Order.objects.filter(sessionOrder=session_order, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Количество было обновлено.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Товар был добавлен в корзину.")
            return redirect("core:order-summary")
    else:
        order = Order.objects.create(
            sessionOrder=session_order
            )
        
        order.items.add(order_item)
        messages.info(request, "Товар был добавлен в корзину.")
        return redirect("core:product", slug=slug)

def remove_from_cart(request, slug):
    session_order = SessionOrder.objects.get(
            pk=request.session.get('session_id')
        )
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        sessionOrder=session_order,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                sessionOrder=session_order,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Товар был удален.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "Товара не было в корзине")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "У вас нет активного заказа")
        return redirect("core:product", slug=slug)


def remove_single_item_from_cart(request, slug):
    session_order = SessionOrder.objects.get(
            pk=request.session.get('session_id')
        )
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        sessionOrder=session_order,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                sessionOrder=session_order,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")

class AddCouponView(View):
    def post(self, *args, **kwargs):
        self.session_order = SessionOrder.objects.get(
            pk=self.request.session.get('session_id').pk
        )
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    sessionOrder=self.session_order, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")
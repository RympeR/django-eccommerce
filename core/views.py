from django.http import request
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
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, SessionOrder
from django.conf import settings    

# stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def switch_to_English_link(request):
    request.session['lang'] = 'en'
    return HttpResponse('switched to english')


def switch_to_Ukraiunian_link(request):
    request.session['lang'] = 'uk'
    return HttpResponse('switched to ukrainian ')


def view_404(request):
    return render(request, '404.html')


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        if coupon.amount > 0:
            coupon.amount -= 1
            coupon.save()
            return coupon
        else:
            return 0
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
    paginate_by = 1
    template_name = "shop.html"


class ItemView(ListView):
    model = Item
    template_name = "menu3.html"


def OrderSummaryView(request):
    if request.method == 'GET':
        try:
            session_order = SessionOrder.objects.get(
                pk=request.session.get('session_id')
            )
            print(request)
            order = Order.objects.get(
                sessionOrder=session_order, ordered=False)
            print(order)
            context = {
                'object': order
            }
            return render(request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("/")


def itemview(request):
    items = Item.objects.all()
    if request.session.get('lang') is None:
        request.session['lang'] = 'uk'
    return render(request, "menu3.html", context={
        'items': items,
    })


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-single.html"


def shop_product(request, slug):
    qs = Item.objects.filter(item_tag__slug=slug)
    context = {
        'items': qs,
    }
    return render(request, 'shop.html', context)


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


class AddCouponView(View):
    def post(self, *args, **kwargs):
        self.session_order = SessionOrder.objects.get(
            pk=self.request.session.get('session_id')
        )
        self.coupon_code = self.request.POST['coupon']
        print(self.coupon_code)
        try:
            order = Order.objects.get(
                sessionOrder=self.session_order, ordered=False)
            try:
                order.coupon = get_coupon(self.request, self.coupon_code)
            except ValueError:
                print('non existing')
            order.save()
            print('\nadded\n')
            messages.success(self.request, "Successfully added coupon")
            return redirect("core:checkout")
        except ObjectDoesNotExist:
            print('\n non existing \n')
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")


class CheckoutView(View):

    def get(self, *args, **kwargs):
        context = {}

        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        self.session_order = SessionOrder.objects.get(
            pk=self.request.session.get('session_id')
        )
        print(self.request.POST)
        try:
            order = Order.objects.get(
                sessionOrder=self.session_order, ordered=False)
        except ObjectDoesNotExist:
            print('\n non existing \n')
            messages.info(self.request, "You do not have an active order")
            return redirect("core:shop")
        name = self.request.POST['name']
        phone_order_number = self.request.POST['phone_order_number']
        person_amount = self.request.POST['person_amount']
        need_learning_branch = self.request.POST['need_learning_branch']
        dont_recall = self.request.POST['dont_recall']
        street_address = self.request.POST['street_address']
        apartment_address = self.request.POST['apartment_address']
        payment_option = self.request.POST['payment_option']
        order.name=name
        order.phone_number=phone_order_number
        order.person_amount=person_amount
        order.need_learning_branch=bool(need_learning_branch)
        order.dont_recall=bool(dont_recall)
        
        shipping_address = Address(
                            sessionOrder=self.session_order,
                            street_address=street_address,
                            apartment_address=apartment_address
                        )
        shipping_address.save()

        order.address = shipping_address
        order.save()

        if payment_option == 'W':
            return redirect('core:payment', payment_option='wayforpay')
        elif payment_option == 'H':
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            payment = Payment(
                sessionOrder=self.session_order,
                amount=order.get_total(),
                paytype='H'
            )
            payment.save()
            order.payment = payment
            order.ordered = True
            order.ref_code = create_ref_code()
            order.save()
            message = f'''
                Имя: {name}
                Номер телефона: {phone_order_number}
                Кол-во персон: {person_amount}
                Учебные палочки: {'Да' if need_learning_branch == 1 else 'Нет'}
                Не перезванивать: {'Да' if dont_recall == 1 else 'Нет'}
                Адрес улицы: {street_address}
                Адрес дома: {apartment_address}
                Тип оплаты: {'На месте' if payment_option=='H' else 'wayforpay на сайте'}
            '''
            send_mail(
                f'Заказ номер {self.request.session.get("session_id")}',
                message,
                'georg.rashkov@gmail.com',
                ['georg.rashkov@gmail.com'],
                fail_silently=False,
            )
            del self.request.session['session_id']
            return redirect('core:shop')

        else:
            messages.warning(
                self.request, "Invalid payment option selected")
            return redirect('core:checkout')
        
        return render(self.request, "checkout.html")


def deliveryAndPayPage(request):
    return render(request, 'delivery.html')
    
class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

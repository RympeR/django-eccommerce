from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    person_amount = forms.IntegerField(required=True) 

    street_address = forms.CharField(required=False)
    apartment_address = forms.CharField(required=False)

    need_learning_branch = forms.BooleanField(required=False)
    dont_recall = forms.BooleanField(required=False)



class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'cartcoupon',
        'placeholder': 'Coupon code',
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)

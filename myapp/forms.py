from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    # Payment method choices defined in the Order model
    PAYMENT_METHOD_CHOICES = Order.PAYMENT_METHOD_CHOICES

    # Adding custom fields for checkout
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES, 
        widget=forms.RadioSelect(), 
        label="Choose Payment Method"
    )

    class Meta:
        model = Order
        fields = ['payment_method']  # You can add more fields like shipping address here if required

    # You can add custom validation if needed, for example, to check if the payment method is valid
    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        if payment_method not in dict(self.PAYMENT_METHOD_CHOICES).keys():
            raise forms.ValidationError("Invalid payment method selected.")
        return payment_method

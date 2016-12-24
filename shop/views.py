import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
import stripe

logger = logging.getLogger(__name__)


class ShowCartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/cart.html', {
            'data_key': settings.STRIPE_PUBLISHABLE_KEY,
            'data_amount': 500,  # Amount in cents
            'data_name': 'akiyoko blog',
            'data_description': 'TEST',
        })


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_API_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a charge: this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=500,  # Amount in cents
                currency='usd',
                source=token,
                description='This is a test.',
            )
        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'error.html', {
                'message': "Your payment cannot be completed. The card has been declined.",
            })

        logger.info("Charge[{}] created successfully.".format(charge.id))
        messages.info(request, "Your payment has been completed successfully.")
        return render(request, 'shop/complete.html', {
            'charge': charge,
        })

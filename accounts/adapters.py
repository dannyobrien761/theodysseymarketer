from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class MyAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        """
        After signup, redirect the user to the checkout page for the selected plan.
        """
        plan_id = request.GET.get('plan')
        if plan_id:
            return f'/subscriptions/checkout/{plan_id}/'
        #  If no plan was provided, send back to pricing page
        return '/pricing/?error=must-select-plan'

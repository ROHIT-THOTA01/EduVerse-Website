from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,View
from memberships.models import Membership,UserMembership,Subscription
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership = get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type =  request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

class MembershipSelectView(LoginRequiredMixin, ListView):
    template_name = 'memberships/membership_list.html'
    context_object_name = 'memberships'
    model = Membership
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        if current_membership:
            context['current_membership'] = str(current_membership.membership)
        else:
            context['current_membership'] = None
        return context

    def post(self,request,*args,**kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership = get_user_membership(self.request)
        user_subscription = get_user_subscription(self.request)

        selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
        else:
            messages.error(request, 'Invalid membership type selected.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_membership and user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, 'The selected membership is your current membership, and your next payment will be processed until {}'.format('get this value from the line'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))


@login_required
def PaymentView(request):
    user_membership = get_user_membership(request)
    if not user_membership:
        messages.error(request, 'Please create a membership first.')
        return redirect(reverse("memberships:select_membership"))
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("memberships:select_membership"))
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']

            # Only process Stripe if properly configured
            if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY and not user_membership.stripe_customer_id.startswith('temp_'):
                customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
                customer.source = token 
                customer.save()

                subscription = stripe.Subscription.create(
                    customer=user_membership.stripe_customer_id,
                    items=[
                        { "plan": selected_membership.stripe_plan_id },
                    ]
                )
                subscription_id = subscription.id
            else:
                # Create a temporary subscription ID for testing
                subscription_id = f'temp_sub_{request.user.id}_{selected_membership.membership_type}'

            return redirect(reverse('memberships:update_transaction',
                                    kwargs={
                                        'subscription_id': subscription_id
                                    }))
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
            return redirect(reverse("memberships:select_membership"))


    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payment.html", context)

@login_required
def UpdateTransactionRecords(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, '{} membership successfully created'.format(
        selected_membership))
    return redirect(reverse('memberships:select_membership'))

@login_required
def CancelSubscription(request):
    user_sub = get_user_subscription(request)

    if not user_sub or user_sub.active is False:
        messages.info(request, "You don't have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Only cancel Stripe subscription if it's a real one
    if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY and not user_sub.stripe_subscription_id.startswith('temp_'):
        try:
            sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
            sub.delete()
        except Exception as e:
            messages.warning(request, f'Stripe subscription cancellation failed: {str(e)}')

    user_sub.active = False
    user_sub.save()

    try:
        free_membership = Membership.objects.get(membership_type='Bepul')
    except Membership.DoesNotExist:
        free_membership = Membership.objects.filter(membership_type='free').first()
        if not free_membership:
            messages.error(request, 'Free membership not found. Please contact support.')
            return redirect(reverse('memberships:select_membership'))
    
    user_membership = get_user_membership(request)
    if user_membership:
        user_membership.membership = free_membership
        user_membership.save()
    
    user = get_object_or_404(User,username=request.user.username)
    user_email = user.email

    messages.info(
        request, "Subscription successfully cancelled. We have sent you an email notification")
    # sending an email here
    try:
        send_mail(
            'Subscription successfully cancelled',
            'Your subscription has been successfully cancelled. Thank you for using our service.',
            'support@courseraclone.com',
            [user_email],
            fail_silently=True,
        )
    except Exception:
        pass  # Email sending is optional
    
    return redirect(reverse('memberships:select_membership'))

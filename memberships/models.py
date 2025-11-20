from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import stripe
from datetime import datetime

# Only set Stripe API key if it's configured
if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your models here.
MEMBERSHIP_CHOICES = (
('Professional','pro'),
('Korxona','ent'),
('Bepul','free')
)

class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES,default='Bepul',max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.user.username

def post_save_create_user_membership(sender, instance, created, *args, **kwargs):
    user_membership, created_membership = UserMembership.objects.get_or_create(user=instance)
    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        try:
            if instance.email and hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY:
                new_customer_id = stripe.Customer.create(email=instance.email)
                user_membership.stripe_customer_id = new_customer_id['id']
                user_membership.save()
            else:
                # Create a placeholder customer ID if Stripe is not configured
                user_membership.stripe_customer_id = f'temp_{instance.id}_{instance.username}'
                user_membership.save()
        except Exception as e:
            # If Stripe fails, create a placeholder customer ID
            # This allows the user to be created even if Stripe is not configured
            user_membership.stripe_customer_id = f'temp_{instance.id}_{instance.username}'
            user_membership.save()

# Connect the signal
post_save.connect(post_save_create_user_membership, sender=User)

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership,on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        try:
            if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY and not self.stripe_subscription_id.startswith('temp_'):
                subscription = stripe.Subscription.retrieve(
                    self.stripe_subscription_id)
                return datetime.fromtimestamp(subscription.created)
        except Exception:
            pass
        return None

    @property
    def get_next_billing_date(self):
        try:
            if hasattr(settings, 'STRIPE_SECRET_KEY') and settings.STRIPE_SECRET_KEY and not self.stripe_subscription_id.startswith('temp_'):
                subscription = stripe.Subscription.retrieve(
                    self.stripe_subscription_id)
                return datetime.fromtimestamp(subscription.current_period_end)
        except Exception:
            pass
        return None

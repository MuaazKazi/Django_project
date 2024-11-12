from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from dateutil.relativedelta import relativedelta
from MMApps.Masterwork.models import TimeStamp
from MMApps.Masterwork.helpers.create_primary_key import generate_primary_key
import os

# Define the function to handle dynamic upload paths
def profile_image_upload_path(instance, filename):
    return f'client_profiles/{instance.client.client_id}/{filename}'

class Clients(TimeStamp):
    POST_FIX = 'client'
    client_id = models.CharField(primary_key=True, max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    mobile = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_verified_tac = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, default='123456')

    def save(self, *args, **kwargs):
        if not self.client_id:
            self.client_id = generate_primary_key(self.POST_FIX)
            self.password = make_password(self.password)
        super(Clients, self).save(*args, **kwargs)

class ClientProfile(TimeStamp):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    POST_FIX = 'client_profile'
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='client_profile')
    profile = models.ImageField(upload_to=profile_image_upload_path, default='default-images/client-default.png')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True, null=True, choices=GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        try:
            existing_profile = ClientProfile.objects.get(pk=self.pk)
        except ClientProfile.DoesNotExist:
            existing_profile = None

        if self.profile and (is_new or (existing_profile and existing_profile.profile != self.profile)):
            if self.profile.name.startswith('default-images'):
                new_filename = self.profile.name
                self.profile.name = os.path.join(new_filename)
            else:
                base, ext = os.path.splitext(self.profile.name)
                new_filename = f"{self.client.client_id}_{self.POST_FIX}{ext}"
                self.profile.name = self.generate_unique_filename(new_filename)

        super(ClientProfile, self).save(*args, **kwargs)

    def generate_unique_filename(self, filename):
        base, ext = os.path.splitext(filename)
        unique_name = f"{base}_{get_random_string(length=8)}{ext}"
        return unique_name


class ClientAddress(TimeStamp):
    POST_FIX = 'client_address'
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='client_address')
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

class ClientMeasurements(TimeStamp):
    POST_FIX = 'client_measurements'
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='client_measurements')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    body_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

from django.db import models

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Plan(TimeStamp):
    name = models.CharField(max_length=50)  # e.g., "1 Month", "2 Months", "Quarterly"
    duration_in_months = models.PositiveIntegerField()  # Number of months for the plan
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price of the plan

    def __str__(self):
        return self.name



class ClientSubscription(TimeStamp):
    POST_FIX = 'client_subscription'
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('hold', 'Hold'),
        ('deactive', 'Deactive')
    ]

    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='client_subscription')
    start_date = models.DateField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    end_date = models.DateField(blank=True, null=True)  # Allow it to be blank initially
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Default status to Active

    def save(self, *args, **kwargs):
        # Calculate the end_date based on the plan's duration in months
        if self.plan:
            self.end_date = self.start_date + relativedelta(months=self.plan.duration_in_months)

        # Call the original save method
        super().save(*args, **kwargs)


# Automatically create ClientProfile, ClientAddress, and ClientMeasurements when a new Client is added
@receiver(post_save, sender=Clients)
def create_related_client_data(sender, instance, created, **kwargs):
    if created:  # Only run this for newly created clients
        # Create a related ClientProfile entry
        ClientProfile.objects.create(client=instance)

        # Create a related ClientAddress entry
        ClientAddress.objects.create(client=instance)

        # Create a related ClientMeasurements entry
        ClientMeasurements.objects.create(client=instance)

# Connect the signal
post_save.connect(create_related_client_data, sender=Clients)
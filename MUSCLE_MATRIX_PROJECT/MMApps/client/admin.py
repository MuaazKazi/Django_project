from django.contrib import admin
from .models import Clients, ClientProfile, ClientAddress, ClientMeasurements, Plan, ClientSubscription
from django.utils import timezone
from datetime import timedelta

class ClientsAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'email', 'mobile']
    search_fields = ['client_id', 'email', 'mobile']

admin.site.register(Clients, ClientsAdmin)

class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'first_name', 'last_name', 'gender', 'dob']
    list_filter = ['gender']

admin.site.register(ClientProfile, ClientProfileAdmin)

admin.site.register(ClientAddress)

admin.site.register(ClientMeasurements)

admin.site.register(Plan)

class ExpiringDeactiveFilter(admin.SimpleListFilter):
    title = 'Expiring Deactive Plans'
    parameter_name = 'expiring_deactive'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Expiring in 5 Days'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            # Calculate the date for 5 days from now
            five_days_from_now = timezone.now().date() + timedelta(days=5)
            return queryset.filter(status='deactive', end_date__lte=five_days_from_now)
        return queryset

@admin.register(ClientSubscription)
class ClientSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'plan', 'start_date', 'end_date', 'status')
    list_filter = (ExpiringDeactiveFilter,)  # Add the custom filter here

    def get_queryset(self, request):
        # Optionally, you can override the queryset to limit displayed objects
        return super().get_queryset(request)




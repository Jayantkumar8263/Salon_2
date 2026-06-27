from django.contrib import admin
from .models import Service, Appointment, WorkingHours, Payment
from Staff_app.models import StaffProfile
from customer_app.models import CustomerProfile

# Method 1: Simple registration
# admin.site.register(Service)

# Method 2: With customization (BETTER)

admin.site.site_header = "Salon & Co.Management Staff"
admin.site.site_title = "Salon Admin "
admin.site.index_title = "Welcome Boss"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'duration', 'price', 'is_active')
    list_filter = ['is_active']
    search_fields = ('service_name', 'description')
    ordering = ['service_name']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'service')
    filter_horizontal = ['Service']

    def service(self, obj):
        return ", ".join([s.service_name for s in obj.Service.all()])
    service.short_description = 'Services Offered'

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'staff', 'service', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'staff')
    search_fields = ('customer__user__username', 'staff__user__username')
    date_hierarchy = 'appointment_date'
    readonly_fields = ['booked_at']

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'staff')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
    readonly_fields = ['payment_date']
from django.contrib import admin
from .models import Medicine, Cart, Order, Bill, BillItem
from django.contrib import admin

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'price', 'requires_prescription')
    search_fields = ('name', 'company')
    list_filter = ('requires_prescription', 'company')

admin.site.register(Medicine, MedicineAdmin)
# admin.site.register(Medicine)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Bill)
admin.site.register(BillItem)
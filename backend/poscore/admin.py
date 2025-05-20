from django.contrib import admin
from .models import MenuItem, Bill, BillItem

admin.site.register(MenuItem)
admin.site.register(Bill)
admin.site.register(BillItem)

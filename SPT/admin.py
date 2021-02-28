from django.contrib import admin
from .models import Members,Spendings,Shares

# Register your models here.
admin.site.register(Members)
admin.site.register(Spendings)
admin.site.register(Shares)
class MembersInline(admin.TabularInline):
    model=Members
    extra=1
class SharesAdmin(admin.ModelAdmin):
    inlines=[MembersInline]
    
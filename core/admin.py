from django.contrib import admin
from django.db import transaction
from django.utils import timezone
from .models import MemberProfile,DepositOption,PaymentWallet,DepositRequest,WithdrawalRequest,StockRequest,RecoveryCase
admin.site.register(MemberProfile); admin.site.register(DepositOption); admin.site.register(PaymentWallet)
@admin.register(DepositRequest)
class DepositAdmin(admin.ModelAdmin):
 list_display=('id','user','requested_amount','method','status','created_at'); list_filter=('status','method')
 actions=['confirm_verified_deposits','reject_deposits']
 @admin.action(description='Confirm selected deposits after verifying payment')
 def confirm_verified_deposits(self,request,queryset):
  for d in queryset.filter(status='pending'):
   with transaction.atomic():
    d=DepositRequest.objects.select_for_update().get(pk=d.pk)
    if d.status!='pending': continue
    profile,_=MemberProfile.objects.get_or_create(user=d.user)
    amount=d.confirmed_amount if d.confirmed_amount is not None else d.requested_amount
    profile.available_balance+=amount; profile.save(update_fields=['available_balance'])
    d.status='successful'; d.save(update_fields=['status'])
@admin.register(WithdrawalRequest)
class WithdrawalAdmin(admin.ModelAdmin): list_display=('id','user','amount','status','created_at'); list_filter=('status',)
@admin.register(StockRequest)
class StockAdmin(admin.ModelAdmin): list_display=('id','user','company','amount','status','created_at'); list_filter=('status','company')
@admin.register(RecoveryCase)
class RecoveryAdmin(admin.ModelAdmin): list_display=('reference','user','platform_name','amount','status','created_at'); list_filter=('status',)

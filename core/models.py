from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
class MemberProfile(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
 available_balance=models.DecimalField(max_digits=12,decimal_places=2,default=Decimal('0.00'))
 def __str__(self): return self.user.username
class DepositOption(models.Model):
 amount=models.DecimalField(max_digits=10,decimal_places=2,unique=True,validators=[MinValueValidator(Decimal('1'))]); active=models.BooleanField(default=True)
 def __str__(self): return f'${self.amount}'
class PaymentWallet(models.Model):
 METHOD=[('bank','Bank transfer'),('crypto','Cryptocurrency')]
 method=models.CharField(max_length=12,choices=METHOD); label=models.CharField(max_length=100); instructions=models.TextField(); active=models.BooleanField(default=True)
 def __str__(self): return self.label
class DepositRequest(models.Model):
 STATUS=[('pending','Pending admin review'),('successful','Successful'),('rejected','Rejected')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='deposits'); requested_amount=models.DecimalField(max_digits=12,decimal_places=2); confirmed_amount=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True); method=models.CharField(max_length=12,choices=PaymentWallet.METHOD); receipt=models.FileField(upload_to='receipts/',blank=True); status=models.CharField(max_length=12,choices=STATUS,default='pending'); created_at=models.DateTimeField(auto_now_add=True)
class WithdrawalRequest(models.Model):
 STATUS=[('pending','Pending review'),('paid','Paid'),('rejected','Rejected')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='withdrawals'); amount=models.DecimalField(max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('10'))]); bank_name=models.CharField(max_length=100); account_name=models.CharField(max_length=150); account_number=models.CharField(max_length=80); status=models.CharField(max_length=12,choices=STATUS,default='pending'); created_at=models.DateTimeField(auto_now_add=True)
class StockRequest(models.Model):
 COMPANIES=[('TSLA','Tesla Inc. (TSLA)'),('AAPL','Apple (AAPL)'),('NVDA','NVIDIA (NVDA)'),('MSFT','Microsoft (MSFT)'),('AMZN','Amazon (AMZN)'),('GOOGL','Alphabet (GOOGL)'),('META','Meta Platforms (META)'),('AMD','Advanced Micro Devices (AMD)')]; STATUS=[('pending','Pending review'),('approved','Approved'),('rejected','Rejected')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='stock_requests'); company=models.CharField(max_length=8,choices=COMPANIES); amount=models.DecimalField(max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('50'))]); status=models.CharField(max_length=12,choices=STATUS,default='pending'); created_at=models.DateTimeField(auto_now_add=True)
class RecoveryCase(models.Model):
 STATUS=[('submitted','Submitted'),('reviewing','Under review'),('more_info','More information needed'),('closed','Closed')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='recovery_cases'); reference=models.CharField(max_length=24,unique=True); platform_name=models.CharField(max_length=150); amount=models.DecimalField(max_digits=12,decimal_places=2); description=models.TextField(); status=models.CharField(max_length=12,choices=STATUS,default='submitted'); created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.reference

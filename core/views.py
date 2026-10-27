import uuid
from decimal import Decimal,InvalidOperation
from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import render,redirect
from .models import MemberProfile,DepositOption,PaymentWallet,DepositRequest,WithdrawalRequest,StockRequest,RecoveryCase
class SignUpForm(UserCreationForm):
 email=forms.EmailField(required=True)
 class Meta(UserCreationForm.Meta): fields=('username','email','password1','password2')
def profile(user): return MemberProfile.objects.get_or_create(user=user)[0]
def home(request): return render(request,'site.html',{'page':'home'})
def page(request,page): return render(request,'site.html',{'page':page})
def signup(request):
 form=SignUpForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  user=form.save(); profile(user); login(request,user); return redirect('dashboard')
 return render(request,'site.html',{'page':'signup','form':form})
@login_required
def dashboard(request): return render(request,'site.html',{'page':'dashboard','profile':profile(request.user),'deposits':request.user.deposits.order_by('-created_at')[:5],'stocks':request.user.stock_requests.order_by('-created_at')[:5],'cases':request.user.recovery_cases.order_by('-created_at')[:5]})
@login_required
def buy_stocks(request):
 p=profile(request.user)
 if request.method=='POST':
  try: amount=Decimal(request.POST.get('amount','0'))
  except InvalidOperation: amount=Decimal('0')
  company=request.POST.get('company')
  if company not in dict(StockRequest.COMPANIES) or amount<50: messages.error(request,'Choose a company and enter at least $50.')
  else:
   with transaction.atomic():
    p=MemberProfile.objects.select_for_update().get(pk=p.pk)
    if amount>p.available_balance: messages.error(request,'Insufficient available balance.')
    else: p.available_balance-=amount; p.save(); StockRequest.objects.create(user=request.user,company=company,amount=amount); messages.success(request,'Request submitted for review. This is not proof of a brokerage trade.'); return redirect('portfolio')
 return render(request,'site.html',{'page':'buy_stocks','profile':p,'companies':StockRequest.COMPANIES})
@login_required
def portfolio(request): return render(request,'site.html',{'page':'portfolio','stocks':request.user.stock_requests.order_by('-created_at')})
@login_required
def add_funds(request):
 options=DepositOption.objects.filter(active=True); wallets=PaymentWallet.objects.filter(active=True)
 if request.method=='POST':
  option=options.filter(pk=request.POST.get('amount_option')).first(); method=request.POST.get('method'); receipt=request.FILES.get('receipt')
  if not option or method not in ('bank','crypto') or not wallets.filter(method=method).exists() or not receipt: messages.error(request,'Select an available amount and payment method, then upload evidence.')
  elif receipt.size>5*1024*1024: messages.error(request,'Receipt must be 5 MB or smaller.')
  else: DepositRequest.objects.create(user=request.user,requested_amount=option.amount,method=method,receipt=receipt); messages.success(request,'Submitted for admin review. Funds are not available until payment is verified.'); return redirect('dashboard')
 return render(request,'site.html',{'page':'add_funds','options':options,'wallets':wallets})
@login_required
def withdraw(request):
 p=profile(request.user)
 if request.method=='POST':
  try: amount=Decimal(request.POST.get('amount','0'))
  except InvalidOperation: amount=Decimal('0')
  bank=request.POST.get('bank_name','').strip(); name=request.POST.get('account_name','').strip(); number=request.POST.get('account_number','').strip()
  if amount<10 or not all([bank,name,number]): messages.error(request,'Minimum withdrawal is $10. Complete all bank details.')
  else:
   with transaction.atomic():
    p=MemberProfile.objects.select_for_update().get(pk=p.pk)
    if amount>p.available_balance: messages.error(request,'Insufficient available balance.')
    else: p.available_balance-=amount; p.save(); WithdrawalRequest.objects.create(user=request.user,amount=amount,bank_name=bank,account_name=name,account_number=number); messages.success(request,'Withdrawal request submitted for review.'); return redirect('dashboard')
 return render(request,'site.html',{'page':'withdraw','profile':p})
@login_required
def recovery(request):
 if request.method=='POST':
  try: amount=Decimal(request.POST.get('amount','0'))
  except InvalidOperation: amount=Decimal('0')
  platform=request.POST.get('platform_name','').strip(); desc=request.POST.get('description','').strip()
  if amount<=0 or not platform or not desc: messages.error(request,'Complete the required fields.')
  else: RecoveryCase.objects.create(user=request.user,reference='CJ-'+uuid.uuid4().hex[:10].upper(),platform_name=platform,amount=amount,description=desc); messages.success(request,'Case submitted. Recovery is not guaranteed.'); return redirect('recovery')
 return render(request,'site.html',{'page':'recovery','cases':request.user.recovery_cases.order_by('-created_at')})

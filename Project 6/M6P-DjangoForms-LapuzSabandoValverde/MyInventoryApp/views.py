from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import WaterBottle, Supplier, Account
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.


def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'supplier' :supplier_objects})

def view_bottles(request):
    bottles_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles' :bottles_objects})

def view_bottle_details(request, pk):
    b = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'b': b})

def add_bottle(request):
    if request.method == "POST":
        sku = request.POST.get('sku')
        brand = request.POST.get('brand')
        cost = request.POST.get('cost')
        size = request.POST.get('size')
        mouth_size = request.POST.get('mouth_size')
        color = request.POST.get('color')
        supplied_by = request.POST.get('supplied_by')
        current_qty = request.POST.get('current_qty')

        supplier = Supplier.objects.get(id=supplied_by)

        WaterBottle.objects.create(
            sku=sku,
            brand=brand,
            cost=cost,
            size=size,
            mouth_size=mouth_size,
            color=color,
            supplier=supplier,
            current_quantity=current_qty
        )        
        return redirect('MyInventoryApp/view_bottles')
    else:
        supplier_objects = Supplier.objects.all()
        return render(request, 'MyInventoryApp/add_bottle.html', {'supplier': supplier_objects})

def delete_bottle(request, pk):
    WaterBottle.objects.filter(pk=pk).delete()
    return redirect('view_bottles')

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')

        try:
            user = Account.objects.get(username=uname, password=pword)
            return redirect('MyInventoryApp/view_supplier.html')
        except Account.DoesNotExist:
            messages.error(request, "Invalid login")
            return render(request, 'MyInventoryApp/base.html')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('view_supplier') 
        else:
            messages.error(request, 'Invalid login')
            return render(request, 'MyInventoryApp/login.html')  

    return render(request, 'MyInventoryApp/login.html')


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')

        if Account.objects.filter(username=uname).exists():
            messages.error(request, 'Account already exists')
            
        else:
            Account.objects.create(username=uname, password=pword)
            messages.success(request, 'Account created successfully')
            return redirect('MyInventoryApp/login.html')  

    return render(request, 'MyInventoryApp/signup.html')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account})

def delete_account(request, pk ):
    Account.objects.filter(pk=pk).delete()
    return redirect('MyInventoryApp/signup.html')

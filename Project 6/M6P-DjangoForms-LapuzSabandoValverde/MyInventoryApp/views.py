from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import WaterBottle, Supplier, Account
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'supplier' :supplier_objects})



def view_bottles(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    bottles = WaterBottle.objects.filter(supplier=supplier)
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottles, 'supplier': supplier})


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
    global id  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            account = Account.objects.get(username=username)
            if account.getPassword() == password:
                request.session['user_id'] = account.pk
                request.session['username'] = account.username
                id = account.pk
                return redirect ('view_supplier')
            else:
                messages.error(request, 'Invalid login')
        except Account.DoesNotExist:
            messages.error(request, 'Invalid login')

    return render(request, 'MyInventoryApp/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(username=username).exists():
            messages.warning(request, 'Account already exists')
        else:
            Account.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')  

    return render(request, 'MyInventoryApp/signup.html')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account})

def delete_account(request, pk ):
    Account.objects.filter(pk=pk).delete()
    return redirect('MyInventoryApp/signup.html')

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new1 = request.POST.get('new_password')
        new2 = request.POST.get('confirm_password') 

        if check_password not in(current, account.password):
            messages.error(request, 'Current password is incorrect.')
        elif new1 != new2:
            messages.error(request, 'New passwords do not match.')
        else:
            account.password = new1
            account.save()
            return redirect('manage_account', pk=pk)
        
        return render(request, 'tapasapp/change_password.html', {'account': account})

from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import WaterBottle, Supplier, Account
from django.contrib import messages
# Create your views here.


def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'view_supplier.html', {'supplier' :supplier_objects})

def view_bottles(request):
    bottles_objects = WaterBottle.objects.all()
    return render(request, 'view_bottles.html', {'bottles' :bottles_objects})

def view_bottle_details(request, pk):
    b = get_object_or_404(WaterBottle, pk=pk)
    return render(request, 'view_bottle_details.html', {'b': b})

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
        return redirect('view_bottles')
    else:
        supplier_objects = Supplier.objects.all()
        return render(request, 'add_bottle.html', {'supplier': supplier_objects})

def delete_bottle(request, pk):
    WaterBottle.objects.filter(pk=pk).delete()
    return redirect('view_bottles')

def base(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(username=username, password=password)
            return redirect('view_supplier')
        except Account.DoesNotExist:
            messages.error(request, "Invalid login")
            return render(request, 'login.html')

    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    return render(request, 'signup.html')

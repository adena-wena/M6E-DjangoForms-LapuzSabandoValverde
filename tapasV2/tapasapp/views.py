from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages  # type: ignore
from .models import Dish, Account

# Create your views here.




def better_list(request):
    dish_objects = Dish.objects.all()
    account = None

    account_id = request.session.get('account_id')
    if account_id:
        try:
            account = Account.objects.get(pk=account_id)
        except:
            pass
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects, 'account': account})


    return render(request, 'tapasapp/better_list.html', {'dishes':dish_objects, 'account': account})

# def basic_list(request, pk):
#     a = get_object_or_404(Account, pk=pk)
#     return render(request, 'tapasapp/basic_list.html', {'a':a})

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    return render(request, 'tapasapp/manage_account.html', {'account': account})

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('better_list')

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_list')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_list')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})
    
def login(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        try:
            account = Account.objects.get(username=uname)
            if account.password == pword:
                request.session['account_id'] = account.pk
                return redirect('better_list')
            else:
                messages.error(request, "Invalid login. Please try again.")
        except Account.DoesNotExist:
            messages.error(request, "Invalid login. Please try again.")
    return render(request, 'tapasapp/login.html')

def signup(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')
        confirm_pword = request.POST.get('confirm_pword')
        if pword != confirm_pword:
            messages.error(request, "Passwords do not match")
        elif Account.objects.filter(username=uname).exists():
            messages.error(request, "Account already exists")
        else:
            Account.objects.create(username=uname, password=pword)
            messages.success(request, "Account created successfully!")
            return redirect('login')
    return render(request, 'tapasapp/signup.html')

def change_password(request, pk):
    
    account = Account.objects.get(pk=pk)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('manage_account', pk=pk)

        current = request.POST.get('current_password')
        new1 = request.POST.get('new_password')
        new2 = request.POST.get('confirm_password') 

        if current != account.getPassword():  
            messages.error(request, 'Current password is incorrect.')
        elif new1 != new2:
            messages.error(request, 'New passwords do not match.')
        else:
            account.password = new1  
            account.save()
            return redirect('manage_account', pk=pk)
    
    return render(request, 'tapasapp/change_password.html', {'account': account})


from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib import messages  # type: ignore
from .models import Dish, Account

# Create your views here.


def login(request):
    return render(request, 'tapasapp/login.html')

def signup(request):
    return render(request, 'tapasapp/signup.html')

def better_list(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes':dish_objects})

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
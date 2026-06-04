from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Item, Order
from django.contrib.auth.forms import UserCreationForm

# Home Page
def home_view(request):
    return render(request, 'hotel/home.html')


# ---------------------- AUTH ----------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('hotel-home')
    return render(request, 'hotel/login.html')


def logout_view(request):
    logout(request)
    return redirect('hotel-home')


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel-home')
    else:
        form = UserCreationForm()

    return render(request, 'hotel/register.html', {'form': form})


# ---------------------- MENU ----------------------

def menu_view(request):
    items = Item.objects.all()
    cart = request.session.get('cart', {})
    return render(request, 'hotel/menu.html', {'items': items, 'cart': cart})


# ---------------------- CART ----------------------

@login_required
def update_cart(request, item_id, action):
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if action == "add":
        cart[item_id] = cart.get(item_id, 0) + 1
    elif action == "remove":
        if item_id in cart:
            if cart[item_id] > 1:
                cart[item_id] -= 1
            else:
                del cart[item_id]

    request.session['cart'] = cart
    return redirect('menu')


# ---------------------- ORDER ----------------------

@login_required
def order_view(request):
    cart = request.session.get('cart', {})

    if request.method == "POST" and cart:
        items = Item.objects.filter(id__in=[int(i) for i in cart.keys()])
        items_dict = {item.id: item for item in items}

        for item_id, quantity in cart.items():
            item = items_dict[int(item_id)]
            Order.objects.create(
                user=request.user,
                item=item,
                quantity=quantity,
                total_price=item.price * quantity
            )

        request.session['cart'] = {}
        return redirect('order')

    items = Item.objects.filter(id__in=[int(i) for i in cart.keys()])
    items_dict = {item.id: item for item in items}

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'hotel/order.html', {
        'cart': cart,
        'items_dict': items_dict,
        'orders': orders
    })


# ---------------------- ADMIN ----------------------

@staff_member_required
def admin_dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'hotel/admin_dashboard.html', {'orders': orders})

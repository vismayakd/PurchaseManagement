from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,ProductForm,PaymentForm
from . models import Product,Cart,CartItem,OrderHistory
from django.contrib import messages


# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin_dashboard')
               
            else:
                return redirect('user_dashboard')
    return render(request,'home.html')

@login_required
def admin_dashboard(request):
    prods = Product.objects.all()
    return render(request,'admin_dashboard.html', context={'products':prods})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product added succesfully')
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request,'add_product.html',context={'form':form})

def user_logout(request):
    logout(request)
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User registered succesfully')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'user_register.html',context={'form':form})

@login_required
def user_dashboard(request):
    prods = Product.objects.all()
    return render(request,'user_dashboard.html', context={'products':prods})

@login_required
def add_to_cart(request,id):
    product_id = id
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    print("cart", cart)
    if request.method == 'POST':
        quantity =  int(request.POST['quantity'])
        try:
            cart_item = CartItem.objects.get(order=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                order=cart,
                product=product,
                quantity=quantity,
                price=product.price
            )
        
        total = 0
        for item in cart.items.all():

            total += item.price * item.quantity
        cart.total = total
        cart.save()
        messages.success(request,f"{product.name} added to cart")
        return redirect('user_dashboard')
    return render(request,'add_to_cart.html',context={'product':product})

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    each_items = []
    total_price = 0
    if cart:
        for item in cart.items.all():
            each_item_total = item.price * item.quantity
            total_price += each_item_total  
            each_items.append({
                'id':item.id,
                'product': item.product,
                'quantity': item.quantity,
                'price': item.price,
                'total': each_item_total
            })
    return render(request, "cart.html", {"items": each_items, "total": total_price})


@login_required
def delete_item(request,id):
    item_id = id
    item = get_object_or_404(CartItem,id=item_id)
    item.delete()
    messages.success(request,'Item removed from cart')
    return redirect('user_dashboard')


@login_required
def place_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    for item in cart.items.all():
        OrderHistory.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_amount=item.price * item.quantity,
            status="requested"  
        )
    messages.success(request, "Order requested successfully! Waiting for admin approval.")
    return redirect("user_orders")

@login_required
def make_payment(request, order_id):
    try:
        order = OrderHistory.objects.get(id=order_id, user=request.user, status="accepted")
    except OrderHistory.DoesNotExist:
        messages.error(request, "This order is not available for payment.")
        return redirect("user_orders")
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            order.status = "paid"
            order.save()
            Cart.objects.filter(user=request.user).delete()
            messages.success(request, f"Payment successful for Order {order.order_id}")
            return redirect("user_orders")
    else:
        form = PaymentForm()
    return render(request, "payment_form.html", {"form": form, "order": order,"total": order.total_amount})

@login_required
def user_orders(request):
    orders = OrderHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'user_orders.html',context={'orders':orders})

@login_required
def admin_orders(request):
    orders = OrderHistory.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {"orders": orders})

@login_required
def update_order_status(request, order_id, action):
    order = OrderHistory.objects.get(id=order_id)
    if action == "accept":
        order.status = "accepted"
    elif action == "reject":
        order.status = "rejected"
    order.save()
    messages.success(request, f"Order {order.order_id} marked as {order.status}.")
    return redirect("admin_orders")
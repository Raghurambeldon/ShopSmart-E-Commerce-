from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Category, Customer,Cart,Order, OrderItem
from .decorators import login_required_custom
from .forms import CheckoutForm

def home(request):
    categories = Category.objects.all()
    data = {'categories': categories}
    return render(request, 'home.html', data)


def deals(request):
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    
    if categoryID:
        products = Product.objects.filter(category_id=categoryID)
    else:
        products = Product.objects.all()
    data = {'products': products, 'categories': categories}
    return render(request, 'deals.html', data)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products.html', {'product': product})


def signup(request):
    if request.method == 'GET':
        return render(request, "signup.html")
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
 
        if not first_name or not last_name or not email or not mobile or not password:
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")
        
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")
        

        hashed_password = make_password(password)
        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=hashed_password
        )
        messages.success(request, "Account created successfully. Please Login")
        return redirect('login')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                request.session['user_id'] = customer.id
                request.session['email'] = customer.email
                messages.success(request, f"Welcome back, {customer.first_name}!")
                print(request.session.get('user_id'))
                return redirect('deals') 
            else:
                messages.error(request, 'Incorrect password.')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer with this email does not exist.')

    if request.session.get('user_id'):
        return redirect('deals')

    return render(request, 'login.html')



def logout(request):
    request.session.flush()  
    messages.success(request, "Logged out successfully.")
    return redirect('login') 



def search_products(request):
    query = request.GET.get('search', '').strip()  

    if query:
        product_results = Product.objects.filter(name__icontains=query)
    else:
        product_results = Product.objects.none() 

    if not product_results.exists() and query:
        messages.warning(request, "No products found matching your search query.")

    context = {
        'query': query,
        'product_results': product_results,
    }

    return render(request, 'search_products.html', context)

@login_required_custom
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    email = request.session.get('email')
    if not email:
        messages.error(request, "Please log in first.")
        return redirect('login')

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Another {product.name} has been added to your cart.")
    else:
        messages.success(request, f"{product.name} has been added to your cart.")

    return redirect('cart')


@login_required_custom
def cart(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Please log in first.")
        return redirect('login')

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

    cart_items = Cart.objects.filter(customer=customer)
    return render(request, 'cart.html', {'cart_items': cart_items})




@login_required_custom
def remove_from_cart(request, cart_item_id):
    # Get the cart item from the database
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    # Check if the logged-in customer owns this cart item
    if cart_item.customer.email == request.session.get('email'):
        # Remove the cart item
        cart_item.delete()
        messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
    else:
        messages.error(request, "You cannot remove items that don't belong to you.")

    # Redirect to the cart page after removal
    return redirect('cart')


@login_required_custom
def checkout(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Please log in first.")
        return redirect('login')

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

    cart_items = Cart.objects.filter(customer=customer)

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('deals')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.total_price = total_price
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            cart_items.delete()

            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_summary', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })



def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'order_summary.html', context)


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from backend.models import Product, Category, Cart


# Create your views here.
def home(request):

    # Retrieve all categories for use in the view
    categories = Category.objects.all()

    # Check if 'category' query parameter is present
    category_present = 'category' in request.GET

    data = {
        'categories': categories,
        'category_present': category_present,
    }

    # Apply category filter if category is present and is not 'All'
    category_id = request.GET.get('category')

    if category_id and category_id != 'All':

        # Filter products based on the selected category
        products = Product.objects.filter(category__id=category_id)

        # Get the category object and set page title and product count
        category = get_object_or_404(Category, pk=category_id)
        data['page_title'] = category.name
        data['product_count'] = category.products.count()

        # Pass filtered products to the template
        data['products'] = products

        print(products)
        for product in products:
            print(product.category.all())

        return render(request, 'frontend/product/list/type1.html', data)

    return render(request, 'frontend/home.html', data)

def show(request, product_id):
    # Retrieve the specific product using the provided product_id
    product = get_object_or_404(Product, pk=product_id)

    # Prepare the data to be passed to the template
    data = {
        'product': product,
        'page_title': product.name,  # You can set the page title as per your requirement
        'category': product.category,  # Optional: if you want to display the category
    }

    # Render the product detail template
    return render(request, 'frontend/product/detail/type1.html', data)

def auth_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'frontend/auth/login.html')


def auth_logout(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the login page or home page

def register(request):
    return render(request, 'frontend/auth/register.html')

def forget_password(request):
    return render(request, 'frontend/auth/forget_password.html')

def account(request):
    return render(request, 'frontend/auth/account.html')

def about(request):
    return render(request, 'frontend/auth/about.html')

@login_required  # Ensures the user is authenticated
def cart(request):
    # Get the current logged-in user
    user = request.user

    # Print user email for debugging (only if the user is authenticated)
    if user.is_authenticated:
        print(user.email)

        # Filter cart items for the current user
        cart_items = Cart.objects.filter(custom_user=user)

        # Calculate the grand total for the cart
        grand_total = Cart.grand_total(customer_id=user.id)

        # Prepare the data to be passed to the template
        data = {
            'cart_items': cart_items,  # Pass the filtered cart items to the template
            'grand_total': grand_total,
            'page_title': 'Cart',  # You can set the page title as per your requirement
            'cart_count': cart_items.count()
        }
    else:
        # If the user is not authenticated, handle accordingly
        data = {
            'cart_items': [],  # No cart items for unauthenticated users
            'page_title': 'Cart',  # Page title remains the same
            'error_message': 'You need to log in to view your cart.'  # Optional error message
        }

    return render(request, 'frontend/cart/index.html', data)

@login_required
def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, custom_user=request.user)

    if cart_item:
        # Increase the quantity
        cart_item.qty += 1
        cart_item.save()
        messages.success(request, f'Quantity increased for {cart_item.product.name} in your cart.')
    else:
        messages.error(request, 'Cart item not found.')

    return redirect('cart')  # Adjust as necessary

@login_required
def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, custom_user=request.user)

    # Decrease the quantity, ensuring it doesn't go below 1
    if cart_item.qty > 1:
        cart_item.qty -= 1
        cart_item.save()
        messages.success(request, f'Quantity decreased for {cart_item.product.name} in your cart.')
    else:
        messages.warning(request, f'Cannot decrease quantity for {cart_item.product.name} below 1.')

    return redirect('cart')  # Adjust as necessary

@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, custom_user=request.user)

    # Remove the cart item
    product_name = cart_item.product.name
    cart_item.delete()

    messages.success(request, f'{product_name} removed from your cart.')
    return redirect('cart')  # Adjust as necessary


@login_required
def clear_cart(request):
    cart_items = Cart.objects.filter(custom_user=request.user)

    if cart_items.exists():
        cart_items.delete()
        messages.success(request, 'Cart cleared successfully.')
    else:
        messages.error(request, 'No items found in the cart.')

    return redirect('cart')  # Adjust as necessary

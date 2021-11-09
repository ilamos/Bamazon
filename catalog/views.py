from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm

from .models import Product
# Create your views here.

def generate_product(title, price, imagesource, id):
    return f"""
            <span class="product_span">
                <a href="/catalog/product/{id}">
                    <h3 class="product_title">{title}</h3>
                    <h4 class="product_price">Price: {price} €</h4>
                    <span class="align_bottom">
                        <center>
                            <img class="product_img" src="{imagesource}"> </img>
                        </center>
                    </span>
                    </a>
                    <button onclick="window.location.href='/catalog/add_cart/{id}'">Add to cart</button>
            </span>
            """

def index(req):
    product_list = Product.objects.all()
    product_string = ""
    for product in product_list:
        product_string += generate_product(product.title, product.price, product.image_source, product.id)
    return render(req, 'catalog.html', {'product_list': product_string})

def register_req(req):
    if req.method == "POST":
        form = NewUserForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            messages.success(req, "Registration successfull.")
            return redirect(index)
        messages.error(req, "Error while registering")
    form = NewUserForm()
    return render(req, "register.html", {"register_form":form})

def login_req(req):
    if req.method == "POST":
        form = AuthenticationForm(req, data= req.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                messages.info(req, f"Logged in as {username}")
                return redirect(index)
            else:
                messages.error(req, "Invalid username or password")
        else:
            messages.error(req, "Invalid username or password")
    form = AuthenticationForm()
    return render(req, "login.html", {"login_form":form})

def logout_req(req):
    logout(req)
    messages.info(req, "You have logged out")
    return redirect(index)

def add_to_cart(req, product_id):
    if not req.session.get('cart'):
        req.session['cart'] = [product_id]
        req.session['cart_sz'] = 1
    else:
        cur_cart = req.session.get('cart')
        cur_cart.append(product_id)
        req.session['cart'] = cur_cart
        req.session['cart_sz'] = len(cur_cart)
    return redirect(req.META.get('HTTP_REFERER'))

def cart(req):
    return render(req, 'cart.html', {})

def product_by_id(req, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except:
        return HttpResponse("Error getting product")
    if not product:
        return HttpResponse("Product not found")
    else:
        return render(req, 'product_info.html', {'product': generate_product(product.title, product.price, product.image_source, product.id)})
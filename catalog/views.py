from django.contrib.auth.forms import AuthenticationForm
from django.forms.forms import Form
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm
from .forms import SearchForm

from .models import Product
# Create your views here.

def generate_product(title, price, imagesource, id):
    return f"""
            <div class="product_div">
                <a href="/catalog/product/{id}">
                    <h3 class="product_title">{title}</h3>
                    <h4 class="product_price">{price} €</h4>
                    <span class="align_bottom">
                        <center>
                            <img class="product_img" src="{imagesource}"> </img>
                        </center>
                    </span>
                    </a>
                    <button class="button_main" onclick="window.location.href='/catalog/add_cart/{id}'">Add to cart</button>
            </div>
            """

def index(req):
    product_list = Product.objects.all()[:12]
    product_string = '<div class="product_container">'
    prod_count = 0
    for product in product_list:
        prod_count += 1
        product_string += generate_product(product.title, product.price, product.image_source, product.id)
        if prod_count == 3:
            product_string += '</div><div class="product_container">'
            prod_count = 0
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

def search_req(req):
    if req.method == "POST":
        form = SearchForm(req.POST)
        if form.is_valid():
            search_q = form.cleaned_data.get("search_query")
            print("[SEARCH] Search submitted with query: " + search_q)
            product_list = Product.objects.filter(title__icontains=search_q)
            product_string = '<div class="product_container">'
            prod_count = 0
            for product in product_list:
                prod_count += 1
                product_string += generate_product(product.title, product.price, product.image_source, product.id)
                if prod_count == 3:
                    product_string += '</div><div class="product_container">'
                    prod_count = 0
            messages.info(req, "Searched successfully")
            return render(req, "search.html", {"show_search": False, "results": product_string, "no_results": (len(product_list) == 0), "query": search_q})
        messages.error(req, "Search error")
    form = SearchForm()
    return render(req, "search.html", {"form": form, "show_search": True})

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
        if len(cur_cart) >= 100:
            messages.error(req, "Cart is full (MAX 100)")
            cur_cart = cur_cart[:99]
            req.session['cart'] = cur_cart
            return redirect(req.META.get('HTTP_REFERER'))
        cur_cart.append(product_id)
        req.session['cart'] = cur_cart
        req.session['cart_sz'] = len(cur_cart)
    return redirect(req.META.get('HTTP_REFERER'))

def calculate_cart_price(cart):
    price = 0
    for product in cart:
        price += product.price
        
    return round(price, 2)

def cart(req):
    cart_products = []
    if req.session.get('cart'):
        for prod in req.session.get('cart'):
            cur_prod = Product.objects.get(pk=prod)
            if len(cur_prod.title) > 30:
                cur_prod.title = cur_prod.title[:29] + "..."
            cart_products.append(cur_prod)
    return render(req, 'cart.html', {"cart" : cart_products, "sum_price": calculate_cart_price(cart_products)})

def remove_cart(req, item_id):
    if not req.session.get('cart'):
        req.session['cart'] = []
        req.session['cart_sz'] = 1
    else:
        cur_cart = req.session.get('cart')
        cur_cart.remove(item_id)
        req.session['cart'] = cur_cart
        req.session['cart_sz'] = len(cur_cart)
    return redirect(req.META.get('HTTP_REFERER'))

def product_by_id(req, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except:
        return HttpResponse("Error getting product")
    if not product:
        return HttpResponse("Product not found")
    else:
        return render(req, 'product_info.html', {'product': product})
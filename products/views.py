from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
import razorpay
from django.conf import settings

from django.contrib.auth.decorators import login_required


# Create your views here.
from .models import Product
from .models import Category
from django.core.paginator import Paginator

def product_list(request):            
    query = request.GET.get('q')   # search box
    categ_id=request.GET.get('category')  # category

    sort_items = request.GET.get('sort')
    products = Product.objects.all()   
    categories = Category.objects.all()
    

    if sort_items == 'low':
        products = products.order_by('price')

    if sort_items == 'high':
        products = products.order_by('-price')

    if query:
        products = Product.objects.filter(name__icontains=query)
    if categ_id:
        products = Product.objects.filter(category_id = categ_id)
    page_number = request.GET.get('page')   # paginator

    paginator = Paginator(products,3) 

    page_obj = paginator.get_page(page_number)

    
    return render(request,'products/product_list.html',{'products':products,'query':query,'category':categories,'page_obj':page_obj})

def product_details(request,id):
    product = get_object_or_404(Product,id=id)

    return render(request,'products/product_details.html',{'product':product})

from django.contrib import messages

def add_to_cart(request,id):
    
    product = get_object_or_404(Product,id=id)

    if product.stock == 0:
        return HttpResponse("Out of stock")
    
    cart_item,created = Cart.objects.get_or_create(
        user = request.user,
        products = product,
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(
        request,"Product added to cart successfully"
    )
    return redirect('product_list')

    # cart = request.session.get('cart',{})
    
    # product = get_object_or_404(Product,id=id)
     
    # if product.stock == 0:
    #     return HttpResponse(f"Out of stock")
    # else:
    #     if str(id) in cart:
    #         cart[str(id)] += 1
        
    #     else:
    #         cart[str(id)] = 1

    #     request.session['cart'] = cart
    #     messages.success(
    #         request,"Product added to cart successfully"
    #     )
    # return redirect('product_list')


# cart implementation

from .models import Cart

def cart_view(request):
    cart_items = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.products.price*item.quantity
    #     print(price.products.price)
    # print('total_price',total_price)
    print(Cart.objects.all())
    return render(request,'products/cart.html',{'cart_items':cart_items,'total_price':total_price})



    # total_price = 0
    # cart = request.session.get('cart',{})
    # for product_id,quantity in cart.items():
    #     product = Product.objects.get(id = product_id)
    #     item_total = product.price*quantity
    #     total_price += item_total

  

    # return render(request,'products/cart.html',{'cart_items':cart_items,'total_price':total_price})

def cart_increment(request,id):
    cart_item = get_object_or_404(
        Cart,
        user = request.user,
        products_id = id

    )
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')






    # product = get_object_or_404(Product,id=id)
    # cart_item = Cart.objects.get(user=request.user,
    #                            products=product,
    #                            )
    # cart_item.quantity += 1
    # cart_item.save()
    # return redirect('cart_view')

    

    # cart = request.session.get('cart',{})

    # if str(id) in cart:
    #     cart[str(id)] += 1
    
    # request.session['cart'] = cart
    # return redirect('cart_view')


def cart_decrement(request,id):

    cart_item = get_object_or_404(
        Cart,
        user = request.user,
        products_id = id,

    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')




    # cart = request.session.get('cart',{})

    # if str(id) in cart:
    #     if cart[str(id)] > 0:
    #         cart[str(id)] -= 1
    #     if cart[str(id)] == 0:
    #         del cart[str(id)]

    # request.session['cart'] = cart

    # return redirect('cart_view')

def clear_cart(request):

    Cart.objects.all().delete()
    
    return redirect('cart_view')

    # cart = request.session.get('cart',{})

    # request.session['cart'] = {}

    # return redirect('cart_view')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            print("username already exists")
        else:
           User.objects.create_user(
           username = username,
           email = email,
           password = password)
           return redirect('login_view')
        
        
    return render(request,'products/register.html')       

from .forms import LoginForm

def login_view(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
            username = username,
            password = password
            )
            if user is not None:
              login(request,user)
              messages.success(
            request,"User logged in successfully")
              return redirect('product_list')
            else:
                messages.error(
    request,
    "Invalid username or password"
)
  
    else:
        form = LoginForm()

    return render(request,'products/login.html',{'forms':form})

def logout_view(request):
    logout(request)

    return redirect('login_view')



@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user = request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.products.price*item.quantity


    client = razorpay.Client(
        auth = (
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
        )
    )

    payment =  client.order.create({
        'amount':int(total_price*100),
        'currency':'INR',
        'payment_capture':"1"
    }

    )
    return render(request,'products/checkout.html',{'payment':payment,'key_id':settings.RAZORPAY_KEY_ID,'total_price':total_price})



#     total_price = 0
#     order_item = []
#     cart = request.session.get("cart",{})

#     for product_id,quantity in cart.items():

#         product = Product.objects.get(id=product_id)
#         total_price += product.price * quantity

#         if product.stock < quantity:
#             return HttpResponse(f"only {product.stock} items available for {product.name}")
#     client = razorpay.Client(
#     auth = (
#         settings.RAZORPAY_KEY_ID,
#         settings.RAZORPAY_KEY_SECRET
#     )
# )    
#     payment = client.order.create({
#             'amount':int(total_price*100),
#             'currency':'INR',
#             'payment_capture':1
#         })            
                
    
    # return render(request,"products/checkout.html",{'payment':payment,'key_id':settings.RAZORPAY_KEY_ID,'total_price':total_price})

'''

# if request.method == "POST":
    #         customer_name = request.POST['customer_name']
    #         phone = request.POST['phone']
    #         address = request.POST['address']
    # if customer_name.strip() and phone.strip() and address.strip() and total_price:

            
    # if request.method == 'POST':
    #         form = CheckoutForm(request.POST)
    #         if form.is_valid():
    #             customer_name = form.cleaned_data['customer_name']      # forms.Form
    #             phone = form.cleaned_data['phone']
    #             address = form.cleaned_data['address']

                 

                #     order = Order.objects.create(
            # user = request.user,
            # name = customer_name,
            # phone = phone,
            # address = address,
            # total_amount = total_price
            # )

'''


from .models import Order
from .models import OrderItem


# from .forms import CheckoutForm
from .forms import OrderForm
@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    total_price = 0
 
    order_item = []
    cartitems = Cart.objects.filter(user = request.user)
    for item in cartitems:
        total_price += item.products.price*item.quantity

        # if product.stock < quantity:
        #     return HttpResponse(f"only {product.stock} items available for {product.name}")

    if request.method == 'POST':     

        form = OrderForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user                                   
            order.total_amount = total_price
            order.save()

            for item in cartitems:
                product = Product.objects.get(id=item.products_id)
                items = OrderItem.objects.create(
                order = order,
                product = product,
                quantity = item.quantity,
                price = product.price
            )
                order_item.append(items)
                product.stock -= item.quantity
                product.save()
                item.delete()
                return render(request,"products/success.html",{'ord':order,'order_items':order_item,'total_price':total_price})             
    else:
            # form = CheckoutForm()
        form = OrderForm()
        return render(request,'products/order.html',{'form':form,'total_price':total_price})



    


from django.contrib import admin

# admin.site.register(Order)

def myorder(request): 
     myorder = Order.objects.filter(
         user = request.user
     ).order_by('-id')

     return render(request,"products/myorder.html",{'order':myorder})


def orderdetails(request,id):
    order = Order.objects.get(id=id,user=request.user)
    return render(request,'products/orderdetails.html',{'order':order})

def usr(request):
    total_order = Order.objects.filter(user = request.user).count()
    usr = request.user
    return render(request,'products/user.html',{'usr':usr,'total_order':total_order})



from .models import Whishlist
@login_required
def wishlist(request,id):
    
    # product = Product.objects.get(id=id)
    product = get_object_or_404(Product,id=id)

    Whishlist.objects.get_or_create(
        user = request.user,
        products = product,
    )
    
    wishlist = Whishlist.objects.filter(user=request.user)
    messages.success(
        request,"Item added to wishlist"
    )


    return redirect('product_list')

def wishlist_view(request):
    wishlist = Whishlist.objects.filter(user = request.user)
    return render(request,'products/wishlist.html',{'wishlist':wishlist})

# 

# Connect Django to Razorpay.

# Flow:

# Django
# ↓
# Client Object
# ↓
# Razorpay











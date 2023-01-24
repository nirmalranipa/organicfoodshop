from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from .utils import VerifyPaytmResponse
from . import Checksum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

# register


def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # print(fname,lname,email,pass1,pass2)
        # print("#############")
        user_exists = Register.objects.filter(email=email).exists()
        if user_exists:
            messages.error(request, 'Email already exists !!')
            return redirect('register')

        else:

            if pass1 == pass2:
                obj = Register(first_name=fname, last_name=lname,
                               email=email, pass1=pass1)
                obj.save()
                messages.success(request, 'You are Registered !!')
                return redirect('login')
            else:
                messages.error(request, 'Password are not match !!')
                return redirect('register')
    else:
        return render(request, "register.html")


# login
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['pass1']
        print("@@@@@@@@@@@")
        print(email, pass1)
        try:
            ob = Register.objects.get(email=email)
            if ob.pass1 == pass1:
                messages.success(request, 'You are logged')
                request.session['user'] = email
                return redirect('myaccount')
            else:
                messages.error(request, ' Password Incorrect!!')
                return redirect('login')
        except:
            messages.error(request, 'User not Registered !!')
            return redirect('login')

    else:
        return render(request, "login.html")


# myaccount
def myaccount(request):
    if 'user' in request.session:
        return render(request, "myaccount.html")
    return redirect('login')


# delet add to card
def delete(request, id):
    print('########', id)
    s1 = Cart.objects.filter(id=id)
    s1.delete()
    return redirect('cart')


def plus(request, id):
    email = request.session['user']
    obj = Register.objects.get(email=email)
    cart = Cart.objects.filter(id=id)
    qty = cart[0].qty + 1
    price = qty*cart[0].prod_name.price
    Cart.objects.filter(id=id).update(price=price, qty=qty)
    return redirect('cart')


def minus(request, id):
    email = request.session['user']
    obj = Register.objects.get(email=email)
    cart = Cart.objects.filter(id=id)
    qty = cart[0].qty - 1
    price = qty*cart[0].prod_name.price
    Cart.objects.filter(id=id).update(price=price, qty=qty)
    return redirect('cart')


# logout
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect("index")
    return redirect('login')


# cart product add
def cart(request):
    if 'user' not in request.session:
        return redirect("login")
    email = request.session['user']
    obj = Register.objects.get(email=email)
    obj1 = Cart.objects.filter(user_id=obj.id, status=False)
    list1 = []
    for i in obj1:
        list1.append(i.price)
    total = sum(list1)
    return render(request, 'cart.html', {'cart_product': obj1, 'total': total})


# add_to_card
def add_to_cart(request, id):
    if 'user' in request.session:
        print("####")
        user = Register.objects.get(email=request.session['user'])
        product = Product.objects.filter(id=id)
        count = Cart.objects.filter(
            user_id=user.id, prod_name_id=product[0].id).count()
        print(count)
        cart = Cart.objects.filter(user_id=user.id, prod_name_id=product[0].id)

        if count > 0:
            qty = cart[0].qty + 1
            price = qty * product[0].price
            Cart.objects.filter(user_id=user.id, prod_name_id=product[0].id).update(
                qty=qty, price=price)
            print("@@@@@@@")
            return redirect('index')
        else:
            cart = Cart(user_id=user.id,
                        prod_name_id=product[0].id, qty=1, price=product[0].price)
            cart.save()
            print("&&&&&&&")
            return redirect('shop')
    else:
        return redirect('login')


def shop(request):
    prod = Product.objects.all()
    return render(request, 'shop.html', {'prod': prod})


def indexView(request):
    feaufruit = Product.objects.filter(cat_name__id=6)
    js = Product.objects.filter(cat_name__id=7)
    new = Product.objects.filter(cat_name__id=8)
    prod = Product.objects.all()
    # Pagination Featur fruit
    paginator = Paginator(feaufruit, 6, orphans=0)
    page_number = request.GET.get('page')
    feaufruit = paginator.get_page(page_number)

    # Pagination js
    paginator = Paginator(js, 6, orphans=0)
    page_number = request.GET.get('page')
    js = paginator.get_page(page_number)

    # Pagination new
    paginator = Paginator(new, 6, orphans=0)
    page_number = request.GET.get('page')
    new = paginator.get_page(page_number)

    return render(request, 'index.html', {'feaufruit': feaufruit, 'js': js, 'new': new, 'page_number': page_number, 'prod': prod})


def myaccount(request):
    return render(request, 'myaccount.html')


def about(request):
    return render(request, 'about.html')


def blogdetails(request):
    return render(request, 'blog_details.html')


def blog(request):
    return render(request, 'blog.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        subject = request.POST['subject']
        comment = request.POST['comment']

        ob = Contact(name=name, email=email, contact=contact,
                     subject=subject, comment=comment)
        ob.save()
        return redirect('contact')

    return render(request, 'contact.html')


def productdetails(request):
    sid = request.GET.get("cid")
    if sid is not None:
        sp = Product.objects.get(pk=sid)
        m_images = Multiple_image.objects.filter(p_image__id=sid)
        return render(request, 'productdetails.html', {"pid": sp})
    return redirect('shop')


def checkout(request):
    if 'user' in request.session:
        address_list = Chack.objects.filter(
            user__email=request.session['user'])
        if request.method == "POST":

            user = Register.objects.get(email=request.session['user'])
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            postcode = request.POST['postcode']
            email = request.POST['email']
            phone = request.POST['phone']

            obj = Chack(user=user, first_name=first_name, last_name=last_name, address=address,
                        city=city, state=state, postcode=postcode, email=email, phone=phone)
            print("????????")
            obj.save()
            return redirect("checkout")
        email = request.session['user']
        obj = Register.objects.get(email=email)
        obj1 = Cart.objects.filter(user_id=obj.id, status=False)
        list1 = []
        for i in obj1:
            list1.append(i.price)
        total = sum(list1)
        x = total + 50

        return render(request, 'checkout.html', {"address": address_list, "total": total, 'cart_product': obj1, "shipping": x})
    else:
        return redirect('login')


def myorder(request):
    if 'user' in request.session:
        email = request.session['user']
        my_order = Order.objects.filter(user__email=email)
        if request.method == "POST":
            address_id = request.POST.get("ADDRESS")
            address = Chack.objects.get(pk=int(address_id))
            print(address_id)

            obj = Register.objects.get(email=email)
            obj1 = Cart.objects.filter(user__email=email)
            list1 = []
            cart_id = ''
            for i in obj1:
                cart_id += ","+str(i.id)
                list1.append(i.prod_name.price)
                i.delete()
            total = sum(list1)
            x = total + 50
            order = Order(user=obj, product=x, address=address)
            order.save()

            order_id = Checksum.__id_generator__()
            totals = int(total)+50
            bill_amount = str(totals)
            data_dict = {
                'MID': settings.PAYTM_MERCHANT_ID,
                'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
                'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
                'MOBILE_NO': '7573803684',
                'EMAIL': 'ritesh1112k@gmail.com',
                'CUST_ID': '123123',
                'ORDER_ID': order_id,
                'TXN_AMOUNT': bill_amount,
            }  # This data should ideally come from database
            data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
                data_dict, settings.PAYTM_MERCHANT_KEY)
            context = {
                'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
                'comany_name': settings.PAYTM_COMPANY_NAME,
                'data_dict': data_dict
            }
            return render(request, 'payment.html', context)
            return render(request, 'myorder.html', {"myorder": my_order, "obj1": obj1})
        else:
            return render(request, 'myorder.html', {"myorder": my_order})
    else:
        return redirect('login')


def payment(request):
    return render(request, "payment.html")


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:

        return redirect("myorder")
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)

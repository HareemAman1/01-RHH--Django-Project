import json

from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rhh import settings
from shop.models import UserOtpModel, ProductModel, DjangoUser, Order, OrderItem, MessageUs
from shop.serializers import DjangoUserSerializer, MessageSerializer


# Create your views here.
def home(request):
    if request.method == 'POST':
        data = {"username": request.POST['name'], 'phonenum': request.POST['pnumber'],
                'useremail': request.POST['email'],
                'message': request.POST['msg']}
        sendEmail(data)

        return render(request, 'shop/index.html', context={"send": True})
    return render(request, 'shop/index.html')


def about(request):
    if request.method == 'POST':
        data = {"username": request.POST['name'], 'phonenum': request.POST['pnumber'],
                'useremail': request.POST['email'],
                'message': request.POST['msg']}
        sendEmail(data)
        return render(request, 'shop/about.html', context={"send": True})
    return render(request, 'shop/about.html')


def sendEmail(data):
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    context = data
    email_html = render_to_string('email.html', context)
    email_text = strip_tags(email_html)
    email = EmailMultiAlternatives(
        subject='New Message from {}'.format(data['username']),
        body=email_text,
        from_email=data['useremail'],
        to=[settings.EMAIL_HOST_USER, ]
    )
    email.attach_alternative(email_html, 'text/html')
    email.send()


def new(request):
    return render(request, 'shop/news.html')


@login_required(login_url='login')
def cart(request):
    return render(request, 'shop/Cart.html')


def place_order(request):
    if request.method == 'POST':
        cart_list = json.loads(request.POST['cart'])
        order = Order.objects.create(user=request.user)
        for product in cart_list:
            product_obj = ProductModel.objects.filter(id=product['id']).get()
            OrderItem.objects.create(order=order, product=product_obj, price=product_obj.product_price,
                                     quantity=int(product['quantity']))
        return JsonResponse({'message': 'Order placed successfully.',
                             'status': 'success',
                             'order_id': str(order.id)})


class LoginView(APIView):

    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        check_user = DjangoUser.objects.filter(email=username)
        if check_user.exists():
            if check_user.first().is_active:
                request.session['is_logged'] = True
                password = request.data.get('password')
                user = auth.authenticate(email=username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'auth/login.html',
                                  context={'error': True, 'error_msg': "User does n't Exists."})
            else:
                redirect_url = '/otp-verify/?arg=' + username
                return redirect(redirect_url)
        else:
            return render(request, 'auth/login.html', context={'error': True, 'error_msg': "User does n't Exists."})


class SignUpView(APIView):

    def get(self, request):
        return render(request, 'auth/signup.html')

    def post(self, request):
        username = request.data.get('email')
        check_user = DjangoUser.objects.filter(username=username)
        if check_user.exists():
            return render(request, 'auth/signup.html', context={'error': True,
                                                                'error_msg': 'User with Email Already Exists!'})
        data = {
            "email": request.data.get('email'), "password": request.data.get('password'),
            "first_name": request.data.get('fname'), "last_name": request.data.get('lname'),
            "age": request.data.get('age'), "phone": request.data.get('phone'), "address": request.data.get('address'),
            "is_active": False, 'username': username
        }
        serializer = DjangoUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            redirect_url = '/otp-verify/?arg=' + username
            return redirect(redirect_url)
        return render(request, 'auth/signup.html', context={'error': True, 'error_msg': serializer.errors})


class OTPVerifyView(APIView):

    def get(self, request):
        email = request.GET.get('arg')
        return render(request, 'auth/otp.html', context={'email': email})

    def post(self, request):
        username = request.data.get('email')
        check_user = DjangoUser.objects.filter(username=username)
        if check_user.exists():
            verify = UserOtpModel.objects.filter(user=check_user.get(), code=request.data.get('otp'))
            if verify.exists():
                check_user.update(is_active=True, is_verified=True)
                verify.get().delete()
                return redirect('login')
        return render(request, 'auth/otp.html', context={'error': True, 'error_msg': 'Invalid OTP', 'email': username})


class ProductViewSet(APIView):
    def get(self, request, format=None):
        products = ProductModel.objects.all()
        return render(request, 'shop/buy.html', context={'products': products})

    def post(self, request, format=None):
        value = request.POST['search']
        qs = ProductModel.objects.all()
        if value != '':
            products = qs.filter(product_name__icontains=request.POST['search'])
            return render(request, 'shop/buy.html', context={'products': products, 'search': request.POST['search'],
                                                             'filter': True})
        return render(request, 'shop/buy.html', context={'products': qs, 'search': '', 'filter': False})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        request.session.flush()
        request.session.set_expiry(-1)
        return render(request, 'shop/index.html', context={'logout': True})

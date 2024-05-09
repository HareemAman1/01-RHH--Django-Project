from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm
from .views import LoginView, SignUpView, OTPVerifyView, ProductViewSet, LogoutView

urlpatterns = [

    # path('',views.index,name='shop/index'),
    #   path('',views.ProductView.as_view(), name=('index')),

    # path('home',views.home,name=('index')),
    path('', views.home, name=('home')),
    path('about/', views.about, name='about'),
    path('news/', views.new, name=('news')),
    path('buy/', ProductViewSet.as_view(), name=('buy')),
    path('cart/', views.cart, name=('cart')),
    path('login/', LoginView.as_view(), name=('login')),
    path('signup/', SignUpView.as_view(), name=('signup')),
    path('otp-verify/', OTPVerifyView.as_view(), name=('otp-verify')),
    path('logout/', LogoutView.as_view(), name=('logout')),
    path('place-order/', views.place_order, name=('place-order'))

]

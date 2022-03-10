from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.frontpage, name='frontpage'),
    path('add-employee', views.add_employee, name='add_employee'),
    path('edit-employee<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete-employee<int:pk>/', views.delete_employee, name='delete_employee'),
    path('payment/', views.payment_page, name='payment'),
    # path('order-payment/', views.order_payment, name='order_payment'),
    path('payment/callback/', views.callback, name='callback'),

]

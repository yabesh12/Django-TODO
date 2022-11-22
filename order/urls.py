from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    # path('order-item/', views.order_payment, name='payment'),
    # path('callback/', views.callback, name='callback')

    path("payment/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),
    path("payment-verification/", views.payment_verification, name="payment_verification"),
]

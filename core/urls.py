from django.template.defaulttags import url
from django.urls import path
from .import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.frontpage, name='frontpage'),
    path('add-employee', views.add_employee, name='add_employee'),
    path('edit-employee<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee<int:id>/', views.delete_employee, name='delete_employee'),
]



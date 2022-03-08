from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from core.models import Employee, CustomUser


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'mobile_no', 'department', 'address', 'pincode')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)

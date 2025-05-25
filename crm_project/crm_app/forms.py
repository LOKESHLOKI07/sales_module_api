# crm_app/forms.py
from django import forms
from .models import Lead, CustomUser

from django import forms
from .models import Lead, CustomUser

class LeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Optional: for filtering users by department/role
        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = CustomUser.objects.all()

    class Meta:
        model = Lead
        fields = [
            'assigned_to', 'first_name', 'last_name', 'title', 'company',
            'email', 'secondary_email', 'email_opt_out',
            'phone', 'mobile', 'fax',
            'website', 'lead_source', 'industry', 'annual_revenue',
            'status', 'no_of_employees', 'rating',
            'skype_id', 'twitter',
            'street', 'city', 'state', 'zip_code', 'country',
            'description'
        ]




from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'department', 'password1', 'password2']


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

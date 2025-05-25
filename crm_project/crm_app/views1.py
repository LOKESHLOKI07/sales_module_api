from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import Lead, ActivityLog
from .forms import LeadForm, CustomUserCreationForm
from .filters import LeadFilter

import csv

from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomLoginForm

def custom_login_view(request):
    form = CustomLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login

    return render(request, 'login.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


def home(request):
    return render(request, 'home.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import csv
from .models import Lead
from .filters import LeadFilter  # Make sure this is correctly imported

@login_required
def lead_list(request):
    leads = Lead.objects.all()
    lead_filter = LeadFilter(request.GET, queryset=leads)
    leads = lead_filter.qs

    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Status', 'Assigned To'])

        for lead in leads:

            writer.writerow([
                lead.first_name,
                lead.email,
                lead.phone,
                lead.status,
                lead.assigned_to.username if lead.assigned_to else ''
            ])
        return response

    return render(request, 'lead_list.html', {'filter': lead_filter})

@login_required
def lead_create(request):
    form = LeadForm(request.POST or None, user=request.user)

    if form.is_valid():
        lead = form.save(commit=False)
        lead.created_by = request.user
        lead.save()

        ActivityLog.objects.create(
            user=request.user,
            action='created lead',
            lead=lead
        )

        return redirect('lead_list')

    return render(request, 'lead_form.html', {'form': form, 'action': 'Create'})

@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadForm(request.POST or None, instance=lead, user=request.user)

    if form.is_valid():
        form.save()

        ActivityLog.objects.create(
            user=request.user,
            action='updated lead',
            lead=lead
        )

        return redirect('lead_list')

    return render(request, 'lead_form.html', {'form': form, 'action': 'Update'})


@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == 'POST':
        ActivityLog.objects.create(
            user=request.user,
            action='deleted lead',
            lead=lead
        )

        lead.delete()
        return redirect('lead_list')

    return render(request, 'lead_confirm_delete.html', {'lead': lead})


from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Lead

@login_required
def dashboard(request):
    user = request.user

    # Role-based lead statistics
    if user.role == 'Super Admin':
        lead_stats = Lead.objects.values('status').annotate(total=Count('id'))
    elif user.role in ['Admin', 'Senior Manager']:
        lead_stats = Lead.objects.filter(
            assigned_to__department=user.department
        ).values('status').annotate(total=Count('id'))
    else:
        lead_stats = Lead.objects.filter(
            assigned_to=user
        ).values('status').annotate(total=Count('id'))

    # Unread notifications
    unread_notifications = user.notifications.filter(is_read=False)

    return render(request, 'dashboard.html', {
        'lead_stats': lead_stats,
        'unread_notifications': unread_notifications,
    })

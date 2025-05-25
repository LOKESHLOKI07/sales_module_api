# crm_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Extend Django User
# class CustomUser(AbstractUser):
#     role = models.CharField(max_length=50)
#     department = models.CharField(max_length=50)

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Role choices
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('sr_manager', 'Sr Manager'),
        ('asst_manager', 'Asst Manager'),
        ('sr_tl', 'Sr TL'),
        ('tl', 'TL'),
        ('executive', 'Executive'),
        ('associate', 'Associate'),
    ]

    # Department choices
    DEPARTMENT_CHOICES = [
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('hr', 'HR'),
        ('it', 'IT'),
        ('operations', 'Operations'),
        ('production', 'Production'),
        ('accounts', 'Accounts'),
        ('finance', 'Finance'),
        ('legal', 'Legal'),
        ('lnd', 'L&D'),
        ('rnd', 'R&D'),
        ('design', 'Design'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)



from django.db import models
from django.conf import settings

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
        ('won', 'Won'),
    ]

    RATING_CHOICES = [
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('cold', 'Cold'),
    ]

    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]

    SOURCE_CHOICES = [
        ('web', 'Web'),
        ('referral', 'Referral'),
        ('cold_call', 'Cold Call'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]

    # Lead Information
    lead_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='lead_owner')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    secondary_email = models.EmailField(blank=True, null=True)
    email_opt_out = models.BooleanField(default=False)
    fax = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    lead_source = models.CharField(max_length=50, choices=SOURCE_CHOICES, blank=True, null=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    no_of_employees = models.PositiveIntegerField(blank=True, null=True)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, blank=True, null=True)
    skype_id = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)

    # Address Information
    street = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Description
    description = models.TextField(blank=True, null=True)

    # System fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_leads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.last_name

# crm_app/models.py
from django.conf import settings  # ✅ Use this instead of from django.contrib.auth.models import User
from django.db import models
from .models import Lead  # Make sure this import works; or adjust accordingly

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.user} {self.action} on {self.lead.name}"

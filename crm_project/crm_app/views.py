# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import get_user_model, authenticate
# from django.db.models import Count
# from .models import Lead, ActivityLog
# from .serializers import LeadSerializer, ActivityLogSerializer, UserSerializer
#
# User = get_user_model()
#
# # --- Authentication & Registration ---
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     data = request.data
#     if User.objects.filter(username=data['username']).exists():
#         return Response({'error': 'Username already exists'}, status=400)
#     user = User.objects.create_user(username=data['username'], password=data['password'], email=data.get('email'))
#     return Response({'success': 'User created'}, status=201)
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     user = authenticate(username=request.data['username'], password=request.data['password'])
#     if user:
#         return Response({'success': 'Authenticated', 'user': UserSerializer(user).data})
#     return Response({'error': 'Invalid credentials'}, status=400)
#
#
# # --- Lead Views ---
#
# @api_view(['GET'])
# def lead_list(request):
#     leads = Lead.objects.all()
#     serializer = LeadSerializer(leads, many=True)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def lead_create(request):
#     serializer = LeadSerializer(data=request.data)
#     if serializer.is_valid():
#         lead = serializer.save(created_by=request.user)
#         ActivityLog.objects.create(user=request.user, action='created lead', lead=lead)
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def lead_detail(request, pk):
#     try:
#         lead = Lead.objects.get(pk=pk)
#     except Lead.DoesNotExist:
#         return Response({'error': 'Not found'}, status=404)
#
#     if request.method == 'GET':
#         return Response(LeadSerializer(lead).data)
#
#     elif request.method == 'PUT':
#         serializer = LeadSerializer(lead, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             ActivityLog.objects.create(user=request.user, action='updated lead', lead=lead)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         ActivityLog.objects.create(user=request.user, action='deleted lead', lead=lead)
#         lead.delete()
#         return Response({'success': 'Deleted'}, status=204)
#
#
# # --- Dashboard ---
#
# @api_view(['GET'])
# def dashboard(request):
#     user = request.user
#
#     if user.role == 'Super Admin':
#         lead_stats = Lead.objects.values('status').annotate(total=Count('id'))
#     elif user.role in ['Admin', 'Senior Manager']:
#         lead_stats = Lead.objects.filter(
#             assigned_to__department=user.department
#         ).values('status').annotate(total=Count('id'))
#     else:
#         lead_stats = Lead.objects.filter(
#             assigned_to=user
#         ).values('status').annotate(total=Count('id'))
#
#     unread_notifications = user.notifications.filter(is_read=False).count() if hasattr(user, 'notifications') else 0
#
#     return Response({
#         'lead_stats': lead_stats,
#         'unread_notifications': unread_notifications
#     })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import Lead, ActivityLog
from .serializers import LeadSerializer, ActivityLogSerializer, UserSerializer

User = get_user_model()

# --- Authentication & Registration ---
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()
from .serializers import RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'User created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Lead Views ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lead_list(request):
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lead_create(request):
    serializer = LeadSerializer(data=request.data)
    if serializer.is_valid():
        lead = serializer.save(created_by=request.user)
        ActivityLog.objects.create(user=request.user, action='created lead', lead=lead)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])

def lead_detail(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        return Response(LeadSerializer(lead).data)

    elif request.method == 'PUT':
        serializer = LeadSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            ActivityLog.objects.create(user=request.user, action='updated lead', lead=lead)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        ActivityLog.objects.create(user=request.user, action='deleted lead', lead=lead)
        lead.delete()
        return Response({'success': 'Deleted'}, status=204)


# --- Dashboard ---

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count

import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    logger.info(f'Dashboard accessed by user: {user}, role: {getattr(user, "role", None)}')

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

    unread_notifications = user.notifications.filter(is_read=False).count() if hasattr(user, 'notifications') else 0

    return Response({
        'lead_stats': lead_stats,
        'unread_notifications': unread_notifications
    })

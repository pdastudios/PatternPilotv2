from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from . import views

# Create a router and register the viewset
router = routers.DefaultRouter()
#router.register(r'shapes/', views.ShapeViewSet)

# Add URL patterns
urlpatterns = [
    # URL pattern for the function-based view
    path('pattern/', views.PatternView.as_view(), name='pattern_view'),
    path('track/', views.RoundViewSet.as_view({'get': 'list', 'post': 'create'}), name='track_view'),  # Specifying actions
    path('shapes/', views.ShapeViewSet.as_view({'get': 'list', 'post': 'create'}), name='shapes_view'),  # Specifying actions
    path('track/<int:pk>/', views.RoundViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='round-detail'),  # Endpoint for updating and deleting rounds
]

# Add router URLs to urlpatterns
urlpatterns += router.urls

# Catch-all route for serving Vue app
#urlpatterns += [
#    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
#]

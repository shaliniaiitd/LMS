from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Dummy API",
        default_version='v1',
        description="Dummy description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@dummy.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.books, name='view_books'),
    path('create/', views.add_books, name='add-books'),
    path('all/', views.view_books, name='view_books'),
    path('update/<int:pk>/', views.update_books, name='update-books'),
    path('book/<int:pk>/delete/', views.delete_books, name='delete-books'),
   path('login/', views.LoginView.as_view, name='login'),
    #path('logout/', views.LogoutView.as_view(), name='logout'),

]
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('users', views.UserViewSet, 'user-list')
# router.register('login', views.LoginView, 'login')


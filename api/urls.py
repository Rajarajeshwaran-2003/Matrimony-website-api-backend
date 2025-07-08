from django.urls import path
from .views import register_user,login_user,logout_user,create_profile,get_all_profiles,create_profile,ProfileDetailView,UpdateProfileView

urlpatterns = [
    path('register/', register_user, name = 'register'),
    path('login/', login_user, name='login'),
    path('logout/',logout_user, name='logout'),
    path('profiles/', create_profile, name='profile'),
    path('candidates/', get_all_profiles, name='candidates'),
    path('profile/<str:email>/', ProfileDetailView.as_view(), name='get-profile'),
    path('update/<str:email>/', UpdateProfileView.as_view(), name='update-profile'),
]
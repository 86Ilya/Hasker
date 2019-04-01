from django.urls import path

from Hasker.profile import views

urlpatterns = [
    path(r'login/', views.login_view, name="login"),
    path(r'logout/', views.logout_view, name="logout"),
    path(r'signup/', views.signup_view, name="signup"),
    path(r'settings/', views.settings_view, name="settings")]

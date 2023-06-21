from django.urls import path
from .views import *

urlpatterns = [
    path('add-userdetails/',UserView.as_view(),name="add-userdetails"),
    path('add-category/',CategoryView.as_view(),name="add-category"),
    path('add-product/',ProductView.as_view(),name="add-product"),
    path('add-userprofile/',UserDetailsView.as_view(),name="add-userprofile"),
    path('login/',LoginView.as_view(),name="login"),
    path('add-userproduct/',UserProductView.as_view(),name="add-userproduct"),
    path('password-reset/', SendPasswordResetLinkView.as_view(), name='password-reset'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),


]

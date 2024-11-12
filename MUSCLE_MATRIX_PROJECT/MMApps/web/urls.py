from django.urls import path
from MMApps.web.views import webViewsObject, authViewsObject

urlpatterns = [
    path('login/', authViewsObject.login_view, name='login_view'),
    path('register/', authViewsObject.register_view, name='register_view'),
    path('activate/<str:client_id>/<str:token>/', authViewsObject.activate_account, name='activate_account'),
    path('forgot-password/', authViewsObject.forgot_password_view, name='forgot_password_view'),
    path('otp-verification/', authViewsObject.otp_verification_view, name='otp_verification_view'),
    path('logout/',authViewsObject.logout,name='logout'),
    path('', webViewsObject.index_view, name='index_view'),
    path('services/', webViewsObject.services_view, name='services_view'),
    path('about-us/', webViewsObject.about_view, name='about_view'),
    path('contact-us/', webViewsObject.contact_view, name='contact_view'),
    path('profile/', webViewsObject.profile_view, name='profile_view'),
    path('edit-profile/', webViewsObject.edit_profile, name='edit_profile'),
    path('edit-profile-picture/', webViewsObject.edit_profile_picture, name='edit_profile_picture'),
    path('terms-of-service/', webViewsObject.terms_of_service_view, name='terms_of_service_view'),
] 
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView
urlpatterns=[
path('',views.home,name='home'),
path('spendings/<pk>',views.spendings_update,name='spendings_update'),
path('consolidate',views.consolidate,name='consolidate'),
path('register',views.register,name='register'),
path('login',views.user_login,name='login'),
path('logout',views.user_logout,name="logout"),
path("password_reset",PasswordResetView.as_view(template_name="SPT/password_reset.html"),name="password_reset"),
path("password_reset_done",PasswordResetDoneView.as_view(template_name="SPT/password_reset_done.html"),name="password_reset_done"),
path("password_reset_confirm/<uidb64>/<token>",PasswordResetConfirmView.as_view(template_name="SPT/password_reset_confirm.html"),name="password_reset_confirm"),
path("password_reset_complete",PasswordResetCompleteView.as_view(template_name="SPT/password_reset_complete.html"),name="password_reset_complete"),
path("remove_member/<pk>",views.remove_member,name="remove_member"),
path("remove_spending/<pk>",views.remove_spending,name="remove_spending"),
path("share_update/<pk>",views.member_share_update,name="share_update"),
]
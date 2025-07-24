from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', views.user_login, name='login'), # url for our custom login view in views.py
    # path(
    #     "login/", auth_views.LoginView.as_view(), name="login"
    # ),  # login view from djangos authentication framework
    # path(
    #     "logout/", auth_views.LogoutView.as_view(), name="logout"
    # ),  # logout view from djangos authentictaion framework
    # path("", views.dashboard, name="dashboard"),
    # # change password urls
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # # reset password urls
    # path(
    #     "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>/", views.user_detail, name="user_detail"),
]


"""The PasswordChangeView view will handle the form to change the password, and the
PasswordChangeDoneView view will display a success message after the user has successfully changed
their password. Let’s create a template for each view.
"""


"""Django provides URL patterns for the authentication views that are equivalent to the ones we just
created. We will replace the authentication URL patterns with the ones provided by Django.
Comment out the authentication URL patterns that you added to the urls.py file of the account appli-
cation and include django.contrib.auth.urls instead, as follows.
"""

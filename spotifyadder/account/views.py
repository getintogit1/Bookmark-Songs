from urllib.parse import quote
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

from social_django.models import UserSocialAuth


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate( 
                request, username=cd["username"], password=cd["password"]
            )  
            if user is not None:
                if user.is_active: 
                    login(
                        request, user
                    )  
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = (
            LoginForm()
        )  
    return render(
        request, "account/login.html", {"form": form}
    )  



def dashboard(request):
    # Count how many songs the user created/bookmarked
    total_songs = request.user.tracks_created.count()

    # Check if Spotify is connected
    try:
        spotify_login = request.user.social_auth.get(provider='spotify')
        spotify_connected = True
        # Try to grab the display name from extra_data
        spotify_name = spotify_login.extra_data.get('display_name')
        # If it's not in extra_data, you can also fetch it live:
        # from social_core.backends.spotify import SpotifyOAuth2
        # backend = SpotifyOAuth2()
        # token = spotify_login.get_access_token()['access_token']
        # spotify_profile = backend.user_data(token)
        # spotify_name = spotify_profile.get('display_name')
    except UserSocialAuth.DoesNotExist:
        spotify_connected = False
        spotify_name = None

    return render(request, "account/dashboard.html", {
        "total_songs": total_songs,
        "spotify_connected": spotify_connected,
        "spotify_name": spotify_name,
    })




def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})





@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        both_forms_are_valid = user_form.is_valid() and profile_form.is_valid()
        if both_forms_are_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully") # display custom succes message which get renderer in base.html 
        else:
            messages.error(request, "Error updating your profile") # display custom error message 
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )



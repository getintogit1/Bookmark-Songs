from urllib.parse import quote
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

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


@login_required()
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    # actions = []
    following_ids = request.user.following.values_list("id", flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)

    actions = actions.select_related("user", "user__profile").prefetch_related('target')[:10]
    
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
    
    print("Dashboard: found %d actions for user %r" % (actions.count(), request.user))
    return render(request, "account/dashboard.html", {
       
        "spotify_connected": spotify_connected,
        "spotify_name": spotify_name,
        "actions": actions
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
            create_action(
                new_user, "has created an account"
            )  # save action for activity tream
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






User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request, "account/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "account/user/detail.html", {"section": "people", "user": user}
    )


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import SongCreateForm, SongEditForm

from django.shortcuts import get_object_or_404
from .models import Song

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse


import requests
import json


from social_django.utils import load_strategy


@login_required
def song_create(request):
    if request.method == "POST":
        # form is sent
        form = SongCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_song = form.save(commit=False)
            # assign current user to the item
            new_song.user = request.user
            new_song.save()
            messages.success(request, "Song added successfully")
            # redirect to new created item detail view
            return redirect(new_song.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = SongCreateForm(data=request.GET)
    return render(request, "songs/song/create.html", {"section": "songs", "form": form})


def song_detail(request, id, slug):
    song = get_object_or_404(Song, id=id, slug=slug)
    return render(
        request,
        "songs/song/detail.html",
        {"section": "songs", "song": song},
    )


@login_required
@require_POST
def song_like(request):
    song_id = request.POST.get("id")
    action = request.POST.get("action")
    if song_id and action:
        try:
            song = Song.objects.get(id=song_id)
            if action == "like":
                song.users_like.add(request.user)
            else:
                song.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Song.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def song_list(request):
    if request.user.is_authenticated:
        songs = Song.objects.filter(user=request.user)
    else:
        songs = Song.objects.none()
    paginator = Paginator(songs, 8)
    page = request.GET.get("page")
    songs_only = request.GET.get("songss_only")
    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        songs = paginator.page(1)
    except EmptyPage:
        if songs_only:
            # If AJAX request and page out of range
            # return an empty page
            return HttpResponse("")
        # If page out of range return last page of results
        songs = paginator.page(paginator.num_pages)
    if songs_only:
        return render(
            request,
            "songs/song/list_songs.html",
            {"section": "songs", "songs": songs},
        )
    return render(
        request,
        "songs/song/list.html",
        {"section": "songs", "songs": songs},
    )


@login_required
def song_edit(request, pk):
    # fetch the song (and ensure it belongs to this user)
    song = get_object_or_404(Song, pk=pk)

    if song.user != request.user and not request.user.is_staff:
            messages.error(request, "You are not allowed to delete this song.")
            return redirect(song.get_absolute_url())
#request.POST only contains your text fields (titles, descriptions, etc.). request.FILES contains any uploaded files (your image).
    if request.method == "POST":
        song_form = SongEditForm(request.POST, request.FILES,instance=song)
        if song_form.is_valid():
            song_form.save()
            messages.success(request, "Song updated successfully")
            return redirect(song.get_absolute_url())
        else:
            messages.error(request, "Error updating your Song")
    else:
        song_form = SongEditForm(instance=song)

    return render(request, "songs/song/edit.html", {
        "section": "songs",
        "song_form": song_form,
        "song": song
    })

@login_required
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)

    if song.user != request.user and not request.user.is_staff:
        messages.error(request, "You are not allowed to delete this song.")
        return redirect(song.get_absolute_url())

    if request.method == "POST":
        title = song.title
        song.delete()
        messages.success(request, f'"{title}" was deleted.')
        return redirect('songs:list')

    # Optional: confirmation page (if you want a separate page)
    return render(request, "songs/song/confirm_delete.html", {"song": song})









SPOTIFY_BASE = "https://api.spotify.com/v1"
@login_required
@require_POST
def song_add_to_spotify(request, pk):
    song = get_object_or_404(Song, pk=pk)

    if song.user != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Not allowed'}, status=403)

    # 1. Get spotify social auth
    try:
        sa = request.user.social_auth.get(provider='spotify')
        print("hello", sa)
    except UserSocialAuth.DoesNotExist:
        return JsonResponse({'error': 'Spotify not connected'}, status=400)

    # 2. Get (and refresh) access token
    try:
        strategy = load_strategy()
        access = sa.get_access_token(strategy)
        print("Access: ", access)
        if isinstance(access, dict):
            access_token = access.get('access_token')
        else:
            access_token = access
    except Exception as e:
        return JsonResponse({'error': f'Cannot obtain access token: {e}'}, status=500)
   
    # 3. Parse JSON body
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        payload = {}

    title = (payload.get('title') or song.title).strip()
    artist = (payload.get('artist') or song.artist).strip()
    print("title: ", title)
    print("artist: ", artist)

    trackUri = getTrackUri(title,artist,access_token)
    print(trackUri)

    addToPlayList("My First Playlist", trackUri, access_token)






def fetchWebApi(endpoint, method, params, token, body=None, timeout=10, retry_on_401=True):
    """
    endpoint: may be 'search', 'me', 'playlists/{id}/tracks', or a full path starting with 'v1/'.
    params: dict for query string (use {} if none)
    body:   dict for JSON body (POST/PUT)
    """
    # Build full URL
    if endpoint.startswith("http"):
        url = endpoint
    else:
        # ensure exactly one / between base and endpoint
        endpoint = endpoint.lstrip('/')          # remove leading slash
        if not endpoint.startswith("v1/"):
            endpoint = "v1/" + endpoint
        url = f"{SPOTIFY_BASE}/{endpoint[3:]}"   # because SPOTIFY_BASE already ends with /v1
        # Alternative simpler:
        # url = f"https://api.spotify.com/{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    print("Body: ", body)
    data = json.dumps(body) if body is not None else None
    print("Data ", data)


    resp = requests.request(
        method.upper(),
        url,
        headers=headers,
        params=params or {},
        data=data,
        timeout=timeout
    )

    
    social_auth_obj=None

    if resp.status_code == 401 and retry_on_401 and social_auth_obj:
        # attempt refresh
        strategy = load_strategy()
        refreshed = social_auth_obj.refresh_token(strategy)
        new_token = refreshed.get('access_token') if isinstance(refreshed, dict) else refreshed
        if not new_token:
            raise RuntimeError("Could not refresh Spotify token")
        # retry once
        return fetchWebApi(
            endpoint, method, token=new_token, params=params, body=body,
            timeout=timeout, retry_on_401=False      )
    
    if resp.status_code < 200 or resp.status_code >= 300:
        raise RuntimeError(f"Spotify API {resp.status_code} error at {endpoint}: {resp.text[:200]}")
    try:
        return resp.json()
    except ValueError:
        return {}


def getTrackUri(title, artist, token):
    
    query = f'track:"{title}" artist:"{artist}"'
    payload = fetchWebApi(
        "search",
        "GET",
        {"q": query, "type": "track", "limit": 1}, 
        token,
       
       
)
    items = payload.get("tracks", {}).get("items", [])
    if items:
        return items[0]["uri"]

def addToPlayList(playlistName, trackUri, token): 
    playlist_description="Playlist created by app"
    public = False

    if not trackUri:
        raise RuntimeError("Track URI required")
    
   # 1. Current user
    me = fetchWebApi(
        "me",
       "GET",
        {},
        token=token,
    )
    user_id = me["id"]

    # 2. List existing playlists
    playlists = fetchWebApi(
        "me/playlists",
        method="GET",
        token=token,
        params={"limit": 50},
    )

    target_id = None
    for pl in playlists.get("items", []):
        if pl["name"] == playlistName:
            target_id = pl["id"]
            break

    # 3. Create if missing
    if not target_id:
        body = {
            "name": playlistName,
            "description": playlist_description,
            "public": public,
        }
        created = fetchWebApi(
            f"users/{user_id}/playlists",
            "POST",
            {},
            token=token,
            body=body,
        )
        target_id = created["id"]

    # 4. Add track (POST track URIs)
    fetchWebApi(
        f"playlists/{target_id}/tracks",
        "POST",
        {},
        token=token,
        body={"uris": [trackUri]},
    )

    return target_id 


def get_token(user):
    """
    Return a *fresh* Spotify access token string for the given user.
    Uses social-auth-app-django to refresh if expired.

    Raises RuntimeError if the user is not connected.
    """
    try:
        sa = user.social_auth.get(provider='spotify')
    except UserSocialAuth.DoesNotExist:
        raise RuntimeError("Spotify not connected for this user")

    # Different versions of social-auth may have different signatures/returns.
    access_obj = sa.get_access_token()  # no args for modern versions
    if isinstance(access_obj, dict):
        token = access_obj.get("access_token")
    else:
        token = access_obj
    if not token:
        # very old versions might require strategy
        try:
            access_obj = sa.get_access_token(load_strategy())
            token = access_obj.get("access_token") if isinstance(access_obj, dict) else access_obj
        except Exception as e:
            raise RuntimeError(f"Cannot obtain access token: {e}")
    if not token:
        raise RuntimeError("Empty access token")
    return token

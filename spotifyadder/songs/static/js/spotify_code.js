// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
// const token = 'BQBRo_rT1Q1lL3ydT8oV3NwH-mncmZrTHZUxGO3lN3LXnhFI-1YJ3K1Xjmws7qVPBEcgUCbNZYlhJAEwBbEvbFbwfL6oJd8RbTgOO36p8bbvr_KnBbcNH1UcUrW2Xt2wCRTP9yi1QzP4sVNhEPrDo-p2FAhR50jQeLYfYAoGSlX8q6r7w2l69t_--ihPHfF9Mh2w4nMterMjEL7EBhWWkQ32ulPZ3VMBcBwyP0k5zucAbB-aK4qN1vHMKr0xXwymBnw1qiYS55_mktwxiYsryROqt1-UDjQ9Gtn0InuK8Q';
//
//
// async function fetchWebApi(endpoint, method, body) {
//   const res = await fetch(`https://api.spotify.com/${endpoint}`, {
//     headers: {
//       Authorization: `Bearer ${token}`,
//     },
//     method,
//     body:JSON.stringify(body)
//   });
//   return await res.json();
// }
//
// async function getCurrentTracks(){
//   // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
//   return (await fetchWebApi(
//     'v1/me/top/tracks?time_range=long_term&limit=5', 'GET'
//   )).items;
// }
//
//
// const tracksUri = [
//   'spotify:track:3D7vG5gCxppzAvawI3fJXC','spotify:track:2W5Ee8qMHz0QXV1h7cChbH','spotify:track:2FostOdJkjQ9MvOudhqMyH','spotify:track:2CPj8R9uFPKylqRJonbcfU','spotify:track:2DGixD1h7x1ZoPhRjpiko9'
// ];
//
// async function createPlaylist(tracksUri){
//   const { id: user_id } = await fetchWebApi('v1/me', 'GET')
//
//   const playlist = await fetchWebApi(
//     `v1/users/${user_id}/playlists`, 'POST', {
//       "name": "My Bookmarked tracks playlist",
//       "description": "Playlist with songs i have bookmarked from the internet.",
//       "public": false
//   })
//
//   await fetchWebApi(
//     `v1/playlists/${playlist.id}/tracks?uris=${tracksUri.join(',')}`,
//     'POST'
//   );
//
//   return playlist;
// }
//
// const createdPlaylist = await createPlaylist(tracksUri);
// console.log(createdPlaylist.name, createdPlaylist.id);




document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('add-to-spotify-btn');
  if (!btn) return;
  const statusEl = document.getElementById('spotify-status');

  btn.addEventListener('click', async () => {
    statusEl.textContent = 'Adding…';
    btn.disabled = true;

    const payload = {
      title: btn.dataset.title,
      artist: btn.dataset.artist
    };

    const csrfToken = getCSRFToken();
    console.log('CSRF token:', csrfToken);      
    const res = await fetch(`/songs/${btn.dataset.songId}/add-to-spotify/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload)
      });
        console.log(payload);
    })
})

function getCSRFToken() {
  const name = 'csrftoken=';
  return document.cookie.split(';').map(c=>c.trim()).find(c=>c.startsWith(name))?.slice(name.length) || '';
}


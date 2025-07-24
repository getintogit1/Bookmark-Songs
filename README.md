**Spotify Adder & Bookmark Web App**

A Django-based web application that allows users to:

* Register/login using Google OAuth2 or an email/password.
* Connect their Spotify account to the app.
* Bookmark songs from YouTube videos into their personal song library.
* Add saved songs to a Spotify playlist with one click.
* Discover other users’ profiles, view their saved songs, and like or save them to their own playlists.
* Follow and unfollow other users and view a real-time activity feed of follow/unfollow events and image likes.
* See a global ranking of most-viewed songs powered by Redis.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [License](#license)

---

## Features

* **User Authentication**: Login with Google OAuth2 or email/password.
* **Spotify Integration**: Connect to Spotify and fetch user profile and playlists.
* **YouTube Bookmarking**: Save song bookmarks from YouTube videos via a JavaScript bookmarklet.
* **Song Library**: Manage a personal library of bookmarked songs.
* **One-Click Spotify Playlist**: Add saved songs to a Spotify playlist instantly.
* **User Discovery**: Browse other users’ profiles, saved songs, and like or save them.
* **Social Feed**: Real-time feed of follow/unfollow and like actions of users you follow.
* **Redis Rankings**: A global leaderboard of the most-bookmarked songs powered by Redis.

---

## Tech Stack

* **Backend**: Django, Django REST Framework
* **Frontend**: Django Templates, JavaScript (ES6)
* **Auth**: Django Allauth (Google OAuth2), Django auth
* **Spotify API**: `social-auth-app-django` with Spotify OAuth2 backend
* **YouTube Bookmarklet**: Custom JavaScript bookmarklet
* **Real-Time Feed**: Django channels (optional) or AJAX polling
* **Database**: PostgreSQL
* **Cache & Ranking**: Redis
* **Deployment**: Docker, Gunicorn, Nginx

---

## Prerequisites

* Python 3.10+
* PostgreSQL
* Redis
* Node.js and npm (for frontend build if needed)
* Docker & Docker Compose (optional)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/spotify-adder-webapp.git
   cd spotify-adder-webapp
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install and run Redis and PostgreSQL**

   * Using Docker Compose:

     ```bash
     docker-compose up -d
     ```

---

## Configuration

1. **Environment Variables**
   Create a `.env` file in the project root and add:

   ```ini
   DEBUG=True
   SECRET_KEY=your-django-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/dbname
   REDIS_URL=redis://localhost:6379/0
   SPOTIFY_KEY=your-spotify-client-id
   SPOTIFY_SECRET=your-spotify-client-secret
   ```

2. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

3. **Collect static files**

   ```bash
   python manage.py collectstatic
   ```

4. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## Usage

1. **Sign Up / Login**: Register using Google or email.
2. **Connect Spotify**: Go to Dashboard → Connect Spotify.
3. **Bookmark a Song**: Drag the provided bookmarklet to your browser’s bookmarks bar. While on a YouTube video, click the bookmarklet to save the song.
4. **View Library**: In your Dashboard, view your saved songs, like others’ songs, or add them to your Spotify playlist.
5. **Discover Users**: Browse Users → View Profiles → Follow / Unfollow.
6. **Activity Feed**: See what your followings are doing in real time.
7. **Rankings**: View the global Redis-powered leaderboard in the Rankings page.

---

## Testing

```bash
pytest
```

---

## Deployment

1. **Build Docker image**

   ```bash
   docker build -t spotify-adder-webapp .
   ```
2. **Run with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

---

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

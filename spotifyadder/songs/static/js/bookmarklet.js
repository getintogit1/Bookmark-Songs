function bookmarkletLaunch() {
  const siteUrl = 'https://127.0.0.1:8000/';

  // 1) Remove existing UI if present
  const old = document.getElementById('bookmarklet');
  if (old) old.remove();

  // 2) Inject CSS once
  if (!document.getElementById('bm-css')) {
    const link = document.createElement('link');
    link.id   = 'bm-css';
    link.rel  = 'stylesheet';
    link.href = siteUrl + 'static/css/bookmarklet.css?r=' + Date.now();
    document.head.appendChild(link);
  }

  // 3) Build container
  const box = document.createElement('div');
  box.id = 'bookmarklet';
  Object.assign(box.style, {
    position:   'fixed',
    top:        '10%',
    right:      '10%',
    width:      '300px',
    background: '#fff',
    border:     '1px solid #666',
    padding:    '10px',
    zIndex:     999999
  });
  box.innerHTML = `
    <a href="#" id="close" style="float:right">×</a>
    <h1>Select a song</h1>
    <div class="entries"></div>
  `;
  document.body.appendChild(box);

  // 4) Close button
  box.querySelector('#close').addEventListener('click', e => {
    e.preventDefault();
    box.remove();
  });

  // 5) Pick up the title
  let title = document.title;
  const ytEl = document.querySelector('#title yt-formatted-string');
  if (ytEl) title = ytEl.textContent.trim();

  // 6) Render entry and hook click
  const entry = document.createElement('a');
  entry.href         = '#';
  entry.textContent  = title;
  entry.style.display = 'block';
  entry.style.margin  = '10px 0';
  box.querySelector('.entries').appendChild(entry);

  entry.addEventListener('click', e => {
    e.preventDefault();
    window.open(
      siteUrl + 'songs/create/?title=' + encodeURIComponent(title),
      '_blank'
    );
    box.remove();
  });
}

// Immediately launch on first injection
bookmarkletLaunch();

# AI News Website

A responsive website that displays the latest AI news, updated daily at 7 AM.

## Features
- Automatically fetches AI news from predefined sources.
- Saves news data as JSON files, one per day.
- Responsive design for both mobile and desktop.

## Project Structure
```
AiNews/
├── frontend/          # Frontend code (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── backend/          # Backend code (Python scripts)
│   ├── fetch_news.py
│   └── server.py
├── data/             # Daily news JSON files
└── README.md
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install Python 3.10.
3. Install required Python packages:
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage
1. **Run the crawler** (manually or via Cron Job):
   ```bash
   python backend/fetch_news.py
   ```
2. **Start the web server**:
   ```bash
   python backend/server.py
   ```
3. Open `http://localhost:8000` in your browser.

## Cron Job Setup (Ubuntu)
To run the crawler daily at 7 AM:
```bash
crontab -e
```
Add the following line:
```
0 7 * * * /usr/bin/python3 /path/to/backend/fetch_news.py
```

## Notes
- Replace the news source URL in `fetch_news.py` with an actual AI news website.
- Ensure the `data/` directory exists and is writable.
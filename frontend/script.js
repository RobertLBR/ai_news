// Fetch news data from the server
fetch('/news')
    .then(response => response.json())
    .then(data => {
        const newsContainer = document.getElementById('news-container');
        data.forEach(news => {
            const newsItem = document.createElement('div');
            newsItem.className = 'news-item';
            newsItem.innerHTML = `
                <h2>${news.title}</h2>
                <p>${news.summary}</p>
                <a href="${news.url}" target="_blank">Read more</a>
            `;
            newsContainer.appendChild(newsItem);
        });
    })
    .catch(error => console.error('Error fetching news:', error));
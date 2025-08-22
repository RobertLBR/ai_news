docker build -t ai_news .
docker ps -a | grep -q ai_news && docker rm -f ai_news
docker run -d --name ai_news \
-p 8000:8000 \
-v $(pwd)/data:/usr/src/app/data \
ai_news

web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 main:app
worker: python worker.py
clock: python clock.py

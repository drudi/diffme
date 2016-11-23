import bottle
from api import endpoints

app = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host = '0.0.0.0', port = 8000)

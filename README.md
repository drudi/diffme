# diffme
Compute the diff between two API calls

CI running on https://travis-ci.org/drudi/diffme
![ci status](https://api.travis-ci.org/drudi/diffme.svg?branch=master)

This API uses the Bottle framework, and redis to keep data between requests.

To generate data for testing, use the following command line:

```sh
$ python -c "import base64,pickle;print(base64.b64encode(pickle.dumps({'foo': 'world', 'bar':'1234'})))"
b'gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu'
$
```
and copy whats inside the single quotes to use as input data for the api calls, i.e.:

```
gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu
```

## Running locally for development

In order to run this project for development, first create a python virtual environment. A python interpreter version 3.5 and the virtualenv executable are needed as well as pip. You'll also need Docker installed. Assuming those three are installed on your OS, follow the steps below to set up your development environment:

```sh
$ git clone https://github.com/drudi/diffme.git
$ cd diffme
$ virtualenv -p `which python3` env
$ . env/bin/activate
$ pip install -r requirements.txt
$ # Execute a redis container locally
$ docker run -d -p 0.0.0.0:6379:6379 redis:latest
$ # Configure envvar with the redis host
$ export REDIS_HOST=127.0.0.1
$ sh run_api.sh
```



## Build a docker image and run it locally

You can also build a Docker container and run it locally. It uses 2 images and uses docker-compose to bring up the environment. To do so run the commands bellow inside the diffme directory:

```sh
$ docker-compose build
$ docker-compose start
```

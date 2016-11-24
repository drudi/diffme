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

For running the tests:

```sh
$ sh run_tests.sh
```


## Build a docker image and run it locally

You can also build a Docker container and run it locally. It uses 2 images (the api image and a redis image) and uses docker-compose to bring up the environment. To do so run the commands bellow inside the diffme directory:

```sh
$ docker-compose build
$ docker-compose up
```

The API will be available on localhost and port 8000. Some example calls to the api are:

```sh
$ curl -XPUT http://127.0.0.1:8000/v1/diff/right -d "gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu"
{"bar": "1234", "foo": "world"}

$ curl -XPUT http://127.0.0.1:8000/v1/diff/left -d "gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu"
{"bar": "1234", "foo": "world"}

$ curl -XGET http://127.0.0.1:8000/v1/diff
{"equal": true, "diffs": [], "same_size": true}
```

## Docker image on Docker HUB

The CI process builds the image, and publishes it on Docker HUB. It can be found on https://hub.docker.com/r/mdrudi/diffme/tags/

To pull the the latest image:

```sh
$ docker pull mdrudi/diffme:latest
```

## The deployment

The deployment automation is not finished yet. But a server was set up in Digital Ocean to host the API. The process used to deploy the application to this server was:

- Copy docker-compose.yml.deploy file to docker-compose.yml in the production server
- execute 'docker pull redis:latest' and 'docker pull mdrudi/diffme:latest' in the server
- Stop the containers with 'docker-compose stop'
- As a privileged user, execute the command 'docker-compose up -d'

The server can be accessed through the URL http://diffme.drudi.org/v1/diff

Some example calls:

```sh
$ curl -XPUT http://diffme.drudi.org/v1/diff/right -d "gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu"
{"bar": "1234", "foo": "world"}

$ curl -XPUT http://diffme.drudi.org/v1/diff/left -d "KGRwMApTJ2ZvdScKcDEKUyd3b3JsZCcKcDIKc1MnYmFyJwpwMwpTJzU2NzgnCnA0CnMu"
{"bar": "5678", "fou": "world"}

$ curl -XGET http://diffme.drudi.org/v1/diff
{"diffs": [[9, 4], [19, 1]], "equal": false, "same_size": true}
```

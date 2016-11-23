# diffme
Compute the diff between two API calls


This API uses the Bottle framework, and redis to keep the data.

To generate data for testing, use the following command line:

```sh
$ python -c "import base64,pickle;print(base64.b64encode(pickle.dumps({'foo': 'world', 'bar':'1234'})))"
b'gAN9cQAoWAMAAABiYXJxAVgEAAAAMTIzNHECWAMAAABmb29xA1gFAAAAd29ybGRxBHUu'
$
```
and copy whats inside the single quotes

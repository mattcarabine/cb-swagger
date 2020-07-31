The example below uses a URL-encoded query parameter.

*Curl request*

``` shell
$ curl -v -u Administrator:password -X GET http://10.143.202.102:8095/analytics/service/analytics/service?statement=SELECT%20%22hello%2C%20beer%21%22%20AS%20greeting
```

The example below makes exactly the same request in a more human-readable form.
It uses the `--data-urlencode` option to URL-encode the parameter, and the `--get` option to append the parameter to the query component of the request.

*Curl request*

``` shell
$ curl -v -u Administrator:password -X GET http://10.143.202.102:8095/analytics/service --get --data-urlencode 'statement=SELECT "hello, beer!" AS greeting'
```

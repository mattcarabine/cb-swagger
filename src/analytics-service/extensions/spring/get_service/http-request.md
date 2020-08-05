The example below uses a URL-encoded query parameter.
The N1QL statement is `SELECT "hello, beer!" AS greeting`.

*Curl request*

``` shell
$ curl -v -u Administrator:password http://localhost:8095/analytics/service?statement=SELECT%20%22hello%2C%20beer%21%22%20AS%20greeting
```

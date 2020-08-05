The example below uses URL-encoded data.

*Curl request*

``` shell
$ curl -v -u Administrator:password --data-urlencode "statement=select 1;" http://localhost:8095/analytics/service
```

The example below posts the same query statement as data of type `application/json` and adds a client context ID.

*Curl request*

``` shell
$ curl -v -u Administrator:password -H "Content-Type: application/json" -d '{
    "statement":"select 1;",
    "pretty":true,
    "client_context_id":"xyz"
}' http://localhost:8095/analytics/service
```
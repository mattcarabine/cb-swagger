*Curl request*

``` shell
$ curl -v -u Administrator:password -X GET http://localhost:8095/analytics/service -d 'statement=SELECT "hello, beer!" AS greeting' -d 'logical-plan=true' -d 'optimized-logical-plan=true'
```

The example below queries all links in the `travel-sample.inventory` scope.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       http://localhost:8095/analytics/link?scope='`travel-sample`.inventory'
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
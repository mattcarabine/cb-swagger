The example below deletes the link named `myCbLink` from the `travel-sample.inventory` scope.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X DELETE http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myCbLink
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.

The example below deletes the link named `myAwsLink` from the `travel-sample.inventory` scope.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X DELETE http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myAwsLink
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
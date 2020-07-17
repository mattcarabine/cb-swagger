The example below deletes the link named `myCbLink` from the `Default` dataverse.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X DELETE http://localhost:8095/analytics/link \
       -d dataverse=Default \
       -d name=myCbLink
```

The example below deletes the link named `myAwsLink` from the `Default` dataverse.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X DELETE http://localhost:8095/analytics/link \
       -d dataverse=Default \
       -d name=myAwsLink
```

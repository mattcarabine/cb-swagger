The example below queries all links in the `Default` dataverse.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X GET http://localhost:8095/analytics/link \
       -d dataverse=Default
```

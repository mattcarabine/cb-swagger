The example below edits the link named `myCbLink` in the `Default` dataverse to use full encryption with a client certificate and client key.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X PUT http://localhost:8095/analytics/link \
       -d dataverse=Default \
       -d name=myCbLink \
       -d type=couchbase \
       -d hostname=remoteHostName:8091 \
       -d encryption=full \
       --data-urlencode "certificate=$(cat ./cert/targetClusterRootCert.pem)" \
       --data-urlencode "clientCertificate=$(cat ./cert/clientCert.pem)" \
       --data-urlencode "clientKey=$(cat ./cert/client.key)"
```

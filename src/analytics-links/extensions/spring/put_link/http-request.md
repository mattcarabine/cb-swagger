The example below edits the link named `myCbLink` in the `travel-sample.inventory` scope to use full encryption with a client certificate and client key.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X PUT http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myCbLink \
       -d type=couchbase \
       -d hostname=remoteHostName:8091 \
       -d encryption=full \
       --data-urlencode "certificate=$(cat ./cert/targetClusterRootCert.pem)" \
       --data-urlencode "clientCertificate=$(cat ./cert/clientCert.pem)" \
       --data-urlencode "clientKey=$(cat ./cert/client.key)"
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
The `certificate`, `clientCertificate`, and `clientKey` parameters use command substitution with the `cat` command to return the _content_ of the referenced files.
The content of these files is then URL-encoded to escape any special characters.

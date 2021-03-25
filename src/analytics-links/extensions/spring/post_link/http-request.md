The example below creates a Couchbase link named `myCbLink` in the `travel-sample.inventory` scope, with no encryption.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X POST http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myCbLink \
       -d type=couchbase \
       -d hostname=remoteHostName:8091 \
       -d encryption=none \
       --data-urlencode username=remote.user \
       --data-urlencode password=remote.p4ssw0rd
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
The `username` and `password` parameters are URL-encoded to escape any special characters.

The example below creates an Amazon S3 link named `myAwsLink` in the `travel-sample.inventory` scope.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X POST http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myAwsLink \
       -d type=s3 \
       -d region=us-east-1 \
       -d accessKeyId=myAccessKey \
       --data-urlencode secretAccessKey=mySecretKey
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
The `secretAccessKey` parameter is URL-encoded to escape any special characters.

The example below creates an Amazon S3 link named `myTempLink` with temporary credentials in the `travel-sample.inventory` scope.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X POST http://localhost:8095/analytics/link \
       -d scope='`travel-sample`.inventory' \
       -d name=myTempLink \
       -d type=s3 \
       -d region=eu-west-1 \
       -d accessKeyId=myTempAccessKey \
       -d sessionToken=mySessionToken \
       --data-urlencode secretAccessKey=myTempSecretKey
```

NOTE: The `scope` value is wrapped in single quotes to escape the backticks.
The `secretAccessKey` parameter is URL-encoded to escape any special characters.

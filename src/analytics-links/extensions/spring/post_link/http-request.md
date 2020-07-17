The example below creates a Couchbase link named `myCbLink` in the `Default` dataverse, with no encryption.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X POST http://localhost:8095/analytics/link \
       -d dataverse=Default \
       -d name=myCbLink \
       -d type=couchbase \
       -d hostname=remoteHostName:8091 \
       -d encryption=none \
       -d username=Administrator \
       -d password=password
```

The example below creates an Amazon S3 link named `myAwsLink` in the `Default` dataverse.

*Curl request*

``` shell
$ curl -v -u Administrator:password \
       -X POST http://localhost:8095/analytics/link \
       -d dataverse=Default \
       -d name=myAwsLink \
       -d type=s3 \
       -d region=us-east-1 \
       -d accessKeyId=myAccessKey \
       --data-urlencode secretAccessKey=mySecretKey
```

NOTE: The `secretAccessKey` parameter is URL-encoded to escape any special characters.
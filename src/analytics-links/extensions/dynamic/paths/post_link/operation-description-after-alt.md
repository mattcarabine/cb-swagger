When creating or altering a remote link using an alternate address, note the following:

* At least one node in the remote cluster must expose the `mgmt` port (`rest_port`, default 8091) or the `mgmtSSL` port (`ssl_rest_port`, default 18091).
* Furthermore, *all* data nodes in the remote cluster must expose the `kv` port (`memcached_port`, default 11210) or the `kvSSL` port (`memcached_ssl_port`, default 11207).

Failure to do so will result in a 400 (Bad Request) error.

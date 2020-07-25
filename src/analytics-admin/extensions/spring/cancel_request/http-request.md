The example below uses the `client_context_id` used in the [Query Service](rest-service.html#query-service) example to identify the request.

*Curl request*

``` shell
$ curl -v -u Administrator:password -X DELETE http://localhost:8095/analytics/admin/active_requests -d client_context_id=xyz
```

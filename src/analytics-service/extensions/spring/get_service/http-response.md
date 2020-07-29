*Response 200*

``` json
{
  "requestID": "f59afe63-fd6b-42b8-9aaf-5a2f33d1a53a",
  "signature": {
    "*": "*"
  },
  "results": [ { "greeting": "hello, beer!" }
 ]
  ,
  "plans":{"logicalPlan": {
   "operator" : "distribute-result",
   "expressions" : [ "$$2" ],
   "operatorId" : "1.1",
   "execution-mode" : "UNPARTITIONED",
   "inputs" : [ {
      "operator" : "project",
      "variables" : [ "$$2" ],
      "operatorId" : "1.2",
      "execution-mode" : "UNPARTITIONED",
      "inputs" : [ {
         "operator" : "assign",
         "variables" : [ "$$2" ],
         "expressions" : [ "{\"greeting\": \"hello, beer!\"}" ],
         "operatorId" : "1.3",
         "execution-mode" : "UNPARTITIONED",
         "inputs" : [ {
            "operator" : "empty-tuple-source",
            "operatorId" : "1.4",
            "execution-mode" : "UNPARTITIONED"
         } ]
      } ]
   } ]
},"optimizedLogicalPlan": {
   "operator" : "distribute-result",
   "expressions" : [ "$$2" ],
   "operatorId" : "1.1",
   "physical-operator" : "DISTRIBUTE_RESULT",
   "execution-mode" : "UNPARTITIONED",
   "inputs" : [ {
      "operator" : "exchange",
      "operatorId" : "1.2",
      "physical-operator" : "ONE_TO_ONE_EXCHANGE",
      "execution-mode" : "UNPARTITIONED",
      "inputs" : [ {
         "operator" : "assign",
         "variables" : [ "$$2" ],
         "expressions" : [ "{ greeting: \"hello, beer!\" }" ],
         "operatorId" : "1.3",
         "physical-operator" : "ASSIGN",
         "execution-mode" : "UNPARTITIONED",
         "inputs" : [ {
            "operator" : "empty-tuple-source",
            "operatorId" : "1.4",
            "physical-operator" : "EMPTY_TUPLE_SOURCE",
            "execution-mode" : "UNPARTITIONED"
         } ]
      } ]
   } ]
}},
  "status": "success",
  "metrics": {
    "elapsedTime": "52.755839ms",
    "executionTime": "47.108628ms",
    "resultCount": 1,
    "resultSize": 31,
    "processedObjects": 0
  }
}
```

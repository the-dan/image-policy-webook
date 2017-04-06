Image Policy Webhook Impl
===========================

Checks if image is in one of the allowed repositories.

See https://kubernetes.io/docs/admin/admission-controllers/#imagepolicywebhook

Usage
------
```
$ python main.py -h
$ python main.py myrepo
```

Example
-------

```
httpie POST http://localhost:8090/ @request-ok.json | jq
{
  "apiVersion": "imagepolicy.k8s.io/v1alpha1",
  "kind": "ImageReview",
  "status": {
    "reason": "",
    "allowed": true
  }
}
```


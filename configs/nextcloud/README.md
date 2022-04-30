This is just a quick section to document getting nextcloud up and running.

# Via HELM
Assumably you've already updated the s3 secrets for your specific setup in `nextcloud-values-SAMPLE.yml` and have now moved it to `nextcloud-values.yml`.


*Note: my config is working with BackBlaze, and not AWS. For docs on that hit [this place](https://help.backblaze.com/hc/en-us/articles/360047277954-How-do-I-use-NextCloud-with-B2-Cloud-Storage)*

So, anyway, this was my working command:
```bash
# note: ncattempt9 can be any name you want
helm install ncattempt9 nextcloud/nextcloud -f nextcloud-values.yml
```

Which should produce something like this:
```bash
NAME: ncattempt9
LAST DEPLOYED: Fri Apr 29 11:41:15 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the nextcloud URL by running:

  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=nextcloud" -o jsonpath="{.items[0].metadata.name}")
  echo http://127.0.0.1:8080/
  kubectl port-forward $POD_NAME 8080:80

2. Get your nextcloud login credentials by running:

  echo User:     admin
  echo Password: $(kubectl get secret --namespace default ncattempt9-nextcloud -o jsonpath="{.data.nextcloud-password}" | base64 --decode)

```

I installed this all on a small kind cluster. You can find kind notes in the notes directory of this repo.

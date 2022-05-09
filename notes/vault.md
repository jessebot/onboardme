# Hashicorp Vault

HCV is a secure key/secret store that can be self-hosted or run from the cloud. it's open-source and pretty much the best option for free KV's at the moment.

## Install

Mac:
```zsh
brew tap hashicorp/tap
brew install hashicorp/tap/vault
```

Linux
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```


## usage

Start the dev server and export the address + token to the ENV

```zsh
vault server -dev
export VAULT_ADDR='http://127.0.0.1:8200'

Unseal Key: /oUq84n6azQU0JqPRh+UlWCG2hOEPnvAQENeU5t1OcM=
Root Token: hvs.Zc0JUOYkD0C09nLeefC90Gim

export VAULT_TOKEN="hvs.Zc0JUOYkD0C09nLeefC90Gim"

```

Create a Secret:

```zsh
vault kv put secret/test_secret VAULT_TOKEN="hvs.Zc0JUOYkD0C09nLeefC90Gim"
```

Get a secret's data

```zsh
vault kv get secret/test_secret

===== Secret Path =====
secret/data/test_secret

======= Metadata =======
Key                Value
---                -----
created_time       2022-05-09T15:28:33.457932Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

======= Data =======
Key            Value
---            -----
VAULT_TOKEN    hvs.Zc0JUOYkD0C09nLeefC90Gim
```

Get only a specific field fo data

```zsh
vault kv get -field=VAULT_TOKEN secret/test_secret
hvs.Zc0JUOYkD0C09nLeefC90Gim
```
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

pip
```
pip3 install hvac
pip3 install pyhcl
```

## usage

1. Create a folder for the storage backend

```zsh 
mkdir -p vault/data
```

* Create a config.hcl file for the vault server

```hcl
ui = true
disable_mlock = true

storage "raft" {
  path    = "./vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
```

* Start the server 

```zsh
vault server -config=config.hcl

==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.17.9
              Listener 1: tcp (addr: "0.0.0.0:8200", cluster address: "0.0.0.0:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: false, enabled: false
           Recovery Mode: false
                 Storage: raft (HA available)
                 Version: Vault v1.10.2
             Version Sha: 94325865b12662cb72efa3003d6aaa4f5ae57f3a

==> Vault server started! Log data will stream in below:

2022-05-10T09:44:56.152+0200 [INFO]  proxy environment: http_proxy="" https_proxy="" no_proxy=""
2022-05-10T09:44:56.192+0200 [INFO]  core: Initializing versionTimestamps for core

```

* Export the vault address and initialize

```zsh
export VAULT_ADDR='http://127.0.0.1:8200'
vault operator init

# only works on new vaults
# example output

vault operator init
Unseal Key 1: wNDlQpiz6m7kYbo++j8bPQWWp1wEqXwclv8PMEzLiY8q
Unseal Key 2: 2wbERwNj8GHsuN7gm2MDf8F6k4ttnMhDqUAMZaa6go5M
Unseal Key 3: O1FG9J7NKAGoa7j+RS1tkX2EjaqO0juet/xFqCxtaHdL
Unseal Key 4: LqdJmBcFsQg3U1KMpJeSuCEWzAt5x7NnHqQpE3ytYgHz
Unseal Key 5: bGjpKcBKTJ02Wtf2AtSAnIMF+7jomMDZvnsLNpM5Aery

Initial Root Token: hvs.H7JknpNgEqDVtoSFNLFB5qnc

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated root key. Without at least 3 keys to
reconstruct the root key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```

* Unseal the vault

3 keys are required to unseal the vault

```zsh
export UNSEAL_KEY_1=wNDlQpiz6m7kYbo++j8bPQWWp1wEqXwclv8PMEzLiY8q
export UNSEAL_KEY_2=2wbERwNj8GHsuN7gm2MDf8F6k4ttnMhDqUAMZaa6go5M
export UNSEAL_KEY_3=O1FG9J7NKAGoa7j+RS1tkX2EjaqO0juet/xFqCxtaHdL
export UNSEAL_KEY_4=LqdJmBcFsQg3U1KMpJeSuCEWzAt5x7NnHqQpE3ytYgHz
export UNSEAL_KEY_5=bGjpKcBKTJ02Wtf2AtSAnIMF+7jomMDZvnsLNpM5Aery

vault operator unseal $UNSEAL_KEY_1
vault operator unseal $UNSEAL_KEY_2
vault operator unseal $UNSEAL_KEY_3

Key                     Value
---                     -----
Seal Type               shamir
Initialized             true
Sealed                  false
Total Shares            5
Threshold               3
Version                 1.10.2
Storage Type            raft
Cluster Name            vault-cluster-a9ab480b
Cluster ID              a864af72-bca1-4891-5a7c-35fa259b22e8
HA Enabled              true
HA Cluster              n/a
HA Mode                 standby
Active Node Address     <none>
Raft Committed Index    31
Raft Applied Index      31
```


* Open the UI

```zsh
http://127.0.0.1:8200/ui
```

* Create a Secret:

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
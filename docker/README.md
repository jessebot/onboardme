# Files for building onboardme docker containers

```
├──  arm_config
│   ├──  config.yml
│   ├──  default-onboardme-install.sh
│   ├──  devops-onboardme-install.sh
│   ├──  music-onboardme-install.sh
│   └──  packages.yml
├──  config.conf
├──  Dockerfile
└──  Dockerfile.arm
```

- `config.conf` is a special fastfetch config used for both docker images

- `Dockerfile` is for linux/amd64

- `Dockerfile.arm` is for linux/arm64 and linux/aarch64
- `arm_config` is a directory of files just for arm builds, including the default onboardme configs  for different package groups, installed via source if there's no package manager package.

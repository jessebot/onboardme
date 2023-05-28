# Files for building onboardme docker containers

```
├──  arm_config
│   ├──  config.yml
│   └──  packages.yml
├──  config.conf
├──  Dockerfile
└──  Dockerfile.arm
```

- Dockerfile is for linux/amd64

- Dockerfile.arm is for linux/arm64 and linux/aarch64
- arm_config is a directory of files just for arm builds

- config.conf is a special fastfetch config used for both images

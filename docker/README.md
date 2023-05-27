# Files for building onboardme docker containers

```
├──  arm_config
│   ├──  config.yml
│   └──  packages.yml
├──  config.conf
├──  Dockerfile
├──  Dockerfile.arm
└──  Dockerfile.arm-full
```

- Dockerfile is for x86_64
- Dockerfile.arm is for arm64/aarch
- Dockerfile.arm-full is for arm64/aarch with all the fixins

- arm_config is a directory of files just for arm builds

- config.conf is a special fastfetch config

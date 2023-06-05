# Files for building onboardme docker containers

```
├──  arm_config
│   ├──  default-onboardme-install.sh
│   ├──  devops-onboardme-install.sh
│   └──  music-onboardme-install.sh
├── ⚙️ config.conf
├── 🐳 Dockerfile
├── 🐳 Dockerfile.arm
└──  run_onboardme.sh
```

## Only x86_64 (amd64)
- `Dockerfile` is for linux/amd64
- `run_onboardme.sh` is for running onboardme with package groups based on docker env vars

```bash
docker build --platform=linux/arm64 -t onboardme:dev .
```

## Only ARM 64 (aarch64)
Homebrew on Linux [does not support ARM64 (aarch64)](https://docs.brew.sh/Homebrew-on-Linux#arm-unsupported), so we have special images for that.
- `Dockerfile.arm` is for linux/arm64 and linux/aarch64
- `arm_config` is a directory of files just for arm builds to download binaries and compile from source if there's no package manager package.

To build this image run:

```bash
docker build --platform=linux/arm64 -t onboardme:dev-arm -f Dockerfile.arm .
```

## Used in arm64 (aarch64) _and_ amd64
`config.conf` is a special fastfetch config used for both docker images

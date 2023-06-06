## add somafm for free internet radio out of SF
# ref: https://github.com/cuschk/somafm
echo -e "\n\033[92mInstalling somafm - for internet radio\033[00m"
sudo mkdir -p /usr/local/lib/node_modules
sudo chown -R root:$(whoami) /usr/local/lib/node_modules/
sudo chmod -R 775 /usr/local/lib/node_modules/
npm install --global somafm

## music via free streaming sources
## https://github.com/nukeop/nuclear
# curl -LO https://github.com/nukeop/nuclear/releases/download/v0.6.21/nuclear-v0.6.21.deb

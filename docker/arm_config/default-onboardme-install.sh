echo "setting up default onbaordme config"
mkdir -p $XDG_CONFIG_HOME/onboardme
mv /tmp/packages.yml $XDG_CONFIG_HOME/onboardme/
mv /tmp/config.yml $XDG_CONFIG_HOME/onboardme/

echo ""
echo "compiling neovim from source, before we run onboardme"
echo "ref: https://github.com/neovim/neovim/wiki/Building-Neovim#build-prerequisites"
git clone https://github.com/neovim/neovim /tmp/neovim
cd /tmp/neovim/
git checkout stable
make CMAKE_BUILD_TYPE=RelWithDebInfo
cd build
cpack -G DEB
sudo dpkg -i nvim-linux64.deb

echo ""
EXTRA_GROUPS=""
if [ -n $DEFAULT ]; then EXTRA_GROUPS+=" -g default"; fi
if [ -n $DATA_SCIENCE ]; then EXTRA_GROUPS+=" -g data_science"; fi
if [ -n $DEVOPS ]; then EXTRA_GROUPS+=" -g devops"; fi
if [ -n $MAIL ]; then EXTRA_GROUPS+=" -g mail"; fi
if [ -n $MUSIC ]; then EXTRA_GROUPS+=" -g music"; fi

obm_cmd="onboardme --no_upgrade --log_level debug$EXTRA_GROUPS"
echo "running onboardme command now: $obm_cmd"
$($obm_cmd)

echo ""
echo "downloading bottom debian package. bottom is a top replacement and is aliased to btm, and sometimes top"
curl -LO https://github.com/ClementTsang/bottom/releases/download/0.9.1/bottom_0.9.1_arm64.deb
sudo dpkg -i bottom_0.9.1_arm64.deb
rm bottom_0.9.1_arm64.deb

echo ""
echo "downloading gitui arm binary. gitui is a tui for git"
curl -LO https://github.com/extrawurst/gitui/releases/download/v0.22.1/gitui-linux-aarch64.tar.gz
tar xvf gitui-linux-aarch64.tar.gz
rm gitui-linux-aarch64.tar.gz
mv gitui $HOME/.local/bin/gitui

echo ""
echo "downloading zellij arm binary, a tmux replacement"
curl -LO https://github.com/zellij-org/zellij/releases/download/v0.36.0/zellij-aarch64-unknown-linux-musl.tar.gz
tar xvf zellij-aarch64-unknown-linux-musl.tar.gz
rm zellij-aarch64-unknown-linux-musl.tar.gz
mv zellij $HOME/.local/bin/zellij

echo ""
echo "compile fastfetch, for system facts, from source, requires pkg-config"
echo "ref: https://github.com/LinusDierheimer/fastfetch#building"
git clone https://github.com/LinusDierheimer/fastfetch.git /tmp/fastfetch
cd /tmp/fastfetch
mkdir -p build
cd build
cmake ..
cmake --build . --target fastfetch --target flashfetch
cp fastfetch $HOME/.local/bin/fastfetch
mkdir -p ${XDG_CONFIG_HOME}/fastfetch
mv /tmp/config.conf ${XDG_CONFIG_HOME}/fastfetch/config.conf

if [ -n $DEVOPS ]; then bash /tmp/arm_config/devops-onboardme-install.sh; fi
if [ -n $MUSIC ]; then bash /tmp/arm_config/music-onboardme-install.sh; fi

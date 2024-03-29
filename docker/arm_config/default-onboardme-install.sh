echo -e "\n\033[92mInstalling neovim\033[00m"
echo "ref: https://github.com/neovim/neovim/wiki/Building-Neovim#build-prerequisites"
git clone https://github.com/neovim/neovim /tmp/neovim
cd /tmp/neovim/
git checkout stable
make CMAKE_BUILD_TYPE=RelWithDebInfo
cd build
cpack -G DEB
sudo dpkg -i nvim-linux64.deb

EXTRA_GROUPS=""
if [ ! -z $DEFAULT ]; then
    EXTRA_GROUPS+=" -g default"
fi

if [ ! -z $DATA_SCIENCE ]; then
    EXTRA_GROUPS+=" -g data_science"
fi

if [ ! -z $DEVOPS ]; then
    EXTRA_GROUPS+=" -g devops"
fi

if [ ! -z $MAIL ]; then
    EXTRA_GROUPS+=" -g mail"
fi

if [ ! -z $MUSIC ]; then
    EXTRA_GROUPS+=" -g music"
fi

obm_cmd="onboardme --no_upgrade --log_level debug$EXTRA_GROUPS"
echo -e "\nRunning: \033[92m$obm_cmd\033[00m"
eval $obm_cmd

echo "🏁 Finished running onboardme!"

echo -e "\n\033[92mInstalling btm - top replacement\033[00m"
echo "downloading bottom debian package. bottom is a top replacement and is aliased to btm, and sometimes top"
curl -LO https://github.com/ClementTsang/bottom/releases/download/0.9.1/bottom_0.9.1_arm64.deb
sudo dpkg -i bottom_0.9.1_arm64.deb
rm bottom_0.9.1_arm64.deb

echo -e "\n\033[92mInstalling gitui - TUI for git\033[00m"
echo "downloading gitui arm binary."
curl -LO https://github.com/extrawurst/gitui/releases/download/v0.22.1/gitui-linux-aarch64.tar.gz
tar xvf gitui-linux-aarch64.tar.gz
rm gitui-linux-aarch64.tar.gz
mv gitui $HOME/.local/bin/gitui

echo -e "\n\033[92mInstalling zellij - a tmux replacement\033[00m"
echo "downloading zellij arm binary"
curl -LO https://github.com/zellij-org/zellij/releases/download/v0.36.0/zellij-aarch64-unknown-linux-musl.tar.gz
tar xvf zellij-aarch64-unknown-linux-musl.tar.gz
rm zellij-aarch64-unknown-linux-musl.tar.gz
mv zellij $HOME/.local/bin/zellij

echo -e "\n\033[92mInstalling fastfetch - for system facts\033[00m"
echo "compiling fastfetch from source, requires pkg-config"
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

if [ ! -z $DEVOPS ]; then bash /tmp/devops-onboardme-install.sh; fi
if [ ! -z $MUSIC ]; then bash /tmp/music-onboardme-install.sh; fi

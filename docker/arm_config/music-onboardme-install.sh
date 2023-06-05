## rustup: https://forge.rust-lang.org/infra/other-installation-methods.html
curl -LO https://static.rust-lang.org/dist/rust-1.69.0-aarch64-unknown-linux-gnu.tar.gz /tmp/
tar xvf /tmp/rust-1.69.0-aarch64-unknown-linux-gnu.tar.gz
cd rust-1.69.0-aarch64-unknown-linux-gnu/
rustup update
cd ..

## install spotifyd
# for this we need cargo already via rustup, which is in the devops file
sudo apt install -y libasound2-dev libssl-dev
git clone https://github.com/Spotifyd/spotifyd.git
cd spotifyd
cargo build --release

## install spotify-tui, for controlling spotify
cargo install --git https://github.com/spotify-tui/spotify-tui

## add somafm for free internet radio out of SF
# ref: https://github.com/cuschk/somafm
npm install --global somafm

## music via free streaming sources
## https://github.com/nukeop/nuclear
# curl -LO https://github.com/nukeop/nuclear/releases/download/v0.6.21/nuclear-v0.6.21.deb

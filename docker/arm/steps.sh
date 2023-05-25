apt-get update
apt-get install sudo
sudo apt install git curl libssl-dev libreadline-dev zlib1g-dev autoconf bison build-essential libyaml-dev libreadline-dev libncurses5-dev libffi-dev libgdbm-dev

### begin
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc
rbenv install 2.6.10
rbenv global 2.6.10
git clone https://github.com/Homebrew/brew.git .linuxbrew
eval "$(/.linuxbrew/bin/brew shellenv)"
which -a ruby
ruby --version
brew config
## end

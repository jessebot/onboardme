# install pyenv, for managing multiple python versions
# https://github.com/pyenv/pyenv#automatic-installer
echo "Installing pyenv"
curl https://pyenv.run | bash

# install gpg-tui, a TUI for gpg keys, for the lazy, like me: has to be compiled from source
# maybe use 🤷:
# https://github.com/orhun/gpg-tui/releases/download/v0.9.6/gpg-tui-0.9.6-x86_64-unknown-linux-gnu.tar.gz

## install gh - github's CLI
## ref: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
echo "Installing gh"
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install -y gh

## install glab - gitlab's cli
## ref: https://gitlab.com/gitlab-org/cli/-/blob/main/docs/installation_options.md#mpr-debianubuntu
# git clone 'https://mpr.makedeb.org/glab'
# cd glab/
# makedeb -si

# install kubectl for arm64
# ref: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux
echo "Installing kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" /tmp/
# download the checksum for validation
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl.sha256" /tmp/
# should return kubectl: OK and 0 return code
echo "$(cat /tmp/kubectl.sha256)  kubectl" | sha256sum --check
chmod +x /tmp/kubectl
mkdir -p ~/.local/bin
mv /tmp/kubectl ~/.local/bin/kubectl

# krew, the kubectl plugin manager
# ref: https://krew.sigs.k8s.io/docs/user-guide/setup/install/#bash
# export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
# TODO: is this path correct? can it be XDG spec?
echo "Installing krew"
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)

# k9s - k8s dashboard tui
echo "Installing k9s"
curl -LO https://github.com/derailed/k9s/releases/download/v0.27.4/k9s_Linux_arm64.tar.gz /tmp/
tar xvf /tmp/k9s_Linux_arm64.tar.gz
mv /tmp/k9s ~/.local/bin/k9s

# for installing helm, a package manager for k8s
echo "Installing helm"
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install -y apt-transport-https
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install -y helm

# installing argocd cli
echo "Installing argocd cli"
curl -sSL -o argocd-linux-arm64 https://github.com/argoproj/argo-cd/releases/download/latest/argocd-linux-arm64
sudo install -m 555 argocd-linux-arm64 /usr/local/bin/argocd
rm argocd-linux-arm64

## tfenv: https://github.com/tfutils/tfenv#manual
# TODO: maybe move this $XDG_DATA_HOME/tfenv and
#       add $XDG_DATA_HOME/tfenv to the path?
echo "Installing tfenv"
git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc

echo "Installing tflint"
## tflint: https://github.com/terraform-linters/tflint
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

echo "Installing terraform-docs"
## terraform-docs: https://github.com/terraform-docs/terraform-docs/
curl -LO https://github.com/terraform-docs/terraform-docs/releases/download/v0.16.0/terraform-docs-v0.16.0-$(uname)-amd64.tar.gz /tmp/
tar -xzf terraform-docs-v0.16.0-$(uname)-amd64.tar.gz
chmod +x terraform-docs
mv terraform-docs ~/.local/bin/terraform-docs

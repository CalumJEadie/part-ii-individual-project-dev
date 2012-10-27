#!/bin/sh

base_dir=`dirname $0`
files_dir=$base_dir/files

packages="git-core byobu chromium-browser vim"

# Install
sudo apt-get update
sudo apt-get install $packages

# Configure
sudo mv /boot/boot_enable_ssh.rc /boot/boot.rc
sudo cp $files_dir/etc/rc.local /etc/rc.local

# http://git-scm.com/book/en/Customizing-Git-Git-Configuration
git config --global user.name "CalumJEadie"
git config --global user.email calum@calumjeadie.com
git config --global core.editor vim
git config --global merge.tool vimdiff
git config --global color.ui true

cp $files_dir/home/vimrc $HOME/.vimrc

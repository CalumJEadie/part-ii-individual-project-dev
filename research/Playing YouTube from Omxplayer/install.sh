# Latest version in the repos is broken.
# sudo apt-get install youtube-dl

wget 'https://github.com/rg3/youtube-dl/blob/master/youtube-dl?raw=true' -O /tmp/youtube-dl
chmod +x /tmp/youtube-dl
sudo cp /tmp/youtube-dl /usr/bin/youtube-dl

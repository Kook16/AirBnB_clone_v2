#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# install nginx if not installed
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared

sudo echo "DAMM !!!" | sudo tee /data/web_static/releases/test/index.html

sudo ln -snf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data

str="\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\tindex index.html 0-index.html 0-index.htm;\n\t}"
sudo sed -i "/^\tserver_name .*;/a ${str}" /etc/nginx/sites-enabled/default
sudo service nginx restart

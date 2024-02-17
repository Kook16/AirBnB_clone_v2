#puppet script that sets up web browser for deployment of web_static
exec { 'command':
command  => "sudo apt-get -y update;
sudo apt-get -y install nginx;
mkdir -p /data/web_static/shared;
mkdir -p /data/web_static/releases/test/;
sudo echo 'DAM!!' | sudo tee /data/web_static/releases/test/index.html;
sudo ln -nfs /data/web_static/releases/test /data/web_static/current;
sudo chown -R ubuntu:ubuntu /data",
provider => shell,
}
exec { 'add_lines':
  command  => 'sudo sed -i "s|^\tserver_name .*;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" /etc/nginx/sites-enabled/default',
  provider => shell,
}

exec { 'command2':
command  => 'sudo service nginx restart',
provider => shell,
}
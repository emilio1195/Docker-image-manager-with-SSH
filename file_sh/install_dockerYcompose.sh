#!/bin/bash

sudo echo Test Docker

sudo service docker start
sudo docker run hello-world

echo Installing compose...

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo Installing Successful!

exit
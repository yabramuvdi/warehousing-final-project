wget https://get.docker.com/
mv index.html getDocker.sh
chmod 744 getDocker.sh
sh getDocker.sh
sudo usermod -aG docker ubuntu
sudo docker pull yabramuvdi/dashboards:latest
sudo docker run -d --name app -p 8050:8050 yabramuvdi/dashboards:latest

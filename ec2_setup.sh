#################################################################
# 1. Make sure the EC2 instance has the HTTPS and 8050 ports open
# 2. Get this shell script from github
# 3. Run script
# 4. We will use SUDO to run docker in order to avoid loging out
#################################################################

#Install docker to correctly display Dash content
wget https://get.docker.com/
mv index.html getDocker.sh
chmod 744 getDocker.sh
sh getDocker.sh
sudo usermod -aG docker ubuntu
# At this stage we should logout, but we wont

#Get docker container
docker pull yabramuvdi/dashboards:latest
docker run -d --name app -p 8050:8050 yabramuvdi/dashboards:latest

#################################################################
# OLD CODE
#################################################################

#git clone https://github.com/yabramuvdi/warehousing-final-project.git

#cd warehousing-final-project/
#chmod +x load_final.py
#chmod +x app.py
#chmod +x ec2_setup.sh

#sudo apt-get update
#curl -O https://bootstrap.pypa.io/get-pip.py
#sudo apt-get install python3-distutils
#python3 get-pip.py --user

#python3 -m venv venv && source venv/bin/activate
#sudo pip3 install dash==1.6.1 dash-daq==0.3.1 pandas datetime plotly mysql-connector-python

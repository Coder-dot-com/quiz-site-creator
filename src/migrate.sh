#!/bin/bash

set -e



yes | python manage.py makemigrations
yes | python manage.py migrate 

cd ..



git add . 
set +e
git commit -m "deploy"
set -e
git push



# sudo ssh -i "/home/user/Documents/DeployKey06.02.pem" ubuntu@ec2-18-144-2-42.us-west-1.compute.amazonaws.com  'cd quiz-site-template && git pull && sudo docker-compose  -f docker-compose-deploy.yml build && sudo docker-compose  -f docker-compose-deploy.yml down && sudo docker-compose  -f docker-compose-deploy.yml kill && sudo docker-compose  -f docker-compose-deploy.yml down && sudo docker-compose  -f docker-compose-deploy.yml up'




from ubuntu:20.04

run apt-get update

run apt-get install -y  \
        python3-dev \
        python3-pip 

run apt-get install -y --fix-missing vim

workdir /app

copy requirements requirements

run pip3 install -r requirements/dev.txt

copy . .

#run python3 manage.py collectstatic

cmd gunicorn --bind 0.0.0.0:8000 project.wsgi

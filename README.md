# Saba

Speech Emotion Recognition System (Saba):

In order to run Saba serer enter command bellow:

    FLASK_APP=run.py FLASK_DEBUG=1 flask run

Curl command for registration:

    curl -i -X POST -H "Content-Type: application/json" -d '{"username":"judy","password":"python"}' http://127.0.0.1:5000/registration


For login:

    curl -i -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}' http://127.0.0.1:5000/login


For refresh Tokens:

    curl -X POST -H "Authorization: Bearer <refresh token>" -d "field=value" "http://127.0.0.1:5000/token/refresh"

For Upload and test a voice:

    curl -H "Authorization: Bearer <access token>" -F "file=@filepath" "http://127.0.0.1:5000/predict/model1"

For ava:

    curl -X POST -d "file=hello.wav" "http://127.0.0.1:5000/predict/avamodel1"

<h1>How to deploy?</h1>

1. Install required packages:

        sudo apt-get install nginx python3-pip python-virtualenv

2. Create virtual environment:

        virtualenv -p python3 .env

        source .env/bin/activate

3. Install gunicorn:

        pip3 install gunicorn flask flask-restful flask-jwt-extended passlib flask-sqlalchemy scipy sklearn speechpy tensorflow keras pandas


4. Create a unit file ending in .service within the /etc/systemd/system/saba.service directory to begin:

        [Unit]
        Description=Gunicorn instance to serve myproject
        After=network.target

        [Service]
        User=__user__
        Group=www-data
        WorkingDirectory=/home/__user__/saba
        Environment="PATH=/home/__user__/saba/.env/bin"
        ExecStart=/home/__user__/saba/.env/bin/gunicorn --workers 3 --bind unix:saba.sock -m 007 run:app

        [Install]
        WantedBy=multi-user.target

5. To enable the configuration, run the following commands:

        sudo systemctl start saba
        sudo systemctl enable saba

6. Configuring Nginx to Proxy Requests:

        sudo nano /etc/nginx/sites-available/saba

        server {
                listen 80;
                server_name your_domain www.your_domain;

                location / {
                        include proxy_params;
                        proxy_pass http://unix:/home/__user__/saba/saba.sock;
                }
        }

7. To enable the Nginx server block configuration you've just created, link the file to the sites-enabled directory:

        sudo ln -s /etc/nginx/sites-available/saba /etc/nginx/sites-enabled


8. With the file in that directory, you can test for syntax errors:

        sudo nginx -t
        sudo service nginx restart

9. Configure firewall:

        sudo ufw allow 'Nginx Full'


<h1>How to use UI?</h1>
HTML UI located in ui folder. In order to use it in chrome you should install an extension named "Allow-Controll-Allow-Origin"
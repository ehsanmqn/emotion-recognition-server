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

        pip3 install gunicorn flask flask-restful flask-jwt-extended passlib flask-sqlalchemy scipy peewee flask_peewee flask-admin flask-login sklearn speechpy tensorflow keras pandas

        For mysql-server:
        sudo apt-get update
        sudo apt-get install python3-dev **default-libmysqlclient-dev**
        sudo pip3 install mysqlclient


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
          listen 8080;
          server_name your_domain www.your_domain;

          add_header 'Access-Control-Allow-Origin' '__host_address__';
          add_header 'Access-Control-Allow_Credentials' 'true';
          add_header 'Access-Control-Allow-Headers' 'Authorization,Accept,Origin,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
          add_header 'Access-Control-Allow-Methods' 'GET,POST,OPTIONS,PUT,DELETE,PATCH';

          location / {
            if ($request_method = 'OPTIONS') {
                add_header 'Access-Control-Allow-Origin' '__host_address__';
                add_header 'Access-Control-Allow_Credentials' 'true';
                add_header 'Access-Control-Allow-Headers' 'Authorization,Accept,Origin,DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
                add_header 'Access-Control-Allow-Methods' 'GET,POST,OPTIONS,PUT,DELETE,PATCH';
                add_header 'Access-Control-Max-Age' 1728000;
                add_header 'Content-Type' 'text/plain charset=UTF-8';
                add_header 'Content-Length' 0;
                return 204;
            }

            include proxy_params;
            proxy_redirect off;
            proxy_set_header host $host;
            proxy_set_header X-real-ip $remote_addr;
            proxy_set_header X-forward-for $proxy_add_x_forwarded_for;
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

10. Configure ui:

        sudo mv /var/www/html /var/www/html.back
        sudo ln -s ~/Saba/ui /var/www/html
        sudo chown -R user:user /var/www/html

11. Configure database:

        rm -rf app.db

12. Change IP and port in following html files:
    1. ui/login.html
    2. ui/index.html
    3. ui/pages/analyzefile.html

13. Use postman to insert user into database


14. Login to Saba Analytics

<h1>How to use UI?</h1>
HTML UI located in ui folder.

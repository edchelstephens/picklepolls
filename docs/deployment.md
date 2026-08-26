

# Deploy Django with Gunicorn and Nginx on Ubuntu 22.04
## Base Guide: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

## Assumptions:
1. You already have ssh access to an ubuntu instance
2. You already own a domain which will replace the picklepolls_domain placeholder below
3. You already have a DNS A record that points to the ubuntu instance ip to picklepolls_domain



## 1. On new instance install necessary ubuntu packages

```
sudo apt update && sudo apt ugprade
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3.12-venv
sudo apt install nginx
```

## 2. Setup SSH key access from ubuntu machine to github
https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-22-04


## 3. Clone repository
``
git clone git@github.com:edchelstephens/picklepolls.git
``

If it has error. Then reload the ssh

```

eval "$(ssh-agent -s)"

ssh-add ~/.ssh/ssh_key_name_here

```

## 4. Change directory into the repositry
```
cd picklepolls
```

## 5. Create picklepolls virtual environment and install prod requirements

```
python3 -m venv picklepolls_venv
source picklepolls_venv/bin/activate


pip install -r _requirements/prod.txt


```

## 5.1 Make sure to migrate database and collectstatic
```
python manage.py migrate

# First, ensure that in the settings.py, you have configured the STATIC_URL and STATIC_ROOT
# STATIC_URL = "/static/"
# STATIC_ROOT = "staticfiles"

python manage.py collectstatic


```

## 6. Create picklepolls service

```
sudo nano /etc/systemd/system/picklepolls.service

```

## 7. Put contents on service

``` 
[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/picklepolls
ExecStart=/home/ubuntu/picklepolls/picklepolls_venv/bin/gunicorn --bind 0.0.0.0:8020 project.picklepolls.wsgi:application --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
``` 

## 8. Start up the service

```     
sudo systemctl daemon-reload
sudo systemctl start picklepolls
sudo systemctl enable picklepolls
sudo systemctl status picklepolls
``` 

## 9. Create site for picklepolls in nginx

``` 
sudo nano /etc/nginx/sites-available/picklepolls
``` 

## 10. Define nginx configuration

``` 
server {
        server_name picklepolls.go2courts.com;

        location / {
                proxy_pass http://127.0.0.1:8020;
                include proxy_params;
        }

        location /static/ {
		alias /home/ubuntu/picklepolls/project/staticfiles/;
	}
}
``` 

## 11. Remove the default nginx site on homepage of the ip

``` 
sudo rm /etc/nginx/sites-available/default

# If above doesn't auto delete the /default symbolic link, then manually delete it with
sudo rm /etc/nginx/sites-enabled/default

``` 

## 12. Enable the picklepolls server configuration by creating a symbolic link

``` 
sudo ln -s /etc/nginx/sites-available/picklepolls /etc/nginx/sites-enabled
``` 

## 13. Check nginx configuration

``` 
sudo nginx -t
``` 

## 14. Restart nginx

``` 
sudo systemctl restart nginx
``` 

## 15. Enable HTTPs by creating certificates with Let's Encrypt, first install

``` 
sudo apt install certbot python3-certbot-nginx -y
``` 

## 16. Install certificate and following instructions along

``` 
sudo certbot --nginx -d picklepolls_domain
``` 

## 17. Check the logs
```
# last 100 lines
sudo journalctl -u picklepolls.service -n 100

# follow the log live
sudo journalctl -u picklepolls.service -f
```

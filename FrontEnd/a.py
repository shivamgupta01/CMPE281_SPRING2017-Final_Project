import boto3


shell_script = """
#!/bin/bash
yum update -y
yum install -y apache2 php56 mysql55-server php56-mysqlnd php56-gd
service httpd start
chkconfig httpd on
groupadd www
usermod -a -G www ec2-user
chown -R root:www /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} +
find /var/www -type f -exec chmod 0664 {} +
#echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php
#a2enmod rewrite
sudo service httpd restart
cd /opt/
wget https://www.opensource-socialnetwork.org/downloads/ossn-v4.2-1468404691.zip -O ossn.zip
unzip ossn.zip -d /var/www/html/
yum install mysql-server
service mysqld start
cat << EOF | mysql -u root
SET GLOBAL sql_mode='';
CREATE DATABASE ossndb;
CREATE USER 'ossnuser'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON ossndb.* TO 'ossnuser'@'localhost';
FLUSH PRIVILEGES;
EOF
mkdir -p /var/www/ossndatadir
chown www-data:www-data -R /var/www/html/ossn/
touch /etc/apache2/sites-available/ossn.conf
ln -s /etc/apache2/sites-available/ossn.conf /etc/apache2/sites-enabled/ossn.conf
service httpd start
#vi /etc/apache2/sites-available/ossn.conf
"""


ec2 = boto3.resource('ec2', region_name='us-west-2')
instance_id =  ec2.create_instances(ImageId='ami-4836a428',KeyName= 'cmpe281', MinCount=1, MaxCount=1,
                     InstanceType='t2.micro',SecurityGroupIds= ['sg-f3304688'],UserData= shell_script)

instance_id = instance_id[0]

# Wait for the instance to enter the running state
instance_id.wait_until_running()

# Reload the instance attributes
instance_id.load()
return instance_id.public_dns_name





Creating GCP key

ssh-keygen -t rsa -f gcp -C shiva -b 2048

Login

ssh -i ~/.ssh/gcp shiva@<ip_address>
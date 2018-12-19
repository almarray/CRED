Controleur de Réserve  d'Eau de Drainage : projet avec Rpi pour controler les état de fonctionnement de 3 pompes permettant de réguler le niveau d'eau dans un puisard, et un générateur electrogène en cas de perte de secteur. 

# Installation / Instructions

## Démarrer le projet : 


Pompes haute PH, pompe basse PB, pompe 12V PV, Secteur ... 
Monitor status logs. 0-5
Calcul de débit.

## To migrate

python manage.py makemigrations polls

python manape.py sqlmigrate polls 0001

python manage.py migrate

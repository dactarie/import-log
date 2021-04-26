# import-log 

Un script en python qui vous permet d'importer tous vos log de vos VM/Serveur distant de manière simple et automatisée.

## Fonctionnement :

* 1° : Regroupe les fichiers de l'hôte dans un dossier pré-définit (dans mon exemple /tmp/"nom de l'hote").
* 2° : Création d'une archive dans ce même dossier pré-définit (dans mon exemple /tmp/"nom de l'hote").
* 3° : Import de l'archive sur le serveur dans le dossier pré-définit (dans mon exemple /tmp/"nom de l'hote".tar).
* 4° : Décompactage des fichiers vers leurs endroits définitifs (dans mon exemple /home/"user"/"nom de l'hote").
* 5° : Vidage du contenu des fichiers importés sur l'hôte.
* 6° : Fermeture des sessions Sftp et Ssh. 

## Prérequis :

* Python 3.9, Paramiko (pip install paramiko)

## Configuration :

* 1° : Il vous faut ajouter vôtre clé ssh sur le serveur distant si ce n'est déjà fait (ex : https://blog.microlinux.fr/cle-ssh/)

* 2° : Créez un fichier dans le dossier CUSTOMER portant le nom de vôtre serveur (et sans extension).

* 3° : Ajouter dans ce fichier la liste de vos fichiers à importer (chemin complet depuis la racine et un fichier par ligne).

* 4° : Le serveur doit être joignable à partir de ce même nom de fichier que vous venez de créer (si son nom est différent de celui joignable sur le réseau vous pouvez l'ajouter dans le fichier /etc/hosts ou pour windows C:\windows\system32\drivers\hosts (ex: 192.168.1.2 serveur).

* 4° : Pour finir il vous faut configurer les diverses options de variables dans le fichier python si nécessaire selon vos besoins (Ligne 9 à 12).

* 5° : Exécuter vôtre script (python3.9 main.py).

### Notes :

* Si votre fichier importé est vide, le script vous le notifie.
* Malgré un script totalement fonctionnel il subsiste encore un bug principal : il n'est pas capable de transférer de gros fichier, en effet le module Paramiko n'est pas très adapté dans le cas d'une création d'archive. il semblerait que celui-ci mette fin à la commande dès lors que celle-ci est bien exécutée. Il vaut donc mieux ne pas dépasser quelques MO (au total) afin de pouvoir réussir à importer une archive complète.
* (Encore en développement) Le module Scan rapide vous permettra de faire un premier scan rapide des fichiers importés et de vous notifier dès lors qu'un certain mot apparaît plusieurs fois.

### Ajout a venir :

* Gestion des droits sur les fichiers importés.
* Correction du bug de l'import de gros fichiers (<10Mo).
* Script plus modulaire (n'effacera plus le contenue de fichier source si l'export n'est pas de type Log par exemple).


#### ATTENTION : Vous pouvez toutefois importer tout type de fichiers avec ce script mais celui-ci efface le contenu du fichier importé, pensez donc à commenter la ligne "execution.remove_trace()". 

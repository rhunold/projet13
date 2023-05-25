## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.8.1 ou supérieure
- Un compte CircleCI
- Un compte Heroku
- Heroku CLI
- Un compte Sentry
- Un compte Docker Hub
- Docker Desktop

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/projet13-parent-folder`
- `git clone https://github.com/rhunold/projet13.git`

#### Créer l'environnement virtuel

- `cd /path/to/projet13`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Créer un ficher pour les variables d'environnement
Créer un fichier .env à la racine du projet.
Ce fichier devra contenir les informations de developpement local. Les valeurs DJANGO_SECRET_KEY et SENTRY_KEY sont des valeurs d'exemples qui sont à remplacé par les bonnes valeurs.

```
DJANGO_SECRET_KEY=XXXXXXXX
DEBUG=1
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1
SENTRY_KEY=https://xxxx.ingest.sentry.io/xxxx
```  

#### Exécuter le site

- `cd /path/to/projet13`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).


#### Linting

- `cd /path/to/projet13`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/projet13`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/projet13`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


## Déploiement

### Fonctionnement du déploiement

Lorsque l'on push un fichier sur le repository du projet Github, le service de Circle Ci le détecte et lance les jobs du fichier config.yml se trouvant dans le dossier .circleci. 
Si on est sur une autre branche que le master, seul le jobs de test est lancé.

Si c'est sur le master que l'on a pushé, Circle lance le job test. Si ce dernier est ok, il lance la génération de l'image et la push sur le [registry docker indiqué](https://hub.docker.com/repository/docker/rhunold/amd64_image_oc_letting/general) en y ajoutant un tag se basant sur la variable de hash CIRCLE_SHA1. Si le build est finalisé, c'est le job pour le deploiement sur Heroku qui est activé. Si le déploiement Heroku est réussi, l'application est déployé.

Si l'un des jobs rencontre une erreur, tout s'arrête et les jobs suivant ne sont pas exécutés. 


### Configuration requise pour le déploiement

#### Docker hub & Docker Desktop
- Aller sur le site [https://hub.docker.com](https://hub.docker.com/) et inscrivez-vous.
- Notez bien votre username et votre mot de passe car ils seront utilisé plus tard.
- Téléchargez [Docker Desktop (https://www.docker.com/products/docker-desktop/) et installez le sur votre machine. Cela vous permettra de gérer facilement les image et les containers générés avec une interface user friendly. L'application installe par ailleurs le Docker daemon qui permet d'utiliser Docker via le terminal pour crée des images et des containers.

Pour construire une image, vous devez allez à la racine de votre projet et vous assurer que le fichier DockerFile est bien présent à la racine de votre projet.
Pour générer l'image, vous pouvez utiliser la commande suivante. 
```
docker build -t rhunold/local_image_oc_letting .
```  

La commande suivante est plus élaborée et permet de récupérer le hash du dernier commit pour l'assigner en tant que tag. Une fois l'image crée, elle est publié sur Docker Hub. Puis elle est récupérée et on génère un container avec un nom spécifique. Attention à ce qu'un autre container n'existe pas avec le même nom sans quoi le container ne pourra pas être crée (il faut donc au préalable supprimer le container, soit en ligne de commande, soit via Docker Desktop)
```
COMMIT_HASH=$(git rev-parse HEAD) \
&& \
docker build --build-arg COMMIT_HASH=$COMMIT_HASH -t rhunold/local_image_oc_letting:$COMMIT_HASH . \
&& \
docker push rhunold/local_image_oc_letting:$COMMIT_HASH \
&& \
docker pull rhunold/local_image_oc_letting:$COMMIT_HASH \
&& \
docker run --name local_container_oc_letting -p 8000:8000 rhunold/local_image_oc_letting:$COMMIT_HASH
```  

La commande ci dessus étant un peu longue, vous pouvez créer un script shell contenant ces instructions (oc_site.sh).
Afin d'activer ce script, vous devez utiliser cette ligne une première fois
```
chmod +x oc_site.sh
```  

Ensuite, vous pourrez executer ce script avec cette ligne
```
./oc_site.sh
```  

#### CircleCI
- Aller sur le site  de [CircleCI](https://circleci.com)
- Se créer un compte en utilisant l'option Github (utiliser la flèche et choisir l'option "Public repo only")
- Une fois connecté, allez dans "Projects", puis cliquer sur le bouton "Set Up Project" correspondant à la ligne du nom du projet concerné.
- Choissez l'option " Fastest: Use the .circleci/config.yml". Cela suppose bien entendu que le fichier config.yml soit bien présent le repository Github
- Ensuite cliquez sur "..." et cliquez sur "Project Settings". Dans la barre de gauche, cliquez sur "Environment Variables". Ajouter des variables d'environnement en cliquant sur le bouton.
  - Name : ALLOWED_HOSTS / Value : liste des hosts permis (doit contenir celui de votre app Heroku)
  - Name : DJANGO_SECRET_KEY / Value : la secret key de votre projet Django
  - Name : DOCKERHUB_PASSWORD / Value : votre mot de passe Docker Hub
  - Name : DOCKERHUB_USERNAME / Value : votre username Docker Hub
  - Name : HEROKU_API_KEY / Value : API key fourni par votre compte Heroku
  - Name : HEROKU_EMAIL / Value : email utilisé sur heroku
  - Name : SENTRY_KEY / Value : la key fourni par sentry lors de l'implémentation dans settings.py

Il est a noté que CircleCI fourni un ensemble de variables spécifiques qui sont utilisables sans avoir à les déclarer au préalable. C'est le cas de la variable CIRCLE_SHA1 qui correspond au hash généré par chaque lancement de pipeline. Cette variable est utilisé pour le tag utilisé lors de la publication de l'image sur Docker Hub.

#### Heroku
- Se créer un compte [Heroku](https://www.heroku.com) et notez bien votre mot de passe.
- Pour créer une app et/ou un pipeline, vous devez au préalable fournir vos informations de carte bancaire.
- Dès lors, vous pourrez créer un pipeline (bouton "New" puis "Create new pipeline"). Choisissez un nom (oc-letting) pour votre pipeline puis cliquez sur "Create Pipeline"
- Cliquez sur "Add app" sous "Production".
- Donner un nom (oc-letting) et une région (Europe) à votre nouvelle app.
- Installer [Heroku CLI(https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli) si ce n'est pas déjà fait.


Loguez vous pour créer une SSH public key
```
heroku login
```  

Ensuite vous pourrez vous loguer au Container Registry
```
heroku container:login
```

Puis vous pourrez fournir à Heroku les différentes variables d'environnements
```
heroku config:set --app oc-letting DJANGO_SECRET_KEY='XXXXXXXX'
```  

```
heroku config:set --app oc-letting DEBUG=0
```  

```
heroku config:set --app oc-letting ALLOWED_HOSTS='localhost,0.0.0.0,127.0.0.1,oc-letting.herokuapp.com'
```  

```
heroku config:set --app oc-letting SENTRY_KEY='https://xxxx.ingest.sentry.io/xxxx'
```  

```
heroku config:set --app oc-letting DISABLE_COLLECTSTATIC=0
``` 

Vous pouvez vérifier votre configuration avec 
```
heroku config --app oc-letting
``` 

#### Sentry
- Allez sur le site de [Sentry](https://sentry.io) et créer vous un compte.
- Une fois votre compte crée, cliquez sur "Create Project"
- Choisissez Django dans les plateformes proposées et donner un nom à votre projet Sentry
- Pour configurer le SDK, il faut récupérer le code source et l'implémenter dans le fichier settings.py de votre projet. Pour s'assurer que Sentry marche bien, vous pouvez ajouter l'exemple fourni dans le fichier urls.py (path dirigeant vers une fonction générant une erreur).
- Afin de garantir la sécurité, la valeur de Sentry est remplacée par la variable SENTRY_KEY. Cette dernière est appelée en local par le fichier .env. Sur Heroku et CircleCI, elle est fournie dans les variables renseigné sur ces services comme indiqué préalablement.
- Une fois que l'app a été déployé, en allant sur [la page d'erreur de Sentry](https://oc-letting.herokuapp.com/sentry-debug/) vous tomberez sur une erreur 500. Cette erreur est remontée dans le site de Sentry.


### Déploiement répétable
- A tout moment, vous pouvez décider de supprimer l'application Heroku. Il faudra alors recréer une application Heroku et ajouter les variables d'environnement comme indiqué préalablement.
- Lorsque l'application Heroku a été recrée, vous pouvez allez dans CircleCI, allez dans la partie Dashboard, identifier le dernier pipeline avec les 3 jobs étant success et cliquer sur l'icone "Rerun workflow from start"
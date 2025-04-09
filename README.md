# YouTube Downloader

Une application web simple pour télécharger des vidéos YouTube en MP4 ou MP3.

## Fonctionnalités

- Téléchargement de vidéos YouTube
- Choix de la qualité (Meilleure qualité, 720p, 480p, 360p)
- Choix du format (MP4 ou MP3)
- Interface utilisateur simple et intuitive

## Prérequis

- Python 3.x
- yt-dlp
- Flask

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/youtube-downloader.git
cd youtube-downloader
```

2. Installez les dépendances :
```bash
pip install flask yt-dlp
```

3. Lancez le serveur :
```bash
python app.py
```

4. Accédez à l'application dans votre navigateur :
```
http://127.0.0.1:5000
```

## Guide d'utilisation

Consultez le fichier `guide_serveur.html` pour un guide détaillé sur l'utilisation de l'application.

## Structure du projet

```
youtube-downloader/
├── app.py              # Application principale
├── templates/          # Templates HTML
│   └── index.html     # Page d'accueil
├── README.md          # Documentation
└── guide_serveur.html # Guide d'utilisation
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request. 
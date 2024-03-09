# PatternPilotv2
Pattern Pilot is an application developed for the crotche lovers to ease the pattern calculation and test patterns.
   
## Setup

1. Run `$ git clone git@github.com:pdastudios/PatternPilotv2.git`

Now your top level file structure should look like this:

```yaml
PatternPilotv2/
    src/
    .gitignore
    README.md
    main.js
    package-lock.json
    packge.json
    requirements.txt
```

2. Set up your python virtual development environment  

```sh
$ python -m venv .env
```

3. Start your virtual environment by opening a Git Bash (Windows), PowerShell (Windows) or Terminal (Linux/MacOS):

Windows:
```pwsh
C:/Users/PixelHD/PatternPilotv2>.env/Scripts/activate
```

Linux/MacOS:
```sh
$ source .env/bin/activate
```

4. Download necessary python modules: 

```sh
$ pip install -r requirements.txt
```

Now that you're done with the Django portion, make sure ElectronJS is also ready to be ran:

5. Install Electron.

> Navigate to PatternPilotv2/

```sh
npm install --save-dev electron
```

> Tip: You can check version and verify installation by running `npm list electron`. If Electron was installed successfully, when running the command it should look something like this:

```sh
$ npm list electron
patternpilotv2@1.0.0 C:/Users/PixelHD/PatternPilotv2
└── electron@29.1.0
```

6. Last but not least test everything is setup properly:

```sh
npm start
```

This should pop a window with the Desktop Application

and

```sh
$ cd src/django/pattern_pal
$ python manage.py migrate
$ python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` in the browser. This should load the Web Application html code in successfully.

# Django + ElectronJS
Django will read the same html files as Electron, the way to do this is by going to Django's settings.py and modify TEMPLATES
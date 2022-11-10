# Budget Manager App

This App is designed to manage ones budget. 

We start at the main view, which is a display of the budget entries of the latest month. 
With the plus button in the bottom right one will be redirected to a new screen, 
where a new entry can be added. 
This will happen by selecting the type to be an income or expense, 
which will affect the money value field. 
To submit ths entry, click on the add button below. 

Starting from the main screen, 
the settings screen can be accessed by clicking on the menu symbol on the bottom left. 
Here, next to app settings, one can add or delete categories, 
which will affect the category dropdown in the add new entry screen. 
Keep in mind by deleting a category, it will delete the entries with that category as well. 


## Intended to Run

- For testing out the app, see the `bin/` folder for the current build of the app. 
- For developing, see:
  - [External Documentation](External Documentation)
  - [Installation of Resources](Installation of Resources) 
  - [Project Structure](Project Structure)



## Current State of Project

**Work in Progress**

Currently, we have the following functionalities implemented:
- Displaying entries from the Database by month
- Adding new entries to the database as income or expense 
- Adding categories to the database
- Deleting entries from the database
- Deleting categories and related entries from the database
- Deleting entries from whole month
- Importing (merge) and exporting the database


### Known Issues

None at the moment. 


## External Documentation

[Kivy Documentation](https://kivy.org/doc/stable/)

[Kivymd Documentation](https://kivymd.readthedocs.io)

[SQLite](https://www.sqlitetutorial.net/)



## Installation of Resources

To install resources to develop or clone the project. 

Consult [this documentation](https://www.askpython.com/python/examples/write-android-apps-in-python) for help. 


### Kivy and Kivymd
```commandline
pip install kivy
pip install kivymd
```


### Buildozer
```commandline
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade Cython==0.29.19 virtualenv  # the --user should be removed if you do this in a venv
```

create a `./bashrc` file and add the following line at the end of your `~/.bashrc` and `./bashrc` file
```
export PATH=$PATH:~/.local/bin/
```

Init Buildozer
```commandline
buidozer init
```


## Project Structure

- `main.py`: Heart of project
- `screens/`: Folder with python files for functionalities on screen level
- `templates/`: Folder with kivy language files for structural functionality on screen level
- `assets/`: Folder with supporting scripts and assets



## Build Application
```commandline
buildozer -v android debug
```

You should have an APK file in the `./bin/` directory. 



## License

GNU General Public License v3.0

See the [LICENSE](./COPYING) file.

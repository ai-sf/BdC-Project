# Botta di Coulomb 

Botta di Coulomb is a quiz game developed by the Local Committee of Pavia of Italian Association of Physics Students [AISF](http://ai-sf.it/), and it has been used in different popularization contexts e.g. the European Researchers' Night 2017 and 2018 in Pavia, during workshops and conferences e.g. [ATLAS Italia 2017](https://agenda.infn.it/event/13733/) in Pavia or the Biomedical Physics Lombard Event [BiPLE 2018](http://ai-sf.it/biple/), as well as in pubs or for private events.

Since the game has been developed by physicists, each team is associated to a famous physicist.

## Installation
The game is written in Python 2.7 and it requires [kivy](https://kivy.org), and some other additional packages. See Kivy installation instructions here: https://kivy.org/doc/stable/installation/installation-linux.html

An installation using [virtualenv](https://virtualenv.pypa.io/en/latest/) is recommended:
```
virtualenv --python=python2.7 env
source env/bin/activate
```
Then the required packages can be installed using `pip`:
```
pip install serial configparser Cython==0.28.2 kivy
```

## Usage
Assuming your working in the repository root directory and the configuration file is `parameter.dat`, you can start the game with:
```
python src/main.py parameter.dat
```
(It may require a `sudo` when using the serial input)
You can find an example of parameter file, `parameter_TEST.dat`, based on the files in the `test_game` directory. 

## Useful keyboard shortcuts in Ubuntu 18:
- Move the game windows from a display to another: Shift + Windows + dx/sx
- Fullscreen: Windows+up/down

## Additional remarks

In order to avoid libpng error messages, convert all the images used in the game with:
```
convert *.png -set filename:base "%[base]" "%[filename:base].png"
```
(it requires `imagemagick`, which can be installed with `sudo apt-get install imagemagick`). This is required only if you change something, since all the images present in the game have already been fixed in this way.
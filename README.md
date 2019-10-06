# Botta di Coulomb (BdC)

- Multi-player quiz game, written in Python with the [Kivy](https://kivy.org) library.
- Main goal of the project are popularization activities: first developed for the European Researchers' Night 2017 by [AISF](http://ai-sf.it/) Pavia, and proposed in several other public or private events.
- Apologies for the Italian language, which appears almost everywhere.


## Installation
See Kivy installation instructions [here](https://kivy.org/doc/stable/gettingstarted/installation.html). A local installation via [conda](https://docs.conda.io/projects/conda/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) is recommended.

### Installing with conda
First, create an environment by installing the following packages:
```
conda create -n bdc -c conda-forge pyserial configparser kivy
```
Then remember to load the environment before starting the game:
```
conda activate bdc
```
### Installing with virtualenv
First, create a directory `env` with a local Python installation.
Then activate the environment:
```
virtualenv --python=python2.7 env
source env/bin/activate
```
The required packages can be installed using `pip`:
```
pip install serial configparser Cython==0.28.2 kivy
```

## Usage
Download the repository manually or with `git`:
```
git clone [--deep 1] -b master https://gitlab.com/gstagnit/bdc
```
The option `--deep 1` allows you to save locally only the latest commit.

Then you can start the game with:
```
python path/to/src/main.py path/to/inputcard.dat
```
A full example is in the `test_game` folder (again, sorry for the Italian), with `test_game.dat` as input card.

### Real game session
The software is designed to be used with a set of remote controllers, all connected in a Wi-fi mesh grid, specifically designed for BdC by [@micp](https://gitlab.com/micp). The communications with the laptop are handled by a "master" controller connected via USB, receiving messages from the other controllers and writing them in the serial format.

If the controllers are not used, the game can still be played for debug purposes, however remember to set the variable `no_serial` to `True` in the input card.

## Useful keyboard shortcuts (GNOME 3):
- Move the window from a display to another: Shift + Windows + dx/sx
- Full screen: Windows+up/down


## Possible issues
- In order to avoid `libpng` error messages, convert `*.png` files with:
```
convert *.png -set filename:base "%[base]" "%[filename:base].png"
```
(required `imagemagick`, which can be installed with `sudo apt-get install imagemagick`).

# Botta di Coulomb 

Botta di Coulomb is a quiz game developed by the Local Committee of Pavia of Italian Association of Physics Students [AISF](http://ai-sf.it/), and it has been used in different popularization contexts e.g. the European Researchers' Night 2017 and 2018 in Pavia, during workshops and conferences e.g. [ATLAS Italia 2017](https://agenda.infn.it/event/13733/) in Pavia or the Biomedical Physics Lombard Event [BiPLE 2018](http://ai-sf.it/biple/), as well as in pubs or for private events.

## Installation
The game is written in Python and it requires [kivy](https://kivy.org). Some graphical libraries are also required:
```
libsdl2-ttf-dev libsdl2-net-dev libsdl2-mixer-dev libsdl2-image-dev libsdl2-gfx-dev libsdl2-dev
```

## Usage
Assuming your working in the repository root directory and the configuration file is `parameter.dat`, you can start the game with:
```
sudo python src/main.py parameter.dat
```
You can find an example of parameter file, `parameter_TEST.dat`, based on the files in the `test_game` directory. 

## Useful keyboard shortcuts in Ubuntu 18:
- Move the game windows from a display to another: Shift + Windows + dx/sx
- Fullscreen: Windows+up/down

## Additional remarks

In order to avoid libpng error messages, convert all the images used in the game with imagemagick:
```
convert *.png -set filename:base "%[base]" "%[filename:base].png"
```

TODO PRIMA DELLA RELEASE:
- verificare copyright immagini fisici
- copyright timer + gong?
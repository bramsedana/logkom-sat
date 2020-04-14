# Latin Square Validator

This application is to serve as an assignment for the 2020 Computational Logic course in Universitas Indonesia.

## Contributors:
- Bram Sedana
- Michael Giorgio
- Rahmania Astrid Mochtar

## Setup and Install

Make sure you have python3 installed.

1. Clone this repository
2. cd to repo directory
3. Install the package requirements
```
pip install -r requirements.txt
```
4. Run the program
```
python gui.py
```

**Note: if on running the program there is an error saying a module is not found, please install the module manually by running:
```
pip install <module_name>

ex: pip install minisat
```
## Using the Application

There are 9 buttons on a 3x3 tile in the center of the application. On click, the button will show an image of a pokemon and can't be changed again. After each click, different pokemons will show up from a roaster of 3 in order. The objective is to have a set of row and columns that have unique pokemons inside each of them. After all tiles are inserted a pokemon, click the 'Submit' button to validate the answer. If there is a mistake and wish to reset the tile, then simply click on the 'Reset' button and all tiles will be blank again.

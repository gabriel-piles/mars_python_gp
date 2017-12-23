#### Design

This program has been coded in Python and it is divided into 5 classes:

  * CommunicationCenter: Entry point of the program. Read files and print the results.
  * InputParser: It parses and stores the inputs in a proper way
  * Grid: Store the grid shape and check if a position is into the grid
  * RoversController: Manage the rovers initializations and actions to avoid collisions and bad moves
  * Rover: It stores the rover state and manages the rover movement
  
#### Execution

##### 1. To execute the commands example

`python3 example.py`

##### 2. To execute a file of commands

`python3 file_execution.py`

##### 3. To execute the tests

```
pip install pytest
cd tests
pytest -v
```

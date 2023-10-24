# Zooma

The goal of this project is to provide a web API for the management of
zoos.

## Structure

### zoo_objects.py

In this file the base classes Animal, Caretaker and Enclosure are
defined. These classes are used in the Zoo.
For each class there exists its own test file:

- animal_test.py
- caretaker_test.py
- enclosure_test.py

### zoo.py

This file defines the class Zoo and contains all the logic needed for
managing a zoo. Most of the API calls depend solely on methods from this
class.
There exists a test file for this class:

- zoo.py

### api.py

This file is the heart of the project, as it contains all the API calls.
For defining how objects like Animal, Caretaker, Enclosure and so on
should be encode the following file is used:

- api_json_utils.py

There exists a test file for all the API calls:

- api_test.py

#### conftest.py

This file contains all the pytest fixtures that can be used by all the
test cases without the need of importing them

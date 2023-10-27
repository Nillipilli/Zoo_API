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

## HTTP Methods Summary

### Animal

- **POST** /animal
  - Description: Add a new animal (parameters: age, species_name, common_name).
    This method returns all the details of the animal, including the ID of the
    animal after it is added to the zoo.

- **GET** /animal/<animal_id>
  - Description: Return the details of an animal with the given animal_id.

- **DELETE** /animal/<animal_id>
  - Description: Delete the animal with the given animal_id.

- **GET** /animals
  - Description: Return a list of all animals with all the details about
    each animal.

- **POST** /animal/<animal_id>/feed
  - Description: Calling this method will feed the animal. Keep track of the
    time and date.

- **POST** /animal/<animal_id>/vet
  - Description: Calling this method will trigger a medical checkup for
    the animal. Keep track of the time and date.

- **POST** /animal/<animal_id>/home
  - Description: Assign a home to the animal (parameters: enclosure_id). Make
    sure to remove the animal from the original enclosure it used to live in.

- **POST** /animal/birth
  - Description: A new animal is born (parameters: mother_id). The child lives
    in the same enclosure as the mother and shares the species and common name.

- **POST** /animal/death
  - Description: An animal has died (parameters: animal_id).

- **GET** /animal/stats
  - Description: Get statistics about the zoo animals:
    - Total number of animals per species (based on the scientific name)

### Enclosure

- **POST** /enclosure
  - Description: Add a new enclosure to the zoo (parameters: name, area).

- **GET** /enclosure/<enclosure_id>
  - Description: Return the details of an enclosure with the
    given enclosure_id.

- **DELETE** /enclosure/<enclosure_id>
  - Description: Delete the enclosure with the given enclosure_id. Transfer the
    animals in the corresponding enclosure to another enclosure first.

- **GET** /enclosures
  - Description: Return the details of all the enclosures.

- **POST** /enclosures/<enclosure_id>/clean
  - Description: Calling this method will trigger a clean-up of the enclosure.
    Keep track of the time and date.

- **GET** /enclosures/<enclosure_id>/animals
  - Description: Get the details of all the animals living in the corresponding
    enclosure.

- **GET** /enclosure/stats
  - Description: Get statistics about the zoo enclosures:
    - Average number of animals in enclosures
    - List of all enclosures with multiple different animal species
    - Available space per animal per enclosure

### Employee

- **POST** /caretaker
  - Description: Add a new caretaker (parameters: name, address).

- **GET** /caretaker/<caretaker_id>
  - Description: Return the details of a caretaker with the
    given caretaker_id.

- **DELETE** /caretaker/<caretaker_id>
  - Description: Delete the caretaker with the given caretaker_id. Transfer the
    animals assigned to the corresponding caretaker to another caretaker first.

- **GET** /caretakers
  - Description: Return the details of all the caretakers.

- **POST** /caretaker/<caretaker_id>/care/<animal_id>
  - Description: Assign an animal to a caretaker. Make sure that every animal
    has only one caretaker.

- **GET** /caretaker/<caretaker_id>/care/animals
  - Description: Get a list of animals under the supervision of a caretaker.

- **GET** /caretaker/stats
  - Description: Get statistics about the caretakers:
    - Minimum number of animals assigned to one caretaker
    - Maximum number of animals assigned to one caretaker
    - Average number of animals assigned to one caretaker

### Plan Generation

- **GET** /tasks/medical
  - Description: Generate a medical check-up plan for all the animals. For
    every animal, calculate the next date for a medical check-up.

- **GET** /tasks/feeding
  - Description: Generate a feeding plan for all the animals. For every animal,
    calculate the next date for feeding and the person responsible for feeding.

- **GET** /tasks/cleaning
  - Description: Generate a cleaning plan for all the enclosures. For every
    enclosure, calculate the next date for cleaning and the person responsible
    for cleaning.

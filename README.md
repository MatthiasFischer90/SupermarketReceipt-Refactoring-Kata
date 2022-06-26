# The Supermarket Receipt Refactoring Kata (Matthias Fischer)

This repo contains the refactored result of the Supermarket Receipt Refactoring Kata, worked on by Matthias Fischer as part of the tech challenge for Sonnen.

This README file explains how to set up the project and run the tests. It also lists in detail what changes have been implemented compared to the initial template, as well as what decisions have been made along the way.

## Setup

Instead of using a `requirements.txt` for the Python dependencies like in the project template, the dependencies are now managed via [Pipenv](https://pipenv.pypa.io/). This allows for much more flexibility in dependency management, offering dependency version ranges for development, as well as fixed versions for deployments.

As requested, the project has been set up to be compatible with Python 3.9+.

First, install Pipenv (preferably in a virtual environment):

```
pip install pipenv
```

Afterwards, in order to run the tests, install all dependencies (including the dev dependencies):

```
pipenv install --dev
```

## Tests

The project contains simple unit tests, as well as bigger tests that cover more complex scenarios - if this project was connected to an actual database, these more complex tests would be the closest thing to e2e tests. All tests are contained in the `tests/` subdirectory.

The tests in `tests/test_supermarket.py` test the complete purchasing process, from defining SupermarketCatalogs and Products, to adding Products to ShoppingCarts, to calculating prices and Discounts, to creating Receipts.

The tests in `tests/test_text_receipt_printer.py` and `tests/test_html_receipt_printer.py` create text representations of given Receipts in a text format and an HTML format, respectively, and compare these text representations to the files in `tests/approved_files/`.

All other test files contain unit tests.

In order to run all tests, as well as print the code coverage, you can use the provided Makefile:

```
make test
```

Alternatively, you can run the test command manually:

```
pytest --approvaltests-use-reporter='PythonNative' --cov
```

## What changes have been made?

### New features

Both of the features requested in the template have been implemented in this repo. This means:

- Bundles can now be created, which apply to multiple Products and offer a percentage discount when these Products are purchased together
- an HTML printer has been implemented, which creates (very basic) HTML representations of given Receipts

### Refactoring

The main goal of this task was to refactor the given project, so this is where a lot of effort has been put. This section outlines the changes that have been made.

It should (hopefully) also be reasonably simple to get an understanding about the changes by going through the commit history (see the section at the end of this README file).

#### Project structure and setup changes

- Removed code for all languages other than Python
- Formatted all Python files using [Black](https://github.com/psf/black) (done continuously through all commits)
- Started tracking dependencies using [Pipenv](https://pipenv.pypa.io/) instead of a requirements.txt file
- Updated `.gitignore` file
- Added `setup.cfg` file to provide configuration for tests, as well as generate code coverage with every test
- Added Makefile for running tests

#### Code style and formatting changes

- Added [type hints](https://docs.python.org/3/library/typing.html) to all classes and functions
- Renamed functions, methods, and variables whose names were either inconsistent or didn't follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Refactored all function and method calls to always use [named arguments](https://www.w3schools.com/python/gloss_python_function_keyword_arguments.asp); this improves code readability and increases the visibility of bugs caused by renamed parameters (see also: [link](https://trstringer.com/python-named-arguments/))
- Added Docstrings in many modules, classes, public methods, and functions
- Sorted imports in all files using [isort](https://pycqa.github.io/isort/)

#### Business logic and test changes

- Created comprehensive unit and e2e tests
- Created new `discount_creation.py` module, which contains a vastly cleaned up and expanded version of the Discount creation logic that was previously located in the ShoppingCart class
- Changed all prices to be in cents instead of euros (and converted back to euros when Receipts are printed), so that price values can be stored as integers instead of floats; this avoids rounding errors in calculations and would make it easier to store values in a database
- Updated ShoppingCart to be associated with a specific SupermarketCatalog, and have it raise an Exception if Products that are to be added to the ShoppingCart don't belong to the same SupermarketCatalog
- Added \_\_str\_\_ method to Product class for better string representation in Exception messages
- Added checks in many functions and methods that raise Exceptions on invalid input values

### Additional noteworthy decisions

The code template, which served as a basis for this refactoring task, provided a code base and a list of requirements to fulfill. Nonetheless, since there is not a comprehensive list of business decisions that explains certain decisions that have been made for the existing template code in this theoretical project, some decisions had to be made while working on this refactoring task that are now outlined here.

#### Changes in database models

Some changes have been made in the `model_objects.py` file. For this refactoring task, this of course works without problems, but in an actual app, the classes defined in that module would represent database models that might not be easy to update because of external dependencies. The requirements in this project did not mention that the models are unchangeable, so the decision has been made to treat them as changeable.

These model changes include:

- Completely removing the `ProductQuantity` model; it has been made superfluous by code changes. In an actual app, it might still be desireable to keep this model to track purchases.
- The `argument` field in the Product class has been renamed to `optional_argument`

#### Total price of receipt can be zero

When Products are bought in low enough quantities (e.g. buying a single gram of apples), it's possible to get a receipt with a total price of zero cents. This could be changed pretty easily, e.g. by updating the `get_total_price_cents` method in the Receipt class to return `max(total, 1)` (i.e. always have a minimum price of at least one cent). However, this is not a clearly defined business requirement, and there might be cases where it's desired to have a price of zero cents (e.g. limited 100% discount coupons for a specific product), so no change has been implemented.

#### Assumptions made for Offers and Bundles

Some decisions have been made regarding the behaviors of Offers and Bundles:

- Bundles can only be created for Products that have `ProductUnit.EACH`. Otherwise, in a Bundle with toothbrushes and apples, buying a single gram of apples would qualify both toothbrushes and apples for the Discounts. Also, counting the quantity of purchased items to determine how much of the Discount to apply would otherwise be very arbitrary (How many apples do I need to buy to get the Discount for 2 toothbrushes? 2 kilograms?).
- Bundles can only be created for Products that do not have Offers yet, and vice versa. For the Offers, the logic already implicitly existed in the template and prevented multiple Offers from being created for a Product by overriding the old Offer. Now, explicit checks raise Exceptions if an Offer or a Bundle is being created for a Product that already has an Offer or a Bundle.

#### Raised Exceptions

The project now contains several places where Exceptions are raised when invalid values are encountered; these Exceptions are either [ValueErrors](https://docs.python.org/3/library/exceptions.html#ValueError) or custom Exceptions, depending on the situation. In an actual app, these Exceptions would then be caught higher up, logged, and dealt with appropriately according to the situation; for this refactoring project, the Exceptions are just raised and not caught.

#### Thoughts about storing quantities in grams instead of kilograms

One change in this project has been to store price values in cents instead of euros. This has the advantage that prices can now be stored and calculated with as integers, which is vastly prefered to working with floats.

Another part in the app where a lot of float values are used are product quantities. If a Product price is calculated by weight, the Product quantity is measured in kilograms via a float with three decimal places.

Considerations have been made to change the unit from kilograms to grams, so that, once again, integers could be used. However, this would result in extremely low unit prices, often less than one cent per gram, which again introduces fractions.

One idea could be to start measuring the quantities in grams, but keep the prices for kilograms, as they are, and then simply divide them by 1000 when the total prices are calculated. However, for this project, no such change has been made, and the kilogram measurement has been kept as is.

## The commit history

When implementing the changes for this repo, the goal was to create git commits that make it as easy as possible to understand and follow the individual changes, so best practices for commit messages have been followed.

For the commit message subject lines, the guidelines for [Semantic Commit Messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716) have been followed.

Emphasis has been put on creating many, but atomic commits instead of few commits that introduce many changes.

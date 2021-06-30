# COVIDPLOT¶
This package contains the following classes:

* CovidPlotter : Class to request and plot the covid cases for country
* Connector : Class for getting data from covid-api as a dict
As this is a coding test the class Connector is included only to show the use of heritage. This class can be easily included into the class CovidPlotter.

The class Connector uses functions of the packages pandas and plotly. In addition, it uses a global function, myCaps, defined out of the class definition.

The input is handled by filtering cases:
* 1-word country names
* multi-word country names
* ' and - cases
* explicit exceptions: US

The code shows examples of:
* Documentation
* OOP
* List comprehension
* Handle of exceptions

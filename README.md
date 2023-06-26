# Lectures & Lesroosters

## Table of Contents

* [Introduction](#introduction)
* [Project Overview](#project-overview)
* [Installation](#installation)
* [Usage](#usage)
* [Folder Structure](#project-structure)
* [Project Summary](#project-summary)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## Introduction
This case is based on the University Timetabling Problem, which is inspired by the University of Amsterdam Computer Science track. In this project the timetabling problem contains 29 courses, 609 students and 7 locations. In order to solve this case, several algorithms are used to create the optimal timetable. Algorithms such as: greedy, random-greedy, beam search, hillclimber and simulated annealing.

## Project Overview

## Installation

1. Download Python version 3.10.6
2. Clone the repository: `git clone https://github.com/11907223/lesroosters`
3. Navigate to the project directory: `cd lesroosters`
4. Create a virtual environment for the visualisations: `python3 -m venv venv`
5. Activate the virtual environment:
   - For Mac/Linux: `source venv/bin/activate`
   - For Windows: `venv\Scripts\activate.bat`
6. Install the required dependencies: `pip install -r requirements.txt`

## Usage

To run all algorithms
`python3 main.py`

To see visualisation
`flask run`

## Folder Structure

- `lesroosters/`: Contains all the necessary code and data for this research project.
    - `main.py`: Main program to run to find research results.
    - `libraries/`: Contains all the code to run main.py.
        - `algorithms/`: Contains all the algorithm classes.
        - `classes/`: Contains all the static classes that represent data.
        - `helpers/`: Contains all the helper functions.
    - `data/`: Contains all data in csv files and a data analysis in jupyter notebook.
    - `results/`: Contains all the resulting data from the research.
    - `images/`: Contains image files of results and UML.
    - `requirements.txt`: Lists the required Python packages and their versions.
    - `visualization/`: Generated PDF for user to download.
        - `app.py`: Defines the application routes and all the back-end code.
        - `.env`: Evironment variable configuration file.
        - `static/`: Holds static assets such as CSS.
        - `templates/`: Contains HTML templates for rendering the views.


## Project Summary

## Acknowledgements
This project was conducted by Niels Huang, Nina van der Meulen en Elise van Iterson.

Special thanks to Quinten van der Post and Moos Middelkoop for guiding us through this process.

## Contact


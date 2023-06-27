# Lectures & Lesroosters

## Table of Contents

* [Introduction](#introduction)
* [Project Overview](#project-overview)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Project Summary](#project-summary)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## Introduction
This project aims to generate an optimal university timetable. It is based on the University Timetabling Problem. As an [NP-Hard problem](https://en.wikipedia.org/wiki/NP-hardness), there is no solution that solves the problem in polynomial time. It is currently possible to acquire an approximation of an optimal solution. This is done through several optimalisation algorithms.

The results of several runs of the algorithms can be found in the results folder. This project provides insights and visualisations of choices to be made for problem optimalisation. The results and findings can be used for further optimalisation of algorithms to approach an optimal schedule.

## Project Overview
Data stems from the University of Amsterdam Computer Science track. The timetabling problem tackled in this project contains 29 courses, 609 students and 7 locations. In order to solve this case, several algorithms are used to create the optimal timetable. The following algorithms are used for problem optimalisation:
* Greedy
* Random-Greedy
* Beam Search
* Hill Climber
    - Steepest Ascend
    - Stochastic
    - Random-Restart (Meta-algorithm)
* Simulated Annealing

## Installation

1. Download Python version 3.10.6.
2. Clone the repository: 
```bash
git clone https://github.com/11907223/lesroosters
```
3. Navigate to the project root directory.
4. Create a virtual environment for the visualisations: 
```bash
python3 -m venv venv
```
5. Activate the virtual environment:
   - For Mac/Linux: 
   ```bash
   source venv/bin/activate
   ```
   - For Windows: 
   ```bash
   venv\Scripts\activate.bat
   ```
6. Install the required dependencies: 
```bash
pip install -r requirements.txt
```

## Usage

To see explanation of main.py amnd commandline arguments run:
```bash
python3 main.py -h
```

Structure of command line argument:
```bash
python3 main.py a [--help] [--n N] [--hr HR]
```

To run random 10 times:
```bash
python3 main.py random --n 10
```

To run greedy once:
```bash
python3 main.py greedy
```

## Project Structure

- [libraries:](libraries/) Contains all the code to run main.py.
    - [algorithms:](/libraries/algorithms/) Contains all the algorithm classes.
    - [classes:](/libraries/classes/) Contains all the static classes that represent data.
    - [helpers:](/libraries/helpers/) Contains all the helper functions.
        - [experiments:](/libraries/helpers/experiments/) Contains scripts to perform experiments.
- [data:](/data/) Contains all data in csv files and a data analysis in jupyter notebook.
- [results:](/results/) Contains all the resulting data from the research.
- [images:](/images/) Contains image files of results and UML.
- [requirements.txt](/requirements.txt) Lists the required Python packages and their versions.
- [visualization:](/visualization/) Generated PDF for user to download.
    - [static:](/visualization/static/) Holds static assets such as CSS.
    - [templates:](/visualization/templates/) Contains HTML templates for rendering the views.


## Project Summary

## Acknowledgements
This project was performed by Niels Huang, Nina van der Meulen en Elise van Iterson.

Special thanks to Quinten van der Post and Moos Middelkoop for guiding us through this process.

## Contact
Inquiries about the project can be mailed to niels.huang@student.uva.nl
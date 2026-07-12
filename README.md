# Habit Tracker Application
This is a python backend for a habit tracking application I built for the IU portfolio course using Object-Oriented and Functional Programming with Python.

## Overview
This application allows users to create, manage, edit, and delete daily and weekly habits. Users can mark habits as completed, view predefined habits, and track their progress through reports and streak analytics.

## Project Structure
```shell

oofpp_habits_project/
│
├── files/
   ├── data.db
   └── predefined-habits.db
├── UML/
   └── Diagram.png 
├── habit.py           
├── database.py        
├── analytics.py       
├── seed_data.py       
├── cli.py             
├── requirements.txt   
└── tests/
   ├── conftest.py    
   └── test_habits.py 
```


![Diagram.png](UML/Diagram.png)


## Installation
1. Clone the Repository
```shell
```
2. Navigate to the Project Folder
```shell
cd
```
3. Install Dependencies
```shell
pip install -r requirements.txt
```

## Running the Application
start
```shell
python main.py
```
and follow the instructions in screen

## Tests
```shell
pytest .
```
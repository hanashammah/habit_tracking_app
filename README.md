# Habit Tracker Application
This is a Python backend for a habit tracking application built using object-oriented and functional programming.

## Overview
This application allows users to create, manage, edit, and delete daily and weekly habits. Users can mark habits as completed, view predefined habits, and track their progress through reports and streak analytics.

## Project Structure
```shell

oofpp_habits_project/
│
├── files/
   ├── data.db
   └── predefined-habits.db
├── Screenshots/
   ├── Diagram.png
   ├── Screenshot 2025-09-14 213031.png
   ├── Screenshot 2025-09-14 213855.png
   ├── Screenshot 2025-09-14 224054.png
   ├── Screenshot 2025-09-14 224252.png
   ├── Screenshot 2025-09-14 224437.png
   ├── Screenshot 2025-09-14 224642.png
   ├── Screenshot 2025-09-15 151325.png
   └── Screenshot 2026-07-12 155756.png  
├── .gitignore  
├── db.py           
├── habit_tracker.py        
├── main.py       
├── README.md       
├── requirements.txt            
└──  test.py   
```

## UML Class Diagram
![Diagram.png](Screenshots/Diagram.png)

## Screenshots
### Menu
![Screenshot 2025-09-14 213031.png](Screenshots/Screenshot%202025-09-14%20213031.png)
### Create a habit
![Screenshot 2025-09-14 213855.png](Screenshots/Screenshot%202025-09-14%20213855.png)
### Modify a habit
![Screenshot 2025-09-14 224054.png](Screenshots/Screenshot%202025-09-14%20224054.png)
### View Reports
![Screenshot 2025-09-14 224252.png](Screenshots/Screenshot%202025-09-14%20224252.png)
### Check-off
![Screenshot 2025-09-14 224437.png](Screenshots/Screenshot%202025-09-14%20224437.png)
### Remove a habit
![Screenshot 2025-09-14 224642.png](Screenshots/Screenshot%202025-09-14%20224642.png)
### View predefined habits
![Screenshot 2025-09-15 151325.png](Screenshots/Screenshot%202025-09-15%20151325.png)
### Running the tests
![Screenshot 2026-07-12 155756.png](Screenshots/Screenshot%202026-07-12%20155756.png)

## Installation
1. Clone the Repository
```shell
git clone https://github.com/hanashammah/habit_tracking_app.git
```
2. Navigate to the Project Folder
```shell
cd habit_tracking_app
```
3. Install Dependencies
```shell
pip install -r requirements.txt
```

## Running the Application

Run the application with:

```shell
python main.py
```
Follow the instructions shown on the screen.

## Tests
Run the unit tests with:
```shell
pytest .
```
import sys
import os
import pandas as pd
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow, QStackedWidget, QTimeEdit, QInputDialog
from PyQt6.QtGui import QIntValidator, QPalette, QColor
import numpy as np
import webbrowser
import datetime as dt
from dataclasses import dataclass

# Define constants for better readability
NUM_HOURS = 24

STYLESHEET1 = """
            QMainWindow{
                background-color: #9DBEBB;      
            }
            QPushButton{
                color: #031926;
                background-color: #468189;
                padding: 5px;     
                border: none;
                border-radius: 5px; 
                margin: 2px;    
            }
            *{
                color: #031926;
                font-family: "Poppins";
                font-size: 13px;
                font-weight: 400;
            }
            #LabelHeader{
                color: #254D58; 
                background-color: #77ACA2;
                padding: 10px 10px;
                border-radius: 10px;
                font-family: "Poppins";
                font-size: 20px;
                font-weight: 800;
                text-align: center;
                min-height: 30px;
            }
            #LabelSubHeader{
                color: #254D58;
                font-family: "Poppins";
                font-size: 14px;
                font-weight: 400;
            }
            #ActivityNumber{
                    color: #254D58; 
                    padding: 10px 10px;
                    font-family: "Poppins";
                    font-size: 15px;
                    font-weight: 600;
            }
            QLineEdit{
                color: #031926;
                background-color: #77ACA2;
                padding: 5px 2.5px;
                border-radius: 5px;  
            }
            QTimeEdit{
                color: #031926;
                background-color: #77ACA2;
                padding: 5px 2.5px;
                border-radius: 5px; 
            }            
        """

STYLESHEETWARNING = """
            QMessageBox { 
                background-color: #E76B74; 
            } 
            QMessageBox QLabel { 
                color: #561D25; 
                font-family: "Poppins";
                font-size: 15px;
                text-align: center;
            } 
            QMessageBox QPushButton { 
                color: #561D25; background-color: #EA526F;
                font-family: "Poppins";
                font-size: 12px;
                font-weight: 400;
                border-radius: 5px;
                min-width: 130px;
                min-height: 30px;
                text-align: center;
                alignment: center;
            }
"""
STYLESHEETSUCCESS = """
            QMessageBox { 
                background-color: #96E8BC; 
            } 
            QMessageBox QLabel { 
                color: #3A623F; 
                font-family: "Poppins";
                font-size: 15px;
                alignment: center;
            } 
            QMessageBox QPushButton { 
                color: #3A623F; background-color: #7DD181;
                font-family: "Poppins";
                font-size: 12px;
                font-weight: 400;
                border-radius: 5px;
                min-width: 130px;
                min-height: 30px;
                text-align: center;
                alignment: center;
            }
"""
STYLESHEETQUESTION = """
            QMessageBox {
                background-color: #F2F3AE;
            }
            QMessageBox QLabel { 
                color: #FC9E4F; 
                font-family: "Poppins";
                font-size: 15px;
                alignment: center;
            } 
            QMessageBox QPushButton { 
                color: #FC9E4F; background-color: #EDD382;
                font-family: "Poppins";
                font-size: 12px;
                font-weight: 400;
                border-radius: 5px;
                min-width: 70px;
                min-height: 30px;
                text-align: center;
                alignment: center;
            }
"""


# Data class to represent User
@dataclass(order=True)
class User:
    Username: str = 'default'
    Password: str = 'default'
    Email: str = 'default'

# Read data from CSV to DataFrame
def csvData(file):
    df = pd.read_csv(file)
    return df

# Convert DataFrame rows to User objects
def csvDataToClassObject(object):
    users = []
    for row in object.itertuples(index=False):
        Username, Password, Email = row
        user = User(
            Username=Username,
            Password=Password,
            Email=Email,
        )
        users.append(user)
    return users

# Login Page
class LoginPage(QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.init_ui()
        self.loadUserData()
        


    def init_ui(self):
        # Initialize UI elements
        self.setStyleSheet(STYLESHEET1)

        self.setWindowTitle('Login Page')
        self.setGeometry(300,300, 300, 300)

        # Widgets
        self.labelHeader = QLabel('Login')
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setObjectName("LabelHeader")
        self.labelSubHeader = QLabel('Camp Organiser-3000')
        self.labelSubHeader.setObjectName('LabelSubHeader')
        self.labelUsername = QLabel('Username:')
        self.labelPassword = QLabel('Password:')
        self.editUsername = QLineEdit()
        self.editPassword = QLineEdit()
        self.editPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.btnLogin = QPushButton('Login')
        self.btnLogin.setMinimumHeight(30)
        self.btnPasswordState = QPushButton('Show')
        self.btnPasswordState.setCheckable(True)
        self.btnPasswordState.setChecked(False)
        self.btnSignUp = QPushButton('Sign Up')
        self.btnSignUp.setMinimumHeight(30)

        # Layouts
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)

        formLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        formLayout.addWidget(self.labelHeader)
        formLayout.addWidget(self.labelSubHeader)
        formLayout.addWidget(self.labelUsername)
        formLayout.addWidget(self.editUsername)
        formLayout.addWidget(self.labelPassword)
        formLayout.addWidget(self.editPassword)
        formLayout.addWidget(self.btnPasswordState)
        self.btnPasswordState.setMaximumSize(QtCore.QSize(50,30))
        layout.addLayout(formLayout)
        buttonLayout.addWidget(self.btnLogin)
        buttonLayout.addWidget(self.btnSignUp)
        layout.addLayout(buttonLayout)

        # Connect the login button to the login function
        self.btnLogin.clicked.connect(self.login)
        # Connect the hide/show button to the hide/show function
        self.btnPasswordState.clicked.connect(self.passwordState)

        self.btnSignUp.clicked.connect(self.signUp)
        self.btnSignUp.clicked.connect(self.hide)

        self.setCentralWidget(widget)
        self.show()

    def signUp(self):
        # Open the Sign-Up page
        self.signUpPage = SignUpPage()
        self.signUpPage.show()

    def loadUserData(self):
        # Load user data from CSV and convert to class objects
        userData = csvData('validLogins.csv')
        self.users = csvDataToClassObject(userData)

    def login(self):
        # Attempt user login
        username = self.editUsername.text()
        password = self.editPassword.text()

        for user in self.users:
            if user.Username == username and user.Password.strip() == password:
                successBox = QMessageBox()
                successBox.setWindowTitle("Success")
                successBox.setText("Login Successful")
                successBox.setStyleSheet(STYLESHEETSUCCESS)
                successBox.exec()
                self.HomePage = HomePage(username=username)
                self.hide()
                self.HomePage.show()
                return

        # If login fails, show an error message
        warningBox = QMessageBox()
        warningBox.setWindowTitle("Warning")
        warningBox.setText("Invalid Login!")
        warningBox.setStyleSheet(STYLESHEETWARNING)
        warningBox.exec()
                

    def passwordState(self, checked):
        # Toggle password visibility
        if checked:
            self.btnPasswordState.setText('Hide')
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.btnPasswordState.setText('Show')
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Password)
class HomePage(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        
    def init_ui(self):

        self.setStyleSheet(STYLESHEET1)

        self.setWindowTitle('Home Page')
        self.setGeometry(200, 200, 300, 150)

        self.labelHeader = QLabel('Home')
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setObjectName("LabelHeader")
        self.labelSubHeader = QLabel('Camp Organiser-3000')
        self.labelSubHeader.setObjectName('LabelSubHeader')
        self.btnNewSolutionPage = QPushButton('New Solution')
        self.btnPastSolutions = QPushButton('Past Solutions')
        self.btnLogOut = QPushButton('Log Out')

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        layout.addWidget(self.labelHeader)
        layout.addWidget(self.labelSubHeader)
        layout.addWidget(self.btnNewSolutionPage)
        layout.addWidget(self.btnPastSolutions)
        layout.addWidget(self.btnLogOut)

        self.btnNewSolutionPage.clicked.connect(self.goToNewSolPage)
        self.btnPastSolutions.clicked.connect(self.goToPastSolPage)
        self.btnLogOut.clicked.connect(self.goToLoginPage)

        self.setCentralWidget(widget)
        self.show()

    def set_username(self, username):
        self.username = username    

    def goToNewSolPage(self):
        self.newSolutionPage = NewSolutionPage(username=self.username)
        self.newSolutionPage.show()
        self.hide()

    def goToPastSolPage(self):
        username = self.username
        try:
            with open(f"{username}.txt", 'r') as file:
                lines = file.readlines()

            if len(lines) > 0:
                self.PastSolutionsPage = PastSolutionsPage(username=self.username)
                self.PastSolutionsPage.show()
                self.hide()
            else:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("No past solutions available for this account!")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
        except FileNotFoundError:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("No past solutions available for this account!")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
    
    

    def goToLoginPage(self):
        self.loginPage = LoginPage()
        self.hide()

class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLESHEET1)
        layout = QVBoxLayout(self)
        self.labelCampName = QLabel('Camp Name:')
        self.labelNumStudents = QLabel('Amount of students:')
        self.labelNumTeachers = QLabel('Amount of teachers:')
        self.labelNumLeaders = QLabel('Amount of leaders:')
        self.labelNumActivities = QLabel('Amount of activities:')
        self.editNumStudents = QLineEdit()
        self.editNumTeachers = QLineEdit()
        self.editNumLeaders = QLineEdit()
        self.editNumActivities = QLineEdit()
        self.editCampName = QLineEdit()

        layout.addWidget(self.labelCampName)
        layout.addWidget(self.editCampName)
        layout.addWidget(self.labelNumStudents)
        layout.addWidget(self.editNumStudents)
        layout.addWidget(self.labelNumTeachers)
        layout.addWidget(self.editNumTeachers)
        layout.addWidget(self.labelNumLeaders)
        layout.addWidget(self.editNumLeaders)
        layout.addWidget(self.labelNumActivities)
        layout.addWidget(self.editNumActivities)

        self.editNumStudents.setValidator(QIntValidator())
        self.editNumLeaders.setValidator(QIntValidator())
        self.editNumTeachers.setValidator(QIntValidator())
        self.editNumActivities.setValidator(QIntValidator())

class NewSolutionPage(QMainWindow):
    class Activity(QWidget):
        def __init__(self, i):
            super().__init__()
            self.setStyleSheet(STYLESHEET1)

            layout = QVBoxLayout(self)

            self.labelActivityHeader = QLabel(f'Activity {i+1}')
            self.labelActivityHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelActivityHeader.setObjectName("ActivityNumber")
            self.labelName = QLabel('Name:')
            self.labelNumStudents = QLabel('Students Needed:')
            self.labelNumTeachers = QLabel('Teachers Needed:')
            self.labelNumLeaders = QLabel('Camp Leaders needed:')
            self.labelStartTime = QLabel('Start time: (Activities must be added in ascending order)')
            self.labelEndTime = QLabel('End time:')
            self.editName = QLineEdit()
            self.editNumStudents = QLineEdit()
            self.editNumTeachers = QLineEdit()
            self.editNumLeaders = QLineEdit()
            self.editStartTime = QTimeEdit()
            self.editEndTime = QTimeEdit()


            layout.addWidget(self.labelActivityHeader)
            self.labelActivityHeader.setMinimumSize(QtCore.QSize(0, 40))
            layout.addWidget(self.labelName)
            layout.addWidget(self.editName)
            layout.addWidget(self.labelNumStudents)
            layout.addWidget(self.editNumStudents)
            layout.addWidget(self.labelNumTeachers)
            layout.addWidget(self.editNumTeachers)
            layout.addWidget(self.labelNumLeaders)
            layout.addWidget(self.editNumLeaders)
            layout.addWidget(self.labelStartTime)
            layout.addWidget(self.editStartTime)
            layout.addWidget(self.labelEndTime)
            layout.addWidget(self.editEndTime)

            self.editNumStudents.setValidator(QIntValidator())
            self.editNumLeaders.setValidator(QIntValidator())
            self.editNumTeachers.setValidator(QIntValidator())



    def __init__(self, username):
        super().__init__()
        self.init_ui()
        self.username = username
        self.activities = []      

    def init_ui(self):
        self.setStyleSheet(STYLESHEET1)

        self.setWindowTitle('New Solution Page')
        self.setGeometry(200, 200, 300, 150)

        self.stackedWidget = QStackedWidget(self)

        self.main = Page1()

        self.stackedWidget.addWidget(self.main)

        self.campName = self.main.editCampName
        self.numStudents = self.main.editNumStudents
        self.numTeachers = self.main.editNumTeachers
        self.numLeaders = self.main.editNumLeaders
        self.numActivities = self.main.editNumActivities

        self.btnGenerate = QPushButton('Generate')
        self.btnNextPage = QPushButton('Next')
        self.btnPrevPage = QPushButton('Prev')
        self.btnGenActivities = QPushButton('Generate Activities')
        self.btnHomePage = QPushButton('Home')

        self.btnGenerate.clicked.connect(self.checkGenSolution)
        self.btnPrevPage.clicked.connect(self.prev)
        self.btnNextPage.clicked.connect(self.next)
        self.btnGenActivities.clicked.connect(self.checkActivities)
        self.btnHomePage.clicked.connect(self.goHome)

        self.labelHeader = QLabel('New Camp')
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setObjectName("LabelHeader")
        self.labelSubHeader = QLabel('Camp Organiser-3000')
        self.labelSubHeader.setObjectName('LabelSubHeader')

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        # Header widget
        headerWidget = QWidget()
        headerLayout = QVBoxLayout()
        headerWidget.setLayout(headerLayout)

        headerLayout.addWidget(self.labelHeader)
        self.labelHeader.setMinimumSize(QtCore.QSize(0, 40))
        headerLayout.addWidget(self.labelSubHeader)

        # StackedWidget
        layout.addWidget(headerWidget)
        layout.addWidget(self.stackedWidget)

        # Buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnPrevPage)
        buttonLayout.addWidget(self.btnGenActivities)  # Initially, show only the 'Generate Activities' button
        buttonLayout.addWidget(self.btnGenerate)
        buttonLayout.addWidget(self.btnNextPage)

        self.btnPrevPage.hide()
        self.btnGenerate.hide()
        self.btnNextPage.hide()

        layout.addLayout(buttonLayout)

        layout.addWidget(self.btnHomePage)

        self.currentPage = 0
        self.stackedWidget.setCurrentIndex(self.currentPage)

        self.setCentralWidget(widget)
        self.show()

    def set_username(self, username):
        self.username = username

    def goHome(self):
        print(f"Going back to home page for user: {self.username}")
        self.HomePage = HomePage(username=self.username)  # Pass the username argument here
        self.HomePage.show()
        self.hide()

    def prev(self):
        self.currentPage = (self.currentPage - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(self.currentPage)

    def next(self):
        self.currentPage = (self.currentPage + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(self.currentPage)

    def checkGenSolution(self):
        if not self.checkActivitiesOrder():
            return

        try:
            campNameText = self.campName.text()
            numStudentsText = self.numStudents.text()
            numTeachersText = self.numTeachers.text()
            numLeadersText = self.numLeaders.text()

            if numStudentsText and numTeachersText and numLeadersText and campNameText:
                numStudents = int(numStudentsText)
                numTeachers = int(numTeachersText)
                numLeaders = int(numLeadersText)

                if numStudents > 0 and numLeaders > 0 and numTeachers > 0:
                    self.genSolution()
                else:
                    warningBox = QMessageBox()
                    warningBox.setWindowTitle("Error")
                    warningBox.setText("Number of People must be greater than 0")
                    warningBox.setStyleSheet(STYLESHEETWARNING)
                    warningBox.exec()
            else:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("Please enter valid values for all fields")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
        except ValueError:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Please enter valid inputs in every box")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()

    def checkActivitiesOrder(self):
        # Get the number of activities
        numActivitiesText = self.numActivities.text()
        if not numActivitiesText:
            return False

        numActivities = int(numActivitiesText)

        # Create a list to store the start times of activities
        start_times = []

        # Extract the start times from the activity widgets
        for i in range(numActivities):
            activity = self.activities[i]
            start_time = activity.editStartTime.time()
            start_times.append((start_time.hour(), start_time.minute()))

        # Check if the start times are in ascending order
        for i in range(1, numActivities):
            if start_times[i] < start_times[i - 1]:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Warning")
                warningBox.setText("Please ensure activities are in ascending order by start time.")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
                return False

        return True

    def checkActivities(self):
        try:
            numActivitiesText = self.numActivities.text()

            if numActivitiesText:
                numActivities = int(numActivitiesText)
                if numActivities > 0:
                    self.genActivities()
                else:
                    warningBox = QMessageBox()
                    warningBox.setWindowTitle("Error")
                    warningBox.setText("Number of Activities must be greater than 0")
                    warningBox.setStyleSheet(STYLESHEETWARNING)
                    warningBox.exec()
            else:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("Please enter a valid number of Activities")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
        except ValueError:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Please enter valid inputs in every box")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()

    def genActivities(self):
        numActivities = int(self.numActivities.text())

        for i in range(numActivities):
            activityWidget = self.Activity(i)
            self.activities.append(activityWidget)
            self.stackedWidget.addWidget(activityWidget)

        self.updateButtonsVisibility()

    def updateButtonsVisibility(self):
        self.btnPrevPage.show()
        self.btnGenerate.show()
        self.btnNextPage.show()

        # Hide the 'Generate Activities' button
        self.btnGenActivities.hide()


    def genSolution(self):
        class Person:
            def __init__(self, name, role):
                self.name = name
                self.role = role
                self.available = True   

        numStudents = int(self.numStudents.text())
        numTeachers = int(self.numTeachers.text())
        numLeaders = int(self.numLeaders.text())
        username = self.username

        if numStudents <= 0 or numTeachers <= 0 or numLeaders <= 0:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Number of People must be greater than 0")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
            return
        

        students = [Person(f"Student {i+1}", "Student") for i in range(numStudents)]
        teachers = [Person(f"Teacher {i+1}", "Teacher") for i in range(numTeachers)]
        leaders = [Person(f"Leader {i+1}", "Leader") for i in range(numLeaders)]

        scheduleDf = pd.DataFrame(columns=["Person", "Activity", "Start Time", "End Time"])

        usePlaceholderNames = QMessageBox.question(
            self, "Use Placeholder Names?", "Do you want to use placeholder names for people?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        
        if usePlaceholderNames == QMessageBox.StandardButton.No:
            # Define a function to prompt the user to enter a name for each role
            def enterNamesForRole(role, numPeople):
                while True:
                    names_input, ok = QInputDialog.getText(
                        self, 
                        f"Enter {role} Names", 
                        f"Enter names for {role} ({numPeople} needed, comma-separated):"
                    )
                    if not ok or not names_input:
                        QMessageBox.warning(self, 'Error', f"You must enter names for all {role}s.")
                        return None
                    names = names_input.split(", ")
                    if len(names) != numPeople:
                        QMessageBox.warning(self, 'Error', f"Please provide {numPeople} names for {role}.")
                    else:
                        # Add role indicator to each name
                        prefixed_names = [f"({role[0]}) {name}" for name in names]
                        return prefixed_names

            numStudents = int(self.numStudents.text())
            numTeachers = int(self.numTeachers.text())
            numLeaders = int(self.numLeaders.text())
            username = self.username

            if numStudents <= 0 or numTeachers <= 0 or numLeaders <= 0:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("Number of People must be greater than 0")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
                return

            studentNames = enterNamesForRole("Student", numStudents)
            if studentNames is None:
                return

            teacherNames = enterNamesForRole("Teacher", numTeachers)
            if teacherNames is None:
                return

            leaderNames = enterNamesForRole("Leader", numLeaders)
            if leaderNames is None:
                return

            students = [Person(name, "Student") for name in studentNames]
            teachers = [Person(name, "Teacher") for name in teacherNames]
            leaders = [Person(name, "Leader") for name in leaderNames]

            scheduleDf = pd.DataFrame(columns=["Person", "Activity", "Start Time", "End Time"])

        def isPersonAvailable(person, hourChunks, hour):
            return person.available and person not in hourChunks[hour]

        # Initialize the hourChunks dictionary to track occupied hours for each person
        hourChunks = {hour: set() for hour in range(24)}

        for activity in self.activities:
            numStudentsNeeded = int(activity.editNumStudents.text())
            numTeachersNeeded = int(activity.editNumTeachers.text())
            numLeadersNeeded = int(activity.editNumLeaders.text())

            startTime = activity.editStartTime.time()
            endTime = activity.editEndTime.time()

            startHour = startTime.hour()
            startMinute = startTime.minute()

            endHour = endTime.hour()
            endMinute = endTime.minute()

            # Calculate the number of hours for the activity
            numHours = endHour - startHour

            peopleNeeded = []

            for _ in range(numStudentsNeeded):
                availableStudents = [student for student in students if isPersonAvailable(student, hourChunks, startHour)]
                if not availableStudents:
                    warningBox = QMessageBox()
                    warningBox.setWindowTitle("Error")
                    warningBox.setText("Cannot find a valid solution with no available students")
                    warningBox.setStyleSheet(STYLESHEETWARNING)
                    warningBox.exec()
                    return
                student = np.random.choice(availableStudents)
                peopleNeeded.append(student)
                student.available = False
                for hour in range(startHour, startHour + numHours):
                    hourChunks[hour].add(student)

            for _ in range(numTeachersNeeded):
                availableTeachers = [teacher for teacher in teachers if isPersonAvailable(teacher, hourChunks, startHour)]
                if not availableTeachers:
                    warningBox = QMessageBox()
                    warningBox.setWindowTitle("Error")
                    warningBox.setText("Cannot find a valid solution with no available teachers")
                    warningBox.setStyleSheet(STYLESHEETWARNING)
                    warningBox.exec()
                    return
                teacher = np.random.choice(availableTeachers)
                peopleNeeded.append(teacher)
                teacher.available = False
                for hour in range(startHour, startHour + numHours):
                    hourChunks[hour].add(teacher)

            for _ in range(numLeadersNeeded):
                availableLeaders = [leader for leader in leaders if isPersonAvailable(leader, hourChunks, startHour)]
                if not availableLeaders:
                    warningBox = QMessageBox()
                    warningBox.setWindowTitle("Error")
                    warningBox.setText("Cannot find a valid solution with no available leaders")
                    warningBox.setStyleSheet(STYLESHEETWARNING)
                    warningBox.exec()
                    return
                leader = np.random.choice(availableLeaders)
                peopleNeeded.append(leader)
                leader.available = False
                for hour in range(startHour, startHour + numHours):
                    hourChunks[hour].add(leader)

            # Check if there is no solution
            if len(peopleNeeded) < (numStudentsNeeded + numTeachersNeeded + numLeadersNeeded):
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("There is no solution for creating a schedule without overlapping activities")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
                print("There is no solution for this problem.")
                break

            # Create a dataframe for the activity
            activityDf = pd.DataFrame(columns=["Person", "Activity", "Start Time", "End Time"])
            activityDf["Person"] = [person.name for person in peopleNeeded]
            activityDf["Activity"] = activity.editName.text()
            activityDf["Start Time"] = activity.editStartTime.text()
            activityDf["End Time"] = activity.editEndTime.text()
            scheduleDf = scheduleDf.append(activityDf, ignore_index=True)

            # Reset the availability of all people for the next activity
            for person in peopleNeeded:
                person.available = True

        print(scheduleDf)

        htmlCSS1 = """<!DOCTYPE html>
<html>
<head>
<title>Sort a HTML Table Alphabetically</title>
<style>

    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        border-radius: 5px 5px 0 0;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        margin-left: auto;
        margin-right: auto;
    }

    .styled-table thead tr {
        background-color: #3986BD;
        color: #ffffff;
        text-align: left;
        font-weight: bold;
        cursor: pointer;
    }

    .styled-table thead tr th:hover{
        background-color: #2A628F;
    }

    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #cfebff;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #2A628F;
    }

    .button-container-div {
        text-align: center;
    }

    .button {
    margin: 10px;
    padding: 8px 16px;
    background-color: #3986BD;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    align-self: center;
    }

    .button:hover {
    background-color: #2A628F;
    }

</style>
</head>
<body>
<table id="myTable" class="styled-table">
    <thead>
    <tr>
        <th onclick="sortTable(0)">Index</th>
        <th onclick="sortTable(1)">Person</th>
        <th onclick="sortTable(2)">Activity</th>
        <th onclick="sortTable(3)">Start Time</th>
        <th onclick="sortTable(4)">End Time</th>
    </tr>
    </thead>  
            """
        htmlCSS2 = """
<div class="button-container-div">
  <button class="button" onclick="printTable()">Print Table</button>
  <button class="button" onclick="exportToExcel()">Export to Excel</button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.1/xlsx.full.min.js"></script>
<script>
  function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("myTable");
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc"; 
    /* Make a loop that will continue until
        no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /* Loop through all table rows (except the
          first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
            one from the current row and one from the next: */
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        /* Check if the two rows should switch place,
            based on the direction, asc or desc: */
        if (dir == "asc") {
          if (n === 3 || n === 4) { // Check if it's a time column
            if (compareTimes(x.innerHTML, y.innerHTML) > 0) {
              shouldSwitch = true;
              break;
            }
          } else if (alphanumericalCompare(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase()) > 0) {
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (n === 3 || n === 4) { // Check if it's a time column
            if (compareTimes(x.innerHTML, y.innerHTML) < 0) {
              shouldSwitch = true;
              break;
            }
          } else if (alphanumericalCompare(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase()) < 0) {
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        // Each time a switch is done, increase this count by 1:
        switchcount++;      
      } else {
        /* If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again. */
        if (switchcount === 0 && dir === "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }
  
  // Custom alphanumerical comparison function
  function alphanumericalCompare(a, b) {
    return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
  }
  
  // Custom time comparison function
  function compareTimes(timeA, timeB) {
    const a = convertTo24HourFormat(timeA);
    const b = convertTo24HourFormat(timeB);
    return alphanumericalCompare(a, b);
  }
  
  // Convert AM/PM time to 24-hour format
  function convertTo24HourFormat(time) {
    const parts = time.split(/(\d+:\d+)([APMapm]{2})/);
    const hour = parseInt(parts[1].split(':')[0]);
    const minute = parseInt(parts[1].split(':')[1]);
    const ampm = parts[2].toUpperCase();
    if (ampm === 'PM' && hour !== 12) {
      return `${hour + 12}:${minute}`;
    } else if (ampm === 'AM' && hour === 12) {
      return `00:${minute}`;
    } else {
      return `${hour}:${minute}`;
    }
  }

  function printTable() {
    window.print();
  }
  
  function exportToExcel() {
    var table = document.getElementById("myTable");
    var wb = XLSX.utils.table_to_book(table);
    XLSX.writeFile(wb, "table.xlsx");
  }
</script>
</body>
</html>
        """

        title = self.campName.text()
        currentDate = dt.datetime.now().strftime("%Y-%m-%d")
        htmlFilename = f"{title}_{currentDate}.html"

        html = scheduleDf.to_html(index=True,header=False)

        # Write the HTML file
        textFile = open(htmlFilename, "w")
        textFile.write(htmlCSS1)
        textFile.write(html)
        textFile.write(htmlCSS2)
        textFile.close()

        # list to store file lines
        lines = []
        # read file
        with open(f"{title}_{currentDate}.html", 'r') as fp:
            # read an store all lines into list
            lines = fp.readlines()

        # Write file
        with open(f"{title}_{currentDate}.html", 'w') as fp:
            # iterate each line
            for number, line in enumerate(lines):
                # delete line 81. or pass any Nth line you want to remove
                # note list index starts from 0
                if number not in [80]:
                    fp.write(line)

        with open(f"{title}_{currentDate}.html", 'r') as file:
            fileLines = file.readlines()

        # Process lines after line 86
        for i in range(len(fileLines)):
            if i >= 81:  # Lines are 0-indexed, so line 82 is at index 81
                fileLines[i] = fileLines[i].replace('<th>', '<td>').replace('</th>', '</td>')

        # Save the modified lines back to a file
        with open(f"{title}_{currentDate}.html", 'w') as file:
            file.writelines(fileLines)

        file = open(f"{username}.txt", 'a')
        file.write(f"{htmlFilename}\n")
        file.close()

        # Open the generated HTML file in the user's web browser
        webpageDf = 'file:///' + os.getcwd() + '/' + htmlFilename
        webbrowser.open_new_tab(webpageDf)

class PastSolutionsPage(QMainWindow):
    class PastSolution(QWidget):
        def __init__(self, name, date):
            super().__init__()

            self.setStyleSheet(STYLESHEET1)

            layout = QVBoxLayout(self)

            self.labelName = QLabel(f"Name: {name}")
            self.labelDate = QLabel(f"Date: {date}")

            layout.addWidget(self.labelName)
            layout.addWidget(self.labelDate)

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet(STYLESHEET1)
        
        self.setWindowTitle('Past Solutions Page')
        self.setGeometry(200, 200, 400, 300)

        self.stackedWidget = QStackedWidget(self)
        self.activities = []

        self.main = Page1()
        username = self.username

        with open(f"{username}.txt", 'r') as file:
            lines = file.readlines()

        for line in lines:
            name, dateAndHtml = line.strip().split('_')
            date = dateAndHtml.strip().split('.')[0]
            campWidget = self.PastSolution(name, date)
            self.activities.append(campWidget)
            self.stackedWidget.addWidget(campWidget)

        self.btnNextPage = QPushButton('Next')
        self.btnRemove = QPushButton('Remove')
        self.btnSelect = QPushButton('Select')
        self.btnPrevPage = QPushButton('Prev')
        self.btnHomePage = QPushButton('Home')

        self.btnPrevPage.clicked.connect(self.prev)
        self.btnNextPage.clicked.connect(self.next)
        self.btnRemove.clicked.connect(self.remove)
        self.btnSelect.clicked.connect(self.select)
        self.btnHomePage.clicked.connect(self.goHome)

        self.labelHeader = QLabel('Past Solutions')
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setObjectName("LabelHeader")
        self.labelSubHeader = QLabel('Camp Organiser-3000')
        self.labelSubHeader.setObjectName('LabelSubHeader')
        

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        # Header widget
        headerWidget = QWidget()
        headerLayout = QVBoxLayout()
        headerWidget.setLayout(headerLayout)

        headerLayout.addWidget(self.labelHeader)
        headerLayout.addWidget(self.labelSubHeader)

        # StackedWidget
        layout.addWidget(headerWidget)
        layout.addWidget(self.stackedWidget)

        # Buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.btnPrevPage)
        buttonLayout.addWidget(self.btnRemove)
        buttonLayout.addWidget(self.btnSelect)
        buttonLayout.addWidget(self.btnNextPage)
        layout.addLayout(buttonLayout)

        layout.addWidget(self.btnHomePage)

        self.currentPage = 0
        self.stackedWidget.setCurrentIndex(self.currentPage)

        self.setCentralWidget(widget)
        self.show()

    def set_username(self, username):
        self.username = username

    def remove(self):
        if self.currentPage < 0 or self.currentPage >= len(self.activities):
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Invalid selection")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
            
            return

        selected_widget = self.activities[self.currentPage]
        selected_name = selected_widget.labelName.text().split(': ')[1]
        selected_date = selected_widget.labelDate.text().split(': ')[1]
        selected_html_file = f"{selected_name}_{selected_date}.html"

        try:
            # Remove the HTML file
            os.remove(selected_html_file)
            
            # Remove the line from the username.txt file
            with open(f"{self.username}.txt", 'r') as file:
                lines = file.readlines()
            with open(f"{self.username}.txt", 'w') as file:
                for line in lines:
                    if selected_html_file not in line:
                        file.write(line)
            
            # Remove the widget from the stacked widget
            self.activities.remove(selected_widget)
            self.stackedWidget.removeWidget(selected_widget)
            
            # Update the current page index and display
            self.currentPage = max(self.currentPage - 1, 0)
            self.stackedWidget.setCurrentIndex(self.currentPage)
            
            # If there are no more activities, go back to the Home Page
            if not self.activities:
                self.goHome()
                return
            
            successBox = QMessageBox()
            successBox.setWindowTitle("Success")
            successBox.setText("Solution removed successfully")
            successBox.setStyleSheet(STYLESHEETSUCCESS)
            successBox.exec()

        except FileNotFoundError:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Selected HTML file not found")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()

    def goHome(self):
        print(f"Going back to home page for user: {self.username}")
        self.HomePage = HomePage(username=self.username)
        self.HomePage.show()
        self.hide()

    def prev(self):
        self.currentPage = (self.currentPage - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(self.currentPage)

    def next(self):
        self.currentPage = (self.currentPage + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(self.currentPage)
    
    def select(self):
        if self.currentPage < 0 or self.currentPage >= len(self.activities):
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Invalid selection")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
            return

        selected_widget = self.activities[self.currentPage]
        selected_name = selected_widget.labelName.text().split(': ')[1]
        selected_date = selected_widget.labelDate.text().split(': ')[1]
        selected_html_file = f"{selected_name}_{selected_date}.html"

        try:
            with open(selected_html_file, 'r') as file:
                html_content = file.read()
            
            # Open the selected HTML file in the user's web browser
            webpageDf = 'file:///' + os.getcwd() + '/' + selected_html_file
            webbrowser.open_new_tab(webpageDf)

        except FileNotFoundError:
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Selected HTML file not found")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
            


# Sign-up Page
class SignUpPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # Initialize title and size
    def init_ui(self):

        self.setStyleSheet(STYLESHEET1)

        self.setWindowTitle('Sign Up')
        self.setGeometry(200, 200, 300, 250)

        # Widgets
        self.labelHeader = QLabel('Sign Up')
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelHeader.setObjectName("LabelHeader")
        self.labelSubHeader = QLabel('Camp Organiser-3000')
        self.labelSubHeader.setObjectName('LabelSubHeader')
        self.labelUsername = QLabel('Username:')
        self.labelPassword = QLabel('Password:')
        self.labelEmail = QLabel('Email:')
        self.editUsername = QLineEdit()
        self.editPassword = QLineEdit()
        self.editPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.btnPasswordState = QPushButton('Show')
        self.btnPasswordState.setCheckable(True)
        self.btnPasswordState.setChecked(False)
        self.editEmail = QLineEdit()
        self.btnSignUp = QPushButton('Sign Up')
        self.btnSignUp.setMinimumHeight(30)
        self.btnLogin = QPushButton('Login')
        self.btnLogin.setMinimumHeight(30)

        self.editUsername.textChanged.connect(self.validate_input)
        self.editPassword.textChanged.connect(self.validate_input)
        self.editEmail.textChanged.connect(self.validate_input)

        # Layouts
        layout = QVBoxLayout(self)

        formLayout = QVBoxLayout()
        formLayout.addWidget(self.labelHeader)
        self.labelHeader.setMinimumSize(QtCore.QSize(0,40))
        formLayout.addWidget(self.labelSubHeader)
        formLayout.addWidget(self.labelUsername)
        formLayout.addWidget(self.editUsername)
        formLayout.addWidget(self.labelPassword)
        formLayout.addWidget(self.editPassword)
        formLayout.addWidget(self.btnPasswordState)
        self.btnPasswordState.setMaximumSize(QtCore.QSize(50,30))
        formLayout.addWidget(self.labelEmail)
        formLayout.addWidget(self.editEmail)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnSignUp)
        btnLayout.addWidget(self.btnLogin)

        layout.addLayout(formLayout)
        layout.addLayout(btnLayout)

        # Connect the sign-up button to the sign-up function
        self.btnSignUp.clicked.connect(self.signup)
        self.btnSignUp.clicked.connect(self.hide)
        self.btnLogin.clicked.connect(self.login)
        self.btnLogin.clicked.connect(self.hide)
        self.btnPasswordState.clicked.connect(self.passwordState)

        # Initial validation
        self.validate_input()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

        self.show()

    def validate_input(self):
        username = self.editUsername.text()
        password = self.editPassword.text()
        email = self.editEmail.text()

        # Enable the "Sign Up" button only if all fields are non-empty
        is_valid = all((username, password, email))
        self.btnSignUp.setEnabled(is_valid)

    def passwordState(self, checked):
        if checked:
            self.btnPasswordState.setText('Hide')
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.btnPasswordState.setText('Show')
            self.editPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def signup(self):
        # Take user input from the form
        username = self.editUsername.text()
        password = self.editPassword.text()
        email = self.editEmail.text()

        if ',' in (username + password + email):
            warningBox = QMessageBox()
            warningBox.setWindowTitle("Error")
            warningBox.setText("Fields cannot contain commas")
            warningBox.setStyleSheet(STYLESHEETWARNING)
            warningBox.exec()
            self.SignUpPage = SignUpPage()
            self.SignUpPage.show()
            return

        # Load existing user data
        userData = csvData('validLogins.csv')
        existingUsers = csvDataToClassObject(userData)

        # Check if the email is already in use
        for user in existingUsers:
            if user.Email == email:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("Email is already in use. Please use a different email")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
                self.SignUpPage = SignUpPage()
                self.SignUpPage.show()
                return
            if user.Username == username:
                warningBox = QMessageBox()
                warningBox.setWindowTitle("Error")
                warningBox.setText("Username is already in use. Please use a different username")
                warningBox.setStyleSheet(STYLESHEETWARNING)
                warningBox.exec()
                self.SignUpPage = SignUpPage()
                self.SignUpPage.show()
                return

        # Append the user's details to the CSV file using pandas
        newUser = pd.DataFrame({'Username': [username], 'Password': [password], 'Email': [email]})
        newUser.to_csv('validLogins.csv', mode='a', header=False, index=False)

        successBox = QMessageBox()
        successBox.setWindowTitle("Success")
        successBox.setText("Sign Up Successful!")
        successBox.setStyleSheet(STYLESHEETSUCCESS)
        successBox.exec()
        self.loginPage = LoginPage()
        self.hide()

    
    def login(self):
        self.loginPage = LoginPage()

# run this shizzle
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())
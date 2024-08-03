from PySide6.QtCore import Qt, QTimer
from ui_final_form_gui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout, QWidget, QFileDialog, QProgressBar, QTableWidget, QTableWidgetItem
import subprocess
import pandas as pd
import os
from PyQt6.QtCore import QDateTime, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

class MyGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Recommender System")

        self.dashboard_2.clicked.connect(self.switch_to_dashboardPage)
        self.profile_2.clicked.connect(self.switch_to_profilePage)
        self.messages_2.clicked.connect(self.switch_to_messagesPage)
        self.notifications_2.clicked.connect(self.switch_to_notificationsPage)
        self.settings_2.clicked.connect(self.switch_to_settingsPage)
        self.pushButton.setVisible(False)
        self.pushButton.clicked.connect(self.run_algorithms)
        self.pushButton_2.clicked.connect(self.open_file_dialog)
        self.pushButton_3.clicked.connect(self.open_visual)
        self.label_40.setVisible(False)
        self.progressBar.setVisible(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.load_last_run_time()

        

        self.tableWidget_3.setRowCount(4373)
        load_excel_to_table('compares_results.xlsx',self.tableWidget_3)

        self.tableWidget.setRowCount(4068)
        load_excel_to_table('kmeans_customer_recommendations.xlsx',self.tableWidget)
        
        self.tableWidget_2.setRowCount(4373)
        load_excel_to_table('knn_customer_recommendations.xlsx',self.tableWidget_2)
        
        
        
        

    def switch_to_dashboardPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_profilePage(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_messagesPage(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_notificationsPage(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_settingsPage(self):
        self.stackedWidget.setCurrentIndex(4)

    def open_file_dialog(self):
        # Open file dialog and get the selected file path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Dataset", "", "All Files (*);;CSV Files (*.csv)", options=options)
        
        if file_path:
            self.label_12.setText(f'Dataset Address: {file_path}')
            # Here you can add your code to handle the dataset
            self.pushButton.setVisible(True)

    def open_visual(self):
        self.popup = PopupWindow()
        self.popup.show()

    def run_algorithms(self):
        self.start_progress()
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString('dd/MM/yyyy HH:mm')

        self.label_7.setText(f'Program last run at: {formatted_datetime}')

        self.save_last_run_time(formatted_datetime)


    def save_last_run_time(self, datetime_str):
        with open('last_run_time.txt', 'w') as file:
            file.write(datetime_str)


    def load_last_run_time(self):
        if os.path.exists('last_run_time.txt'):
            with open('last_run_time.txt', 'r') as file:
                last_run_time = file.read()
                self.label_7.setText(f'Program last run at: {last_run_time}')


    def start_progress(self):
        # Show the progress bar and reset the progress value
        self.progressBar.setVisible(True)
        self.progress_value = 0
        self.progressBar.setValue(self.progress_value)
        self.label_40.setVisible(True)
        # Start the timer to update the progress bar every 10 seconds // (10000) olmalı.
        self.timer.start(15000)

    def update_progress(self):
        # Increase the progress value by 1
        self.progress_value += 1
        self.progressBar.setValue(self.progress_value)
        # Stop the timer if the progress value reaches 100
        if self.progress_value >= 100:
            self.timer.stop()
            self.run_algorithms()


def load_excel_to_table(file_path, table_widget):
    # Read the Excel file, skipping the header row (header=0 means the first row is header)
    df = pd.read_excel(file_path, header=0)
    
    # Get the number of rows and columns
    num_rows, num_cols = df.shape
    
    # Set the number of rows and columns in the table widget
    table_widget.setRowCount(num_rows - 1)  # Skip header row
    table_widget.setColumnCount(num_cols)
    
    # Set the column headers
    table_widget.setHorizontalHeaderLabels(df.columns)
    
    # Populate the table widget with data
    for row in range(1, num_rows):  # Start from the second row
        for col in range(num_cols):
            item = QTableWidgetItem(str(df.iat[row, col]))
            table_widget.setItem(row - 1, col, item)  # Adjust row index since we're skipping the header




class PopupWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Visuals Viewer")
        self.resize(950, 800)

        # Layout for the popup window
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Add QWebEngineView to display HTML content
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

        # Path to the HTML file
        html_file_path = os.path.join(os.path.dirname(__file__), '3d_visualization.html')
        file_url = QUrl.fromLocalFile(html_file_path).toString()
        self.web_view.setUrl(file_url)
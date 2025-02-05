**Facial Recognition Attendance System**
    This project is a Facial Recognition-based Attendance System using Deep Learning. It marks attendance by recognizing faces and sends an email alert if a student does not wear an ID.

**Features**
Face recognition using face_recognition library.
Marks attendance in an Excel sheet.
Detects students without ID cards.
Sends email alerts to the Head of Department for students without an ID.
Uses OpenCV for face detection and SQLAlchemy for database integration.

**Installation**
  **Prerequisites**

    Ensure you have the following installed:
    Python 3.11
    OpenCV (cv2)
    Face Recognition (face_recognition)
    Pandas
    SQLAlchemy
    Tkinter

**Install Dependencies**
    Run the following command to install the required Python libraries:
    pip install opencv-python face-recognition pandas sqlalchemy smtplib

**Usage**

1. Train the Model  
  Place training images in the training_images folder, ensuring each image is named after the student (e.g., john_doe.jpg).

2. Run the Application
    Execute the following command:
      python main.py
      The system captures a real-time image.
      Recognizes the student.
      Records attendance in an Excel sheet.
      Sends an email alert if necessary.

**Configuration**
    Update the following parameters in main.py:
    SMTP Configuration (for email alerts)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

**Output**
    Attendance stored in an Excel file (attendance_sheet_<date>.xlsx).
    Alerts sent to students and the HOD via email.

**License**
    This project is open-source under the MIT License.


import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import os
from tkinter import Tk, Label, Entry, Button, Toplevel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a directory to save captured images
if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

# File to store user data
user_data_file = "user_data.csv"

# Load existing user data
if os.path.exists(user_data_file):
    user_data = pd.read_csv(user_data_file)
else:
    user_data = pd.DataFrame(columns=["Name", "Roll No", "Department", "College Email"])

# Admin email address
admin_email = "sivavisu71@gmail.com"

# Email configuration (update with your SMTP server details)
smtp_server = "smtp.gmail.com"  # Example: Gmail SMTP server
smtp_port = 587  # Port for TLS
sender_email = "projectmail2610@gmail.com"  # Your email address
sender_password = "jbyg szpc igft ysww"  # Your email password

# Function to send email
def send_email(to_email, subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, sender_password)  # Log in to the email account
            server.send_message(msg)  # Send the email
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to get user input using a custom dialog box
def get_user_input():
    root = Tk()
    root.withdraw()  # Hide the root window

    # Create a custom dialog box
    dialog = Toplevel(root)
    dialog.title("Input Details")
    dialog.geometry("400x300")  # Set the size of the dialog box

    # Add labels and entry fields
    Label(dialog, text="Enter your roll number:").pack(pady=10)
    roll_no_entry = Entry(dialog, width=30)
    roll_no_entry.pack(pady=10)

    Label(dialog, text="Enter your department:").pack(pady=10)
    department_entry = Entry(dialog, width=30)
    department_entry.pack(pady=10)

    Label(dialog, text="Enter your college email:").pack(pady=10)
    college_email_entry = Entry(dialog, width=30)
    college_email_entry.pack(pady=10)

    # Use a dictionary to store the input values
    user_input = {"roll_no": "", "department": "", "college_email": ""}

    # Function to collect input and close the dialog
    def collect_input():
        user_input["roll_no"] = roll_no_entry.get()
        user_input["department"] = department_entry.get()
        user_input["college_email"] = college_email_entry.get()
        dialog.destroy()

    # Add a submit button
    Button(dialog, text="Submit", command=collect_input).pack(pady=20)

    # Wait for the dialog to close
    dialog.wait_window()

    root.destroy()  # Close the root window
    return user_input["roll_no"], user_input["department"], user_input["college_email"]

# Function to mark attendance based on a specific time window
def mark_attendance(current_time):
    # Define the attendance time window (e.g., 9:00 AM to 9:30 AM)
    start_time = datetime.strptime("18:00:00", "%H:%M:%S").time()
    end_time = datetime.strptime("23:00:00", "%H:%M:%S").time()

    # Convert current_time to a time object
    current_time_obj = datetime.strptime(current_time.split()[1], "%H:%M:%S").time()

    # Check if the current time is within the attendance window
    if start_time <= current_time_obj <= end_time:
        return "Present"
    else:
        return "Absent"

# Function to train the model
def train_model(images_folder):
    known_face_encodings = []
    known_face_names = []

    # Check if the folder exists
    if not os.path.exists(images_folder):
        raise FileNotFoundError(f"The folder '{images_folder}' does not exist. Please create it and add training images.")

    # Loop through each image in the folder
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Load the image
            image_path = os.path.join(images_folder, filename)
            image = face_recognition.load_image_file(image_path)

            # Detect face encodings in the image
            face_encodings = face_recognition.face_encodings(image)

            # If no face is detected, skip the image
            if len(face_encodings) == 0:
                print(f"No face detected in {filename}. Skipping this image.")
                continue

            # Use the first face encoding (assuming one face per image)
            face_encoding = face_encodings[0]

            # Extract the name from the filename (e.g., "john.jpg" -> "john")
            name = os.path.splitext(filename)[0]

            # Add the encoding and name to the lists
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

    return known_face_encodings, known_face_names

# Function to save data to Excel
def save_to_excel(data):
    # Get the current date in the format "dd_mm_yyyy"
    current_date = datetime.now().strftime("%d_%m_%Y")
    excel_file = f"attendance_sheet_{current_date}.xlsx"

    # Check if the file already exists
    if os.path.exists(excel_file):
        # Load the existing workbook
        df = pd.read_excel(excel_file)
    else:
        # Create a new DataFrame
        df = pd.DataFrame(columns=["Date and Time", "Name", "Roll No", "Department", "College Email", "Attendance Status"])

    # Append the new data to the DataFrame
    df.loc[len(df)] = data

    # Save the DataFrame to Excel
    df.to_excel(excel_file, index=False)
    print(f"Attendance data saved to {excel_file}")

# Main Program
def main():
    # Path to the folder containing training images
    images_folder = "C:/Users/sivav/Project_code/app/training_images"

    # Train the model
    known_face_encodings, known_face_names = train_model(images_folder)

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Convert the frame from BGR to RGB (required by face_recognition)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in the frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)  # Adjust tolerance
                name = "Unknown"

                # If a match is found, use the name of the known face
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the name below the face
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # If a known face is detected, capture the photo and mark attendance
                if name != "Unknown":
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    image_name = f"captured_images/{name}_{current_time.replace(':', '-')}.jpg"
                    cv2.imwrite(image_name, frame)  # Save the captured image

                    # Mark attendance based on the current time
                    attendance_status = mark_attendance(current_time)

                    # Check if the user already exists in the user data
                    if name in user_data["Name"].values:
                        roll_no = user_data.loc[user_data["Name"] == name, "Roll No"].values[0]
                        department = user_data.loc[user_data["Name"] == name, "Department"].values[0]
                        if "College Email" in user_data.columns:
                            college_email = user_data.loc[user_data["Name"] == name, "College Email"].values[0]
                        else:
                            college_email = "N/A"
                    else:
                        # Get roll number, department, and college email for new users
                        roll_no, department, college_email = get_user_input()
                        # Add the new user to the user data
                        user_data.loc[len(user_data)] = [name, roll_no, department, college_email]
                        user_data.to_csv(user_data_file, index=False)  # Save the updated user data

                    # Save the attendance data to Excel
                    attendance_data = [current_time, name, roll_no, department, college_email, attendance_status]
                    save_to_excel(attendance_data)

                    print(f"Attendance marked for {name} at {current_time}")

                    # If attendance is marked as "Absent", send an email
                    if attendance_status == "Absent":
                        # Email to the user
                        subject = "Attendance Marked as Absent"
                        body = f"Dear {name},\n\nYour attendance for {current_time} has been marked as Absent because you're getting late for the class timing.\n\nRegards,\nAdmin"
                        send_email(college_email, subject, body)

                        # Email to the admin
                        admin_subject = f"Attendance Alert: {name} Marked as Absent"
                        admin_body = f"Dear Admin,\n\n{name} (Roll No: {roll_no}, Department: {department}) has been marked as Absent for {current_time}.\n\nRegards,\nAttendance System"
                        send_email(admin_email, admin_subject, admin_body)

                    # Stop the program immediately after marking attendance
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # Display the resulting frame
            cv2.imshow('Face Recognition', frame)

            # Break the loop if 'q' is pressed (optional, for manual termination)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the webcam and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    main()  
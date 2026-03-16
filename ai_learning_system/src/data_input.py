def input_student_data():
    """Capture student performance data."""
    try:
        marks = float(input("Enter student marks: "))
        attendance = float(input("Enter student attendance percentage: "))
        study_hours = float(input("Enter study hours per week: "))
        
        return {
            "marks": marks,
            "attendance": attendance,
            "study_hours": study_hours
        }
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return input_student_data()

def load_student_data(file_path):
    """Load student data from a file."""
    import json
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
        return None

def save_student_data(file_path, data):
    """Save student data to a file."""
    import json
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except IOError:
        print("Error writing to file.")
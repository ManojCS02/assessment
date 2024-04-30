from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

# Load student data from CSV file
def load_student_data():
    with open('student_data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        student_data = [row for row in reader]
    return student_data

# Paginate student data
def paginate(data, page, page_size):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return data[start_index:end_index]

# API endpoint to load student details with pagination
@app.route('/students', methods=['GET'])
def get_students():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    student_data = load_student_data()
    paginated_data = paginate(student_data, page, page_size)
    return jsonify(paginated_data)

# API endpoint for server-side filtering
@app.route('/filter', methods=['GET'])
def filter_students():
    name = request.args.get('name')
    total_marks = request.args.get('total_marks')
    student_data = load_student_data()
    filtered_data = student_data

    # Apply filters
    if name:
        filtered_data = [student for student in filtered_data if student['name'] == name]
    if total_marks:
        filtered_data = [student for student in filtered_data if int(student['total_marks']) >= int(total_marks)]

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)

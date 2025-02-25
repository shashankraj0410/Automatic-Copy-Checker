from flask import Flask, render_template, request, jsonify
from checkanswer import process_images
from werkzeug.utils import secure_filename
import os
from pdf2image import convert_from_path

app = Flask(__name__)

# Path to save uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}  # Specify allowed file types
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """
    Check if the file is in an allowed format.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_images(pdf_path):
    """
    Convert each page of the PDF to an image and return the list of image file paths.
    """
    images = convert_from_path(pdf_path)
    image_paths = []
    
    for i, image in enumerate(images):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{i}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    try:
        original_image = request.files.get('originalImage')
        student_image = request.files.get('studentImage')

        if not (original_image and student_image):
            return jsonify({'message': 'Both images or PDFs are required.'}), 400

        # Ensure files are allowed
        if not (allowed_file(original_image.filename) and allowed_file(student_image.filename)):
            return jsonify({'message': 'Invalid file format. Only PNG, JPG, JPEG, and PDF files are allowed.'}), 400

        # Save files
        original_filename = secure_filename(original_image.filename)
        student_filename = secure_filename(student_image.filename)

        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        student_image_path = os.path.join(app.config['UPLOAD_FOLDER'], student_filename)

        original_image.save(original_image_path)
        student_image.save(student_image_path)

        # Check if PDFs need to be converted to images
        if original_filename.lower().endswith('.pdf'):
            original_image_paths = convert_pdf_to_images(original_image_path)
        else:
            original_image_paths = [original_image_path]  # Single image file

        if student_filename.lower().endswith('.pdf'):
            student_image_paths = convert_pdf_to_images(student_image_path)
        else:
            student_image_paths = [student_image_path]  # Single image file

        # Process the first page or image of both the teacher and student submissions (extendable)
        result = process_images(original_image_paths[0], student_image_paths[0])

        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Error processing the images.'}), 500

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': f'Error occurred: {e}'}), 500

    finally:
        # Ensure clean-up of uploaded files even if an error occurs
        if os.path.exists(original_image_path):
            os.remove(original_image_path)
        if os.path.exists(student_image_path):
            os.remove(student_image_path)

if __name__ == '__main__':
    app.run(debug=True)

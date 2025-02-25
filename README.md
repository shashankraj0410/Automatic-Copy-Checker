# Automatic-Copy-Checker
The Auto Grader project automates grading by using OCR and natural language processing to compare students' work with teachers' correct answers. It processes scanned images or PDFs, computes a similarity score between the texts, and analyzes sentiment for further insights.
![image](https://github.com/user-attachments/assets/18ea3190-2de9-4a4d-a9f2-ec51ccc7e95c)
![image](https://github.com/user-attachments/assets/176411b5-b4ab-479e-8cbb-c9ed5cc0bb59)


Key Features--

OCR (Optical Character Recognition):
Uses Tesseract OCR to recognize text from uploaded images (both teacher's and student's answers). The images are preprocessed using OpenCV to enhance OCR accuracy.

Text Preprocessing:
Performs basic image enhancements such as grayscale conversion, noise reduction, and thresholding to improve OCR results.

Spell Correction:
Integrates the SpellChecker library to correct spelling mistakes in the recognized text, ensuring better comparison accuracy.

Similarity Calculation:
Calculates the Jaccard similarity between the teacher's and student's answers by comparing the unique sets of words from each text. This gives a percentage of similarity between the two submissions.

Sentiment Analysis:
Uses TextBlob to determine the polarity (positive or negative sentiment) and subjectivity (objective or subjective nature) of both the teacher's and student's text.

PDF Support:
Supports both image files and PDF uploads. If a PDF is uploaded, it converts the pages into images for further processing.

Web Interface:
Built using Flask, the web interface allows users to upload the teacher's and student's answer sheets. After submission, the results, including the recognized text, similarity percentage, and sentiment analysis, are displayed on the webpage.

Applications--

Automated Grading of Handwritten Assignments:
Teachers can use this system to automatically grade handwritten assignments by comparing student submissions with the teacher's answer sheet.

Examination Paper Checking:
The Auto Grader can be used to compare student answers to a model answer key in large-scale exams, reducing human errors and time spent on manual checks.

Sentiment Analysis of Written Content:
The sentiment analysis feature can be applied to analyze the emotional tone of student feedback, essays, or creative writing.

Transcription of Handwritten Notes:
The system can be repurposed to transcribe handwritten notes, converting them into digital text.

Digitization of Archival Documents:
Libraries or archives holding historical handwritten documents can use the system to digitize and extract text from old manuscripts or letters.

Installation
System Requirements
Operating System: Any OS that supports Python and its libraries (Linux, macOS, or Windows).

Python Version: Python 3.6 or above.

Python Libraries
Install the required Python libraries using pip:

bash
Copy
pip install -r requirements.txt
The project relies on the following libraries:

Flask==2.1.1

Pillow==9.1.0

pdf2image==1.16.0

pytesseract==0.3.8

opencv-python==4.5.5.64

spellchecker==0.4.0

scikit-learn==1.0.2

textblob==0.15.3

werkzeug==2.1.1

Additional Software
Tesseract-OCR:
Install Tesseract OCR separately, as pytesseract is just a Python wrapper.
Set the TESSDATA_PREFIX environment variable to the installation path and add the Tesseract executable (tesseract.exe) to the system's PATH.

Directory Structure
Copy
auto-grader/
├── templates/               # Contains the HTML files for the Flask app
│   └── index.html           # Upload form
├── static/                  # Static files like CSS, JS, etc.
│   └── style.css            # CSS file for frontend styling
├── uploads/                 # Directory where uploaded images are temporarily saved
├── app.py                   # Flask application code
├── recog.py                 # OCR and image processing code
├── checksmswer.py           # Main logic for comparison, sentiment analysis, etc.
├── requirements.txt         # List of required Python packages
└── README.md                # Project description and instructions
Running the Project
Clone the repository:

bash
Copy
git clone https://github.com/your-username/auto-copy-grader.git
Navigate to the project directory:

bash
Copy
cd auto-copy-grader
Install the required dependencies:

bash
Copy
pip install -r requirements.txt
Run the Flask server:

bash
Copy
python app.py
Open your browser and go to http://127.0.0.1:5000/ to access the web interface.

Benefits
Time-Saving for Teachers and Evaluators: Automates the grading process, reducing manual effort.

Consistent Grading: Provides uniformity and consistency in grading, avoiding human bias.

Immediate Feedback: Delivers near-instant feedback to students on their submissions.

Scalability: Suitable for handling large volumes of submissions without additional manpower.

Plagiarism Detection: Helps detect possible copying or plagiarism in handwritten assignments.

Limitations
Accuracy of OCR: Struggles with unclear or messy handwriting.

Dependency on Preprocessing: The quality of OCR results depends on effective preprocessing steps.

Limited to Text-Based Evaluation: Not suitable for subjects that require diagrams, graphs, or complex equations.

Spell-Checking Challenges: May introduce errors if the recognized text is inaccurate.

Limited Contextual Understanding: Cannot assess the reasoning or logic behind answers in essays or complex questions.

Future Scope
Improved OCR and Handwriting Recognition: Use advanced models to enhance handwriting recognition and support multiple languages.

Contextual Grading: Implement NLP techniques for deeper understanding of answers.

Non-text Element Grading: Expand to recognize and grade diagrams, formulas, and mathematical expressions.

Intelligent Feedback: Provide personalized feedback and suggest learning materials.

Learning Management System (LMS) Integration: Seamless integration with LMS platforms for automatic grading and result distribution.

Conclusion
The Automatic Copy Grader is a transformative tool for educators, leveraging OCR, image processing, and AI-driven text analysis to automate the grading process. With future enhancements

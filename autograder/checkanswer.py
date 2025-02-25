from recog import perform_ocr

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from sentence_transformers import SentenceTransformer, util

# Ensure necessary NLTK downloads
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """
    Preprocess text by lowercasing, removing stopwords, and lemmatizing.
    """
    try:
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        # Convert text to lowercase
        words = text.lower().split()

        # Remove stopwords and apply lemmatization
        cleaned_text = [
            lemmatizer.lemmatize(word) for word in words if word not in stop_words
        ]
        return " ".join(cleaned_text)
    except Exception as e:
        print(f"Error during text preprocessing: {e}")
        return text
    
def preprocess_text_for_similarity(text):
    """
    Lowercase, remove special characters, and strip extra whitespaces.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()

def calculate_similarity(text1, text2):
    """
    Calculate semantic similarity using Sentence Transformers.
    """
    try:
        # Pre-trained model for sentence embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Preprocess texts
        text1 = preprocess_text_for_similarity(text1)
        text2 = preprocess_text_for_similarity(text2)

        print(f"Preprocessed Text 1: {text1}")
        print(f"Preprocessed Text 2: {text2}")

        # Generate sentence embeddings
        embedding1 = model.encode(text1, convert_to_tensor=True)
        embedding2 = model.encode(text2, convert_to_tensor=True)

        # Compute cosine similarity between the embeddings
        similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
        print(f"Similarity Score: {similarity}")

        # Return similarity percentage
        return similarity * 100

    except Exception as e:
        print(f"Error during similarity calculation: {e}")
        return 0

def analyze_sentiment(text):
    """
    Analyze sentiment using the VADER sentiment analyzer.
    Returns a dictionary with polarity (compound score) and subjectivity.
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(text)
        polarity = sentiment['compound']  # Compound score: overall sentiment
        # Since VADER doesn't provide subjectivity, set it to a placeholder or calculate separately
        subjectivity = 0.5  # Placeholder value
        return polarity, subjectivity
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return 0, 0  # Return default values

def process_images(original_image_path, student_image_path):
    """
    Perform OCR on both images, correct the recognized text, calculate the similarity
    percentage between them, and return the results.
    """
    try:
        print("Performing OCR on the teacher's image...")
        teacher_text = perform_ocr(original_image_path)

        print("Performing OCR on the student's image...")
        student_text = perform_ocr(student_image_path)

        if not teacher_text or not student_text:
            print("OCR failed or no text was extracted from one or both images.")
            return None

        # Calculate similarity percentage
        similarity_percentage = calculate_similarity(teacher_text, student_text)

        # Perform sentiment analysis on both texts
        teacher_polarity, teacher_subjectivity = analyze_sentiment(teacher_text)
        student_polarity, student_subjectivity = analyze_sentiment(student_text)

        return {
            'teacher_text': teacher_text,
            'student_text': student_text,
            'similarity_percentage': similarity_percentage,
            'teacher_sentiment': {
                'polarity': teacher_polarity,
                'subjectivity': teacher_subjectivity,
            },
            'student_sentiment': {
                'polarity': student_polarity,
                'subjectivity': student_subjectivity,
            },
        }

    except Exception as e:
        print(f"Error processing images: {e}")
        return None

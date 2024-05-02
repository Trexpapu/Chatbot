import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import re
from spellchecker import SpellChecker

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')

# Function to load knowledge from the text file
def load_knowledge(file):
    knowledge = {}
    with open(file, 'r', encoding='utf-8') as file:
        for line in file:
            question, answer = line.strip().split('|')
            knowledge[question] = answer
    return knowledge

# Function to preprocess user's question
def preprocess_question(question):
    # Convert the question to lowercase
    question = question.lower()
    
    # Correct spelling errors
    spell = SpellChecker(language='es')
    corrected_question = []
    for word in question.split():
        corrected_word = spell.correction(word)
        if corrected_word is not None:
            corrected_question.append(corrected_word)
        else:
            corrected_question.append(word)  # Use the original word if it cannot be corrected
    
    question = " ".join(corrected_question)
    clean_question = ''.join((c for c in unicodedata.normalize('NFD', question) if unicodedata.category(c) != 'Mn'))
    
    # Tokenize the question
    tokens = word_tokenize(clean_question, language='spanish')  # Using Spanish tokenizer
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words("spanish"))
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
    
    # Lemmatize the tokens
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in nltk.pos_tag(tokens)]
    
    return " ".join(tokens)




# Function to get the part of speech for lemmatization
def get_wordnet_pos(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun if not recognized

# Function to find the best response
def find_best_response(question, knowledge):
    knowledge_questions = list(knowledge.keys())
    knowledge_answers = list(knowledge.values())
    # Combine questions and answers
    texts = knowledge_questions + knowledge_answers
    # Calculate TF-IDF matrix for questions and answers
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    # Calculate cosine similarity between user's question and known questions and answers
    question_similarity = cosine_similarity(vectorizer.transform([question]), tfidf_matrix[:-len(knowledge_answers)])
    answer_similarity = cosine_similarity(vectorizer.transform([question]), tfidf_matrix[-len(knowledge_answers):])
    # Get the index of the most similar question or answer
    max_similarity_question_index = question_similarity.argmax()
    max_similarity_answer_index = answer_similarity.argmax()
    if max(question_similarity[0]) > max(answer_similarity[0]):
        if question_similarity[0][max_similarity_question_index] > 0:
            # The most similar question has a similarity greater than zero
            return knowledge_answers[max_similarity_question_index]
        else:
            # No similar question found
            return "Lo siento, no conozco la respuesta a esa pregunta."
    else:
        if answer_similarity[0][max_similarity_answer_index] > 0:
            # The most similar answer has a similarity greater than zero
            return knowledge_answers[max_similarity_answer_index]
        else:
            # No similar answer found
            return "Lo siento, no conozco la respuesta a esa pregunta."


# Function to process information from the knowledge dictionary
def process_information(dictionary):
    processed_dictionary = {}
    for question, answer in dictionary.items():
        # Remove accents
        question_without_accents = ''.join((c for c in unicodedata.normalize('NFD', question) if unicodedata.category(c) != 'Mn'))
        answer_without_accents = ''.join((c for c in unicodedata.normalize('NFD', answer) if unicodedata.category(c) != 'Mn'))
        # Remove unwanted characters (including punctuation)
        clean_question = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]', '', question_without_accents.replace("´", ""))
        clean_answer = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ]', '', answer_without_accents.replace("´", ""))
        # Tokenize words
        question_words = word_tokenize(clean_question)
        answer_words = word_tokenize(clean_answer)
        # Convert words to lowercase
        lowercase_question_words = [word.lower() for word in question_words]
        lowercase_answer_words = [word.lower() for word in answer_words]
        # Join words into a single text
        processed_question = ' '.join(lowercase_question_words)
        processed_answer = ' '.join(lowercase_answer_words)
        # Add to the processed dictionary
        processed_dictionary[processed_question] = processed_answer
    return processed_dictionary

# Main function of the chatbot
def chatbot(user_input):
    knowledge_file = "Chat/information.txt"
    knowledge = load_knowledge(knowledge_file)
    processed_knowledge = process_information(knowledge)
    processed_user_input = preprocess_question(user_input)
    response = find_best_response(processed_user_input, processed_knowledge)
    return response


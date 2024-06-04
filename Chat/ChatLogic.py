import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from .models import Question
import unicodedata



# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')



# Function to load knowledge from the database
def load_knowledge():
    try:
        knowledge = {}
        questions = Question.objects.select_related('answerID').all()
        for question in questions:
            knowledge[question.question] = question.answerID.answer
        return knowledge
    except Exception as e:
        print("Error: ", e)



# Function to preprocess user's question
def process_questions(question):
    try:
        # Convert the question to lowercase
        question = question.lower()

        # Remove accents
        question = unicodedata.normalize('NFKD', question)
        question = ''.join([char for char in question if not unicodedata.combining(char)])
        
        # Remove special characters (including question marks)
        clean_question = re.sub(r'[^\w\s]', '', question)
        
        # Tokenize the question
        tokens = word_tokenize(clean_question, language='spanish')  # Using Spanish tokenizer
        

        
        
        # Remove stopwords and punctuation
        stop_words = set(stopwords.words("spanish"))
        clean_tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
        
        # Lemmatize the tokens
        lemmatizer = nltk.WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in nltk.pos_tag(clean_tokens)]
        print(lemmatized_tokens)
        
        return " ".join(lemmatized_tokens)
    except Exception as e:
        print("Error: ", e)





# Function to get the part of speech for lemmatization
def get_wordnet_pos(tag):
    try:
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
    except Exception as e:
        print("Error: ", e)

def find_IDQuestion_Response(ID):
    try:
        # Obtener la pregunta usando el ID
        question = Question.objects.get(questionID=ID)
        # Obtener la respuesta asociada
        response = question.answerID.answer
        return response
    except Exception as e:
        print("Error", e)
        return "Lo siento no se encontró respuesta"


# Function to find the best response
def find_best_response(question, knowledge):
    try:
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
                print(max_similarity_question_index+1)
                #return knowledge_answers[max_similarity_question_index]
                return find_IDQuestion_Response(max_similarity_question_index+1)
            else:
                # No similar question found
                return "Lo siento, no conozco la respuesta a esa pregunta."
        else:
            if answer_similarity[0][max_similarity_answer_index] > 0:
                # The most similar answer has a similarity greater than zero
                print(max_similarity_answer_index+1)
                #return knowledge_answers[max_similarity_answer_index]
                return find_IDQuestion_Response(max_similarity_answer_index+1)
            else:
                # No similar answer found
                return "Lo siento, no conozco la respuesta a esa pregunta."
    except Exception as e:
        print("Error: ", e)
        

# Function to process information from the knowledge dictionary
def process_knowledge(dictionary):
    try:
        processed_dictionary = {}
        for question, answer in dictionary.items():
            print(answer)
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
    
    except Exception as e:
        print("Error: ", e)




# Main function of the chatbot
def chatbot(user_input):
    try:
        knowledge = load_knowledge()
        processed_knowledge = process_knowledge(knowledge)
        processed_user_input = process_questions(user_input)
        response = find_best_response(processed_user_input, processed_knowledge)
        return response
    except Exception as e:
        print("Error: ", e)


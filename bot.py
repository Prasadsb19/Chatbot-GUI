# Meet KKWBOT: your friend

import nltk
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import random
import string  # to process standard python strings

f = open('chatbot1.txt', 'r', errors='ignore')
m = open('chatbot2.txt', 'r', errors='ignore')
checkpoint = "./chatbot_weights.ckpt"

raw = f.read()
rawone = m.read()
raw = raw.lower()  # converts to lowercase
rawone = rawone.lower()  # converts to lowercase
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words
sent_tokensone = nltk.sent_tokenize(rawone)  # converts to list of sentences
word_tokensone = nltk.word_tokenize(rawone)  # converts to list of words

sent_tokens[:2]
sent_tokensone[:2]

word_tokens[:5]
word_tokensone[:5]

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


Introduce_Ans = ["My name is KKWBOT.", "My name is KKWBOT you can called me Bro.", "Im KKWBOT :) ",
                 "My name is KKWBOT. and my nickname is Bro and i am happy to solve your queries :) "]
GREETING_INPUTS = ("hello", "hi", "hiii", "hii", "hiiii", "hiiii", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "hii there", "hi there", "hello", "I am glad! You are talking to me"]
Basic_Q = ("Tell me about KKWagh?", "Tell me about KKWagh", "tell me about kkwagh?", "Tell me about KKWagh","tell me about kkwagh")
Basic_Ans = [("The institute was established in the year 1984 at Bhausahebnagar (Tal. Niphad, Dist. Nashik) and shifted to Nashik City in September 1986. A land of 8.2 hectares was generously donated by Shri. Kakusheth Udesi of Hirabai Haridas Charitable Trust, Mumbai. The Society started building infrastructure at this campus (known as Hirabai Haridas Vidya Nagari) in the year 1987. As on date it is fully developed and provides accommodation for College building, office, classrooms, drawing halls, laboratories, workshops etc. English keywords frequently where as other languages use punctuation, and it has fewer syntactical constructions than other languages.")]
Basic_Om = ("Tell me about Medical Facility?", "Tell me about Medical Facility.", "tell me about medical facility? ", "tell me about medical facility", "Tell me about medical facility")
Basic_AnsM = [("Medical facility is available to all the students and faculty within the campus. Institute has a tie-up with Apollo hospital, Sushrut Hospital and NDMVP Medical College. In case of emergency, the institute ambulance is used to transfer the sick person to the hospital. The institute has Doctor-on-call system and 24*7 availability of ambulance to handle emergencies.  Doctor is also appointed for Boys and Girls hostel.")]

# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Checking for Basic_Q
def basic(sentence):
    for word in Basic_Q:
        if sentence.lower() == word:
            return Basic_Ans


# Checking for Basic_QM
def basicM(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in Basic_Om:
        if sentence.lower() == word:
            return random.choice(Basic_AnsM)


# Checking for Introduce
def IntroduceMe(sentence):
    return random.choice(Introduce_Ans)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


# Generating response
def responseone(user_response):
    robo_response = ''
    sent_tokensone.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokensone)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokensone[idx]
        return robo_response


def chat(user_response):
    user_response = user_response.lower()
    keyword = " module "
    keywordone = " module"
    keywordsecond = "module "

    if (user_response != 'bye'):
        if (user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("ROBO: You are welcome..")
            return "You are welcome.."
        elif (basicM(user_response) != None):
            return basicM(user_response)
        else:
            if (user_response.find(keyword) != -1 or user_response.find(keywordone) != -1 or user_response.find(
                    keywordsecond) != -1):
                print("ROBO: ",end="")
                print(responseone(user_response))
                return responseone(user_response)
                sent_tokensone.remove(user_response)
            elif (greeting(user_response) != None):
                print("ROBO: "+greeting(user_response))
                return greeting(user_response)
            elif (user_response.find("your name") != -1 or user_response.find(" your name") != -1 or user_response.find(
                    "your name ") != -1 or user_response.find(" your name ") != -1):
                return IntroduceMe(user_response)
            elif (basic(user_response) != None):
                return basic(user_response)
            else:
                print("ROBO: ",end="")
                print(response(user_response))
                return response(user_response)
                sent_tokens.remove(user_response)

    else:
        flag = False
        print("ROBO: Bye! take care..")
        return "Bye! take care.."



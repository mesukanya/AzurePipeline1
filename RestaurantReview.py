#import Libararies
import numpy as np
import re
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

#Read train file
data = pd.read_csv("train.csv",encoding="ISO-8859-1")
#print(data)

#x = data.iloc[:,2].values
#y = data.iloc[:,[0,1]].values
#print(x_train)
#print(y_train)

#sentence = []

#for i in range(len(data)):
    #sentence.append((data['SentimentText'][i]))

#print(sentence)

corpus = []
for i in range(0, len(data)):
   sentiment = re.sub('[^a-zA-Z]', ' ', data['SentimentText'][i])
   review = sentiment.split()
   review = word_tokenize(sentiment)
   print(review)
   ps = PorterStemmer()
   [ps.stem(word) for word in review
    if not word in set(stopwords.words('english'))]
   review = ' '.join(review)
   print(review)
   corpus.append(review)
   cv = CountVectorizer(max_features=1500)
   x_train = cv.fit_transform(corpus).toarray()
   y_train = data.iloc[:, [0, 1]].values
   #print(x_train)
   #print(y_train)
   model = RandomForestClassifier(n_estimators=10, criterion='entropy')
   model.fit(x_train, y_train)

#print(x_train)
#print(y_train)

#from sklearn.preprocessing import StandardScaler


#sc = StandardScaler()
#X_train = sc.fit_transform(x_train.reshape(-1, 1))


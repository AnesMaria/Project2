import sys
import nltk
nltk.download(['punkt', 'wordnet','averaged_perceptron_tagger'])

# import libraries
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from operator import itemgetter
import joblib
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.neighbors import KNeighborsClassifier

def load_data(database_filepath):
  '''
    Function : loading data from SQL database
    Parameters : 
    Input: DAtabase 
    Output: Dataframe
    '''
    #load data from database
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('Clean_Disaster_Data', engine)  

    #define X,Y and category_names
    X = df.message
    Y = df[df.columns[4:]]
    category_names = Y.columns
        return X,Y,category_names


def tokenize(text):
   '''
    Function : Tokenizer text from my dataframe
    Parameters : 
    Input: text
    Output: tokens
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
   '''
    Defining my pipeline : 
         - Train pipeline : Vectorizer, Transformer, MultiOutputClassifier
         - Tuning the model to optimize the different hyper parameters
    Input: train_X, Train_Y
    Output: model classifier
    '''
    pipeline =  Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
        )
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=0)

        # train classifier
        pipeline.fit(X_train,y_train)

    # Perform grid search using the pipeline
    model = GridSearchCV(pipeline, param_grid=parameters, cv=3, n_jobs=-1)

    return model

def evaluate_model(model, X_test, Y_test, category_names):
   '''
    Function : model evaluation by  accuracy, precision and recall.
        - Input: model and data.
        - Output: mesures 
    '''
    #Predictions
    Y_pred = model.predict(X_test)

    #Model evaluation
    model_eval = pd.DataFrame(columns=['target_category','accuracy','precision','recall'])

    for col in range(0,len(category_names)):
    
        report = classification_report(Y_test.values[col], Y_pred[col],output_dict=True,zero_division=0.0)
        result_dict = {"target_category":category_names[col],
                    "accuracy":report['accuracy'], 
                    "precision": report['macro avg']['precision'],
                    "recall": report['macro avg']['recall']
                    }
        result = pd.DataFrame([result_dict])
        print(result)
        model_eval = model_eval.append(result)

    print('......\n'
          'Model Quality:\n '
          'Model Accuracy: ',model_eval['accuracy'].mean(),'(+/- ', model_eval['accuracy'].std(),')\n ' 
          'Model Precision: ',model_eval['precision'].mean(),'(+/- ', model_eval['precision'].std(),')\n ' 
          'Model Recall: ',model_eval['recall'].mean(),'(+/- ', model_eval['recall'].std(),')' )

    return model_eval


def save_model(model, model_filepath):
    '''
    Exports model as a pickle file
    '''
  model = 'my_model_classifier'
  model_filepath = 'model.joblib'

# Sauvegarder le modèle sur le disque
joblib.dump(model, model_filepath)



def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
# Project2
The project is organized into three fundamental components.

          1. ETL Pipeline:
In this part of Python script titled process_data.py, a data cleansing workflow is performed that:
          - Loading both messages and categories datasets.
          - Merging the datasets.
          - Cleaning up the data.
          - Storing the cleaned data in a SQLite database.

            2. ML Pipeline:
Utilizing a Python script named train_classifier.py, a machine learning workflow is carried out that:
          - Fetches data from the SQLite database.
          - Segregates the dataset into training and test subsets.
          - Constructs a pipeline for text processing and machine learning.
          - Employs GridSearchCV for training and tuning the model.
          - Evaluates the model on the test set and outputs the results.
          - Exports the refined model as a pickle file for further use.


        3. Flask Web App:
A pre-structured Flask web application is developped, which can be activated by using the run.py script. 

        4. GitHub Repository Link: https://github.com/AnesMaria/Project2

        5. Runing the code 

 Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
    
                  `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/InsertDatabaseName.db`
        
    - To run ML pipeline that trains classifier and saves
    
                  `python models/train_classifier.py data/InsertDatabaseName.db models/classifier.pkl`
        
Go to `app` directory: `cd app`

                    Run the web app: `python run.py`cd



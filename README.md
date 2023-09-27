# Project2
The project is organized into three fundamental components.

ETL Pipeline:
In a dedicated Python script named process_data.py, a data cleansing workflow is performed that:

Loads both messages and categories datasets.
Merges the datasets.
Cleans up the data.
Stores the clean data in a SQLite database.
ML Pipeline:
Utilizing a Python script named train_classifier.py, a machine learning workflow is carried out that:

Fetches data from the SQLite database.
Segregates the dataset into training and test subsets.
Constructs a pipeline for text processing and machine learning.
Employs GridSearchCV for training and tuning the model.
Evaluates the model on the test set and outputs the results.
Exports the refined model as a pickle file for further use.
Flask Web App:
A pre-structured Flask web application is included, which can be launched using the run.py script. This application comes with a text input field for a message to be classified, displays the classification results, and renders visual analytics of the training data.

GitHub Repository Link:
https://github.com/nadinepuetzer/disaster-response-pipeline-project

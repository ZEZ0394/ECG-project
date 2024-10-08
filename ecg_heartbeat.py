# -*- coding: utf-8 -*-
"""ECG Heartbeat

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rTAiMlMFScfwtAzr0YZtfNNgzBelRXsy

# Import datasets from kaggle
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.
import streamlit as st
import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'heartbeat:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F29414%2F37484%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240710%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240710T132355Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D81168ce85a04274c60e8d7fb426b08063ecc86883f3f03cb87e931ff361b3c9c278afe537a190cc0d759c9f70009016cf57c99398a553e53611cd5c014b27665ed7d5995ea238eaffa3451ca13dc59456abb78ef470008fb72ed36c8352497adc0065fe3e3909287f192c00a8b6d453c2ad2e2a2dafb286cf79307dc279221694fd315306c963379fee64c86eeca945877886b7eac7bdbcafb43a230f10e0053068ad6627e02855ca0e1054f905ade602d65d9402f08b239d2e8ce2a07344b556540bd331819a68e7be3cb0f6fee292ffc0dd73606438b0f6acc1fab6c6c9383de326b4ad65414c2a6ec7d06366677068336580ac481a1c51bcefd1209d2c52c'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

os.system('umount /kaggle/input/') 
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

"""# Basic libraries"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

train_df=pd.read_csv('/kaggle/input/heartbeat/mitbih_train.csv',header=None)
test_df=pd.read_csv('/kaggle/input/heartbeat/mitbih_test.csv',header=None)

"""# EDA"""

train_df.head()

train_df.shape, test_df.shape

train_df.describe()

print(train_df.isnull().sum())
print(test_df.isnull().sum())

"""Some notes:
- we can not remove any columns even they are contain many zeros because the dataset is about heartbeat signals
- there is no need for scalling the data, since it is already scaled from zero to one
"""

train_df[187].astype(int).value_counts()

train_df[187].unique()

# change classes label to string labels
class_mapping = {
    0: "Normal beats",
    1: "Supraventrical ectopic beats",
    2: "Ventricular ectopic beats",
    3: "Fusion beats",
    4: "Unknown beats"
}
train_df[187] = train_df[187].map(class_mapping)
test_df[187] = test_df[187].map(class_mapping)

train_df[187].value_counts()

train_df.head()

train_df[187].value_counts().plot(kind = 'bar', rot = 75)
plt.show()
train_df[187].value_counts().plot(kind = 'pie', ylabel = "")
plt.show()

unique_classes = train_df[187].unique()

# Loop over each class and plot the data for the first sample in that class
for class_label in unique_classes:
    class_data = train_df[train_df[187] == class_label].head(1)
    feature_values = class_data.iloc[:, 0:187].values[0]
    feature_indices = np.arange(0, 187)

    plt.figure(figsize=(10, 4))
    plt.plot(feature_indices, feature_values)
    plt.title(class_label)
    plt.show()

"""# Handle imbalanced data"""

from imblearn.over_sampling import SMOTE

X_train = train_df.iloc[:, :-1]
y_train = train_df.iloc[:, -1]
X_test = test_df.iloc[:, :-1]
y_test = test_df.iloc[:, -1]

smote = SMOTE()
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
X_test_resampled, y_test_resampled = smote.fit_resample(X_test, y_test)

y_train_resampled.value_counts(), y_test_resampled.value_counts()

y_train_resampled.value_counts().plot(kind = 'pie', ylabel = "")
plt.show()

"""# Modeling"""

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Logistic Regression
lr = LogisticRegression()
lr.fit(X_train_resampled, y_train_resampled)
print('Logistic Regression Classification Report:')
print(classification_report(y_test_resampled, lr.predict(X_test_resampled)))

# Random Forest
rf = RandomForestClassifier()
rf.fit(X_train_resampled, y_train_resampled)
print('Random Forest Classification Report:')
print(classification_report(y_test_resampled, rf.predict(X_test_resampled)))

print("LR accuracy:", accuracy_score(y_test_resampled, lr.predict(X_test_resampled)))
print("RF accuracy:", accuracy_score(y_test_resampled, rf.predict(X_test_resampled)))

# Predict on a sample from test data
sample_to_pred = X_test_resampled.iloc[20215].values.reshape(1, -1)
pred = rf.predict(sample_to_pred)
print(f"correct prediction✅: {pred[0]}" if y_test_resampled[20215] == pred[0] else "not correct❌")


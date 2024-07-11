import pandas as pd
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import numpy as np

# Reading the training dataset
df = pd.read_csv("training.csv")

# List of symptoms (features) and diseases (labels)
symptoms = list(df.columns[:-1])
disease = df['prognosis'].unique()

# Create a dictionary for mapping disease names to numerical values
disease_dict = {disease[i]: i for i in range(len(disease))}

# Replacing disease names with numerical values in the training dataset
df.replace({'prognosis': disease_dict}, inplace=True)

# Plotting function definitions
def plotPerColumnDistribution(df1, nGraphShown, nGraphPerRow):
    nunique = df1.nunique()
    df1 = df1[[col for col in df1 if nunique[col] > 1 and nunique[col] < 50]]  # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df1.shape
    columnNames = list(df1)
    
    nGraphRow = (nCol + nGraphPerRow - 1) // nGraphPerRow
    plt.figure(num=None, figsize=(6 * nGraphPerRow, 8 * nGraphRow), dpi=80, facecolor='w', edgecolor='k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df1.iloc[:, i]
        if not np.issubdtype(type(columnDf.iloc[0]), np.number):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation=90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.show()

def plotScatterMatrix(df1, plotSize, textSize):
    df1 = df1.select_dtypes(include=[np.number])  # keep only numerical columns
    df1 = df1[[col for col in df1 if df1[col].nunique() > 1]]  # keep columns where there are more than 1 unique values
    columnNames = list(df1)
    if len(columnNames) > 10:  # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df1 = df1[columnNames]
    ax = pd.plotting.scatter_matrix(df1, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df1.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k=1)):
        ax[i, j].annotate(f'Corr. coef = {corrs[i, j]:.3f}', (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

# Plotting the distributions and scatter matrix for the training data
plotPerColumnDistribution(df, 10, 11)
plotScatterMatrix(df, 20, 10)

# Splitting features and labels
X = df[symptoms]
y = df["prognosis"]

# Reading the testing dataset
tr = pd.read_csv("testing.csv")

# Replacing disease names with numerical values in the testing dataset
tr.replace({'prognosis': disease_dict}, inplace=True)

# Plotting the distributions for the testing data
plotPerColumnDistribution(tr, 10, 5)

# Splitting features and labels
X_test = tr[symptoms]
y_test = tr["prognosis"]

# Drop rows with NaN values in y_test
y_test = y_test.dropna()

# Input symptoms
Symptom1 = input("Enter symptom 1: ")
Symptom2 = input("Enter symptom 2: ")
Symptom3 = input("Enter symptom 3: ")
Symptom4 = input("Enter symptom 4: ")
Symptom5 = input("Enter symptom 5: ")
psymptoms = [Symptom1, Symptom2, Symptom3, Symptom4, Symptom5]

# Convert input symptoms to the model input format
input_vector = [0] * len(symptoms)
for symptom in psymptoms:
    if symptom in symptoms:
        input_vector[symptoms.index(symptom)] = 1
print(input_vector)

def DecisionTree(y_test):
    
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
        
        y_pred = clf.predict(X_test)
        print(y_pred)
        # Convert y_test to numerical labels if it's not already in numerical format
        if not np.issubdtype(y_test.dtype, np.number):
            y_test = y_test.map(disease_dict)
        
        # print("Decision Tree")
        # print("Accuracy:", accuracy_score(y_test, y_pred))
        # print("Confusion matrix:")
        # print(confusion_matrix(y_test, y_pred))

        inputtest = [input_vector]
        predict = clf.predict(inputtest)
        predicted = predict[0]

        print("Predicted Disease:", list(disease_dict.keys())[list(disease_dict.values()).index(predicted)])
y_test = y_test.dropna()
DecisionTree(y_test)

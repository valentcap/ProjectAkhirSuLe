import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
%matplotlib inline

doc = "winequality-red.csv"
dataset = pd.read_csv(doc, sep=';', header=0)
print(dataset)

# Memperlihatkan 5 data teratas
dataset.head()


dataset.info()

# Grafik pengaruh variabel terhadap kualitas

#fixed acidity
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'fixed acidity', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'volatile acidity', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'citric acid', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'residual sugar', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'chlorides', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'free sulfur dioxide', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'total sulfur dioxide', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'sulphates', data = dataset)

fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'alcohol', data = dataset)

# Binary Classification
# Wine dengan quality diatas 6.5 dianggap sebagai good(1) dan dibawahnya bad(0)
bins = (2, 6.5, 8)
group_names = ['bad', 'good']
dataset['quality'] = pd.cut(dataset['quality'], bins=bins, labels=group_names)

label_quality = LabelEncoder()

dataset['quality'] = label_quality.fit_transform(dataset['quality'])


sns.countplot(dataset['quality'])

X = dataset.drop('quality', axis=1)
y = dataset['quality']

dataset['quality'].value_counts()

# Training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

# SVC
svc = SVC(gamma='auto')
svc.fit(X_train, y_train)
pred_svc = svc.predict(X_test)

print(classification_report(y_test, pred_svc))


#Metrics otomatis
#accuracy
accuracy = accuracy_score(y_test, pred_svc)
print("accuracy = ",accuracy)

#precision
precision = precision_score(y_test, pred_svc)
print("precision = ",precision)


#Metrics manual
print("Confustion Matrix")
print(confusion_matrix(y_test, pred_svc))

#accuracy
accuracy_manual = (268+12) / (268+12+5+35)
print("accuracy = ", accuracy_manual)

#precision
precision_manual = 12 / (12+5)
print("precision = ", precision_manual)


#Evaluasi dan Perbaikan menggunakan GridSearchCV
param = {
    'C': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4],
    'kernel':['linear', 'rbf'],
    'gamma' :[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4]
}
grid_svc = GridSearchCV(svc, param_grid=param, scoring='accuracy', n_jobs=-1)

grid_svc.fit(X_train, y_train)
#Mengambil parameter terbaik
print(grid_svc.best_params_)

#Lakukan ulang dengan parameter terbaik dari hasil GridSearch
# SVC optimized
svc2 = SVC(gamma=1.1, C=1.1, kernel='rbf')
svc2.fit(X_train, y_train)
pred_svc2 = svc2.predict(X_test)

print(classification_report(y_test, pred_svc2))

#Metrics otomatis setelah optimasi
#accuracy
accuracy2 = accuracy_score(y_test, pred_svc2)
print("accuracy = ",accuracy2)

#precision
precision2 = precision_score(y_test, pred_svc2)
print("precision = ",precision2)

from ucimlrepo import fetch_ucirepo 
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay
from sklearn.svm import SVC
learning_rate = 0.1
breast_cancer_wisconsin_original = fetch_ucirepo(id=15) 

# breast_cancer_wisconsin_original = breast_cancer_wisconsin_original.data.fillna(0)

# print(breast_cancer_wisconsin_original.metadata)
# print(type(breast_cancer_wisconsin_original.data))

x = breast_cancer_wisconsin_original.data.features
y = breast_cancer_wisconsin_original.data.targets
joined_data = pd.concat([x,y],axis=1)
cleaned_data = joined_data.dropna()
data = cleaned_data.reindex(np.random.permutation(cleaned_data.index))

y_raw = data['Class']

x_raw = data[data.columns.drop("Class")].copy()


min_val = x_raw.min()
max_val = x_raw.max()
x_normal = ((x_raw - min_val) / (max_val - min_val)).copy()

X_train, x_test, y_train, y_test = train_test_split(x_normal, y_raw, test_size=0.33, random_state=42)

y_train = np.where(y_train == 2, 0, 1)

y_test = np.where(y_test == 2, 0, 1)



model = Sequential([ 
    
    Dense(258, activation='sigmoid'),   
    
    Dense(128, activation='sigmoid'),  
    
    Dense(64, activation='sigmoid'),  

    Dense(1, activation='sigmoid'),   
]) 

# optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
# model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, clipvalue=1.0)  # Clip gradients to the range [-1.0, 1.0]
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=50,  
          batch_size=32, validation_data=(x_test, y_test))

y_pred = model.predict(x_test)

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

train_loss = history.history['loss']
test_loss = history.history['val_loss']

accuracy = accuracy_score(y_test, y_pred.round())

false_positive, true_positive, _ = roc_curve(y_test, y_pred)

conf_matrix = confusion_matrix(y_test, y_pred.round())

# results = model.evaluate(x_test,  y_test, verbose = 0) 
print('confusion_matrix', conf_matrix)
# print('test loss, test acc:', test_loss, test_accuracy)

plt.plot(train_loss, label='Loss no treinamento')
plt.plot(test_loss, label='Loss no teste')
plt.legend()
plt.title('Loss no treinamento e teste')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()
plt.savefig(f'loss{learning_rate}.png')
plt.clf()
plt.cla()

# Acurácia, Curva ROC e Matriz de Confusão
print(f'Acertos: {round(accuracy*100, 2)}')
plt.plot(false_positive, true_positive)
plt.title('Curva ROC')
plt.xlabel('Falso Positivo')
plt.ylabel('Verdadeiro positivo')
plt.savefig(f'roc{learning_rate}.png')

plt.clf()
plt.cla()
print(conf_matrix)
clf = SVC(random_state=0)
clf.fit(X_train, y_train)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix,
                               display_labels=clf.classes_)
disp.plot()
plt.savefig(f'confusion{learning_rate}.png')

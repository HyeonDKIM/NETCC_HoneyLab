from keras.models import Sequential, load_model
from keras.layers import Dropout, Activation, Dense
from keras.layers import Flatten, Convolution2D, MaxPooling2D
from keras.callbacks import EarlyStopping
from keras.metrics import categorical_accuracy
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
from mlxtend.plotting import plot_confusion_matrix
import json

import matplotlib.pyplot as plt
import numpy as np

X_train, X_test, Y_train, Y_test = np.load('//home//dnslab2//yolo//Weights//version_without_Canker.npy', allow_pickle=True)
categories = ["healthy", "leafminer","leafmold","leafspot","yellowleafcurl"]
early_stopping = EarlyStopping(monitor='loss', patience=10, verbose=1)

num_classes = len(categories)
model = Sequential()
model.add(Convolution2D(16, 3, 3, border_mode='same', activation='relu', input_shape=X_train.shape[1:]))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(32, 3, 3, border_mode='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes,activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=100, nb_epoch=500, callbacks=[early_stopping])

test_predictions = model.predict(X_test)
test_predictions = np.round(test_predictions)
accuracy = accuracy_score(Y_test, test_predictions)
confmat = confusion_matrix(Y_test.argmax(axis=1), test_predictions.argmax(axis=1)) #argmax 미사용시 에러
model.summary()

fig, ax = plot_confusion_matrix(conf_mat=confmat,
                                figsize=(10,10),
                                colorbar=True,
                                class_names=categories)
plt.show()

print(confmat)
print(classification_report(Y_test.argmax(axis=1), test_predictions.argmax(axis=1), target_names=["healthy", "leafminer","leafmold","leafspot","yellowleafcurl"]))

for i in range(len(categories)):
    axis_sum = 0
    for j in range(len(categories)):
        axis_sum = axis_sum + confmat[i, j]
    answer = confmat[i, i]/axis_sum
    print(categories[i]+" accuracy : ", end='')
    print(answer)

print()
print("Overall Accuracy: "+str(accuracy))

model_json = model.to_json()
with open("//home//dnslab2//yolo//Weights//version_without_Canker.json", "w") as json_file :
    json.dump(model_json, json_file)
model.save_weights("//home//dnslab2//yolo//Weights//version_without_Canker.h5")
print("saved model to disk")

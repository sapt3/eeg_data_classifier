import pickle
import numpy as np

from sklearn.metrics import accuracy_score

from keras.models import load_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers.merge import concatenate


def save_history(history,file):
    f = open(file, 'wb')
    pickle.dump(history, f)


# load models from file

def load_all_models():
        all_models = list()
        model = load_model('cnn_lstm_model.h5')
        all_models.append(model)
        model = load_model('lstm_stacked_ensemble.h5')
        all_models.append(model)
        return all_models

# define stacked model from multiple member input models
def define_stacked_model(members):
        # update all layers in all models to not be trainable
        for i in range(len(members)):
                model = members[i]
                for layer in model.layers:
                        # make not trainable
                        layer.trainable = False
                        # rename to avoid 'unique layer name' issue
                        layer.name = 'ensemble_' + str(i+1) + '_' + layer.name
        # define multi-headed input
        ensemble_visible = [model.input for model in members]
        # concatenate merge output from each model
        ensemble_outputs = [model.output for model in members]
        merge = concatenate(ensemble_outputs)
        hidden = Dense(8, activation='relu')(merge)
        output = Dense(4, activation='softmax')(hidden)
        model = Model(inputs=ensemble_visible, outputs=output)
        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model


# fit a stacked model

def fit_stacked_model(model, inputX, inputy):
        # prepare input data
        X = [inputX for _ in range(len(model.input))]
        history = model.fit(X, inputy, batch_size=32, epochs=10, validation_split=0.2, verbose=2)
        model.save('stacked_ensemble_model1.h5')
        save_history(history.history, 'history_stacked_ensemble_model1')


# make a prediction with a stacked model

def predict_stacked_model(model, inputX):
        # prepare input data
        X = [inputX for _ in range(len(model.input))]
        return model.predict(X, verbose=2)


f1 = open('Normalized', 'rb')
example_dict = pickle.load(f1)
f1.close()

x = example_dict

f2 = open('Y_Train', 'rb')
example_dict1 = pickle.load(f2)
f2.close()

y = example_dict1
y1 = np.argmax(y, axis=1)

print(x.shape)
print(y.shape)

x = x[:17000, :, :]
y = y[:17000, ]

y1 = y1[:17000,]

print(y.shape)

# load all models
members = load_all_models()
print('Loaded %d models' % len(members))

# evaluate standalone models on test dataset
for model in members:
        _, acc = model.evaluate(x, y1, verbose=1)
        print('Model Accuracy: %.3f' % acc)

# define ensemble model
stacked_model = define_stacked_model(members)

# fit stacked model on test dataset
fit_stacked_model(stacked_model, x, y)

X = [x for _ in range(len(stacked_model.input))]
_, acc = stacked_model.evaluate(X, y, verbose=1)
print('Model Accuracy: %.3f' % acc)

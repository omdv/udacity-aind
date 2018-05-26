import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
# Answer: just a simple loop
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    for i in range(0, series.shape[0] - window_size):
        X.append(series[i:i+window_size])
    y = series[window_size:]

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
# Answer: One LSTM layer followed by a dense
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape = (window_size,1)))
    model.add(Dense(1))
    return model

### TODO: return the text input with only ascii lowercase and the punctuation given below included.
### Answer: go over all unique chars and if not in the allowed char list - replace with space
def cleaned_text(text):
    import string
    punctuation = ['!', ',', '.', ':', ';', '?']
    for ch in list(set(text)):
        if (ch not in punctuation) & (ch not in string.ascii_lowercase):
            text = text.replace(ch, ' ')
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
### Answer: iterate until we have enough characters
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    
    pos = 0
    while (pos+window_size) < len(text):
        inputs.append(text[pos:pos+window_size])
        outputs.append(text[pos+window_size])
        pos += step_size

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
# Answer: LSTM hidden layer followed by softmax
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape = (window_size, num_chars)))
    model.add(Dense(num_chars, activation='softmax'))
    return model

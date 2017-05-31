


from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
import pre

from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
import os

import numpy as np





def train(src,dest,pivot_num,pivot_min_st,dim):
    outputs = pivot_num
    HUs =dim
    x, y, x_valid, y_valid,inputs= pre.preproc(pivot_num,pivot_min_st,src,dest)



    #mat= np.load("kw.npy")
    #print "the shape is ",mat[0].shape

    model = Sequential()
    model.add(Dense(HUs,input_shape=(inputs,),init='glorot_normal'))
    #model.add(Dense(HUs, input_shape=(inputs,)))
    model.add(Activation('sigmoid'))
    model.add(Dense(outputs))
    model.add(Activation('sigmoid'))
    print model.summary()
    sgd = SGD(lr=0.1, decay=1e-5, momentum=0.9)

    model.compile(optimizer=sgd, loss='binary_crossentropy')


    earlyStopping = EarlyStopping(monitor='val_loss', patience=0, mode='min')
    save_best = ModelCheckpoint("best_model", monitor='val_loss', verbose=0, save_best_only=True, mode='auto')

    h=model.fit(x, y, batch_size=1,callbacks=[earlyStopping],nb_epoch=10,validation_data=(x_valid,y_valid), shuffle=True)
    print (h.history['val_loss'])[-1]
    weight_str = src + "_to_" + dest + "/weights/w_"+src+"_"+dest+"_"+str(pivot_num)+"_"+str(pivot_min_st)+"_"+str(HUs)
    filename = weight_str
    if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

    np.save(weight_str, model.get_weights())

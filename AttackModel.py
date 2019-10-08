from time import sleep
import progressbar
import keras
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as ticker
import keras.backend as K 
import numpy as np
import matplotlib.pyplot as plt

def Mal_I_FGSM(model,x,y,bool_maps,epsilon,N,plot_SR = False):
  if plot_SR == True:
    SR = np.zeros(N)
  x_adv = x
  y_onehot = keras.utils.to_categorical(y, 25)
  sess = K.get_session()
  target = K.one_hot(y, 25)
  loss_f = K.categorical_crossentropy(target, model.output)
  grads_f = K.gradients(loss_f, model.input)
  for i in progressbar.progressbar(range(N), max_value = N, widgets=['Generating: ', progressbar.Bar(),' ',
                                                    progressbar.Counter(format='%(value)02d/%(max_value)d')]):
    grads = sess.run(grads_f, feed_dict={model.input:x_adv})
    grads[0] = grads[0]*bool_maps
    x_adv = x_adv + epsilon*np.sign(grads[0])
    x_adv = np.clip(x_adv,0.0,1.0)
    if plot_SR == True:
      SR[i] =(1 - model.evaluate(x_adv, y_onehot, verbose=0)[1])*100
    sleep(0.05)
  #plot SR through each iterations
  if plot_SR == True:
    index = range(N)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    SR_plt= ax.plot(index,SR)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Success Rate')
    plt.show()
  return x_adv

def Mal_RI_FGSM(model,x,y,bool_maps,epsilon,N,alpha,plot_SR = False):
  if plot_SR == True:
    SR = np.zeros(N)

  x_adv = x
  y_onehot =  keras.utils.to_categorical(y, 25)
  sess = K.get_session()
  target = K.one_hot(y, 25)
  loss_f = K.categorical_crossentropy(target, model.output)
  grads_f = K.gradients(loss_f, model.input)
  for i in progressbar.progressbar(range(N), max_value = N, widgets=['Generating: ', progressbar.Bar(),' ',
                                                    progressbar.Counter(format='%(value)02d/%(max_value)d')]):
    grads = sess.run(grads_f, feed_dict={model.input:x_adv})
    grads[0] = grads[0]*bool_maps
    x_adv = x_adv + alpha*np.sign(np.random.normal(0,1.0,x_adv.shape))*bool_maps
    x_adv = x_adv + (epsilon-alpha)*np.sign(grads[0])
    x_adv = np.clip(x_adv,0.0,1.0)
    if plot_SR == True:
      SR[i] =(1 - model.evaluate(x_adv, y_onehot, verbose=0)[1])*100
    sleep(0.05)
  #plot SR through each iterations
  if plot_SR == True:
    index = range(N)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    SR_plt= ax.plot(index,SR)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Success Rate')
    plt.show()
  return x_adv

def Mal_MI_FGSM(model,x,y,bool_maps,epsilon,N,theta,plot_SR = False):
  if plot_SR == True:
    SR = np.zeros(N)

  x_adv = x
  y_onehot =  keras.utils.to_categorical(y, 25)
  sess = K.get_session()
  target = K.one_hot(y, 25)
  loss_f = K.categorical_crossentropy(target, model.output)
  grads_f = K.gradients(loss_f, model.input)
  g_0 = 0
  for i in progressbar.progressbar(range(N), max_value = N, widgets=['Generating: ', progressbar.Bar(),' ',
                                                    progressbar.Counter(format='%(value)02d/%(max_value)d')]):
    grads = sess.run(grads_f, feed_dict={model.input:x_adv})
    grads[0] = grads[0]*bool_maps
    g = np.reshape(grads[0],[grads[0].shape[0],-1])
    norm_g = np.linalg.norm(g,ord=1,axis = 1)
    if (np.max(grads[0])<1E-10):
        g_1 = theta*g_0
    else:
        g_1 = theta*g_0 + grads[0]/(norm_g[:,None,None,None]+1E-10)
    g_0 = g_1
    x_adv = x_adv + epsilon*np.sign(g_1)
    x_adv = np.clip(x_adv,0.0,1.0)
    if plot_SR == True:
      SR[i] =(1 - model.evaluate(x_adv, y_onehot, verbose=0)[1])*100
    sleep(0.05)
  #plot SR through each iterations
  if plot_SR == True:
    index = range(N)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    SR_plt= ax.plot(index,SR)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Success Rate')
    plt.show()
  return x_adv
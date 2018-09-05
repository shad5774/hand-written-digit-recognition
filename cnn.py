# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zGbKwfNexbPEndTmv-B5Hfmqeudysmuq
"""

#cd Desktop

#ls

# coding: utf-8

# In[6]:


import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


# In[8]:


import numpy as np
import matplotlib.pyplot as plt

#plt.imshow(mnist.train.images[0].reshape(28,28))


# In[9]:


def conv2d(x,F):
    #  x-->[batch,H,W,channel]
    #  F --> [H,W,channel_in,total_Filter_out]
    return tf.nn.conv2d(x,F,strides=[1,1,1,1],padding='SAME')


# In[10]:


def max_pool(x):
    
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')


# In[11]:


def init_weights(shape):
    var=tf.truncated_normal(shape=shape,stddev=0.1)
    return tf.Variable(var)
    


# In[18]:


def init_bias(shape):
    var=tf.constant(0.1,shape=[shape])
    return tf.Variable(var)
    


# In[19]:


def conv_layer(input_x,shape):
    W=init_weights(shape)
    b=init_bias(shape[3])
    return tf.nn.relu(conv2d(input_x,W)+b)


# In[40]:


def den_layer(input_layer,size):
    input_size=int(input_layer.get_shape()[1])
    W=init_weights([input_size,size])
    b=init_bias(size)
    return tf.matmul(input_layer,W)+b

    


# In[41]:


x=tf.placeholder(tf.float32,[None,784])

y=tf.placeholder(tf.float32,[None,10])


# In[42]:


x_image=tf.reshape(x,[-1,28,28,1])


# In[43]:


convo_1=conv_layer(x_image,shape=np.array([5,5,1,32]))
max_pool1=max_pool(convo_1)

convo_2=conv_layer(max_pool1,shape=np.array([5,5,32,64]))
max_pool2=max_pool(convo_2)





# In[46]:


flatten_arr=tf.reshape(max_pool2,[-1,7*7*64])
full_layer=den_layer(flatten_arr,1024)


# In[47]:


hold_prob=tf.placeholder(tf.float32)

full_dropout=tf.nn.dropout(full_layer,keep_prob=hold_prob)


# In[48]:


y_pred=den_layer(full_dropout,10)


# In[68]:


cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=y_pred))

optimizer=tf.train.AdamOptimizer(learning_rate=0.001)


# In[72]:


train_op=optimizer.minimize(cross_entropy)
init=tf.global_variables_initializer()


# In[1]:


steps=1000

with tf.Session() as sess:
    sess.run(init)
    for i in range(steps):
        batch_x,batch_y=mnist.train.next_batch(100)
        sess.run(train_op,feed_dict={x:batch_x,y:batch_y,hold_prob:0.5})
        if i%10==0:
            matches=tf.equal(tf.argmax(y_pred,1),tf.argmax(y,1))
            acc=tf.reduce_mean(tf.cast(matches,tf.float32))
            print(sess.run(acc,feed_dict={x:mnist.test.images,y:mnist.test.labels,hold_prob:1.0}))
            print('\n')


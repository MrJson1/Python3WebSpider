# -*- coding: utf-8 -*
import tensorflow as tf
import math

class captchaModel():
    def __init__(self,
                 width = 160,
                 height = 60,
                 char_num = 4,
                 classes = 62):
        self.width = width
        self.height = height
        self.char_num = char_num
        self.classes = classes

    def conv2d(self,x, W):
        #conv2d 是2维卷积函数，其中X为输入，W是卷积参数,strides 代表卷积模板移动的步长，都是1
        #代表划过图片的每一个点
        #padding 代表边界的处理方式，SAME 让卷积的输出和输入保持同样的尺寸
        # 步长是1，卷积的时候图片大小没有缩小。最大池化的时候图片减为一半。
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(self,x):
        #max_pool最大池化函数，最大池化会保留原始像素中灰度值最高的那一个像素，既保留最显著的特征
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],                 #用2*2的过滤器
                              strides=[1, 2, 2, 1], padding='SAME')  #横竖最大池化步长是2

    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape, stddev=0.1)   #截断正态分布噪声标准为0.1
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.1, shape=shape)     #0.1是用来避免死亡节点的
        return tf.Variable(initial)

    def create_model(self,x_images,keep_prob):   #x_images 是特征
        #first layer
        w_conv1 = self.weight_variable([5, 5, 1, 32])   #通过过滤器计算权重值5*5*32  32个卷积核
        b_conv1 = self.bias_variable([32])              #32是[5,5,1,32]中的32的输出。a[1]=Relu(w[1]a[0]+b[1]),因为w[1]a[0]是32，矩阵相加。
        h_conv1 = tf.nn.relu(tf.nn.bias_add(self.conv2d(x_images, w_conv1), b_conv1))  #relu激励函数进行非线性处理
        #或者可以以下的写法
        # h_conv1 = tf.nn.relu(self.conv2d(x_images, w_conv1) + b_conv1) #relu激励函数进行非线性处理
        h_pool1 = self.max_pool_2x2(h_conv1)

        h_dropout1 = tf.nn.dropout(h_pool1,keep_prob) #keep_prob 减轻过拟合，预测时则保留全部的数据追求最好的预测性能
        conv_width = math.ceil(self.width/2)          #math.ceil 向上取整
        conv_height = math.ceil(self.height/2)

        #second layer
        w_conv2 = self.weight_variable([5, 5, 32, 64])
        b_conv2 = self.bias_variable([64])
        h_conv2 = tf.nn.relu(tf.nn.bias_add(self.conv2d(h_dropout1, w_conv2), b_conv2))
        h_pool2 = self.max_pool_2x2(h_conv2)

        h_dropout2 = tf.nn.dropout(h_pool2,keep_prob)
        conv_width = math.ceil(conv_width/2)
        conv_height = math.ceil(conv_height/2)


        #third layer
        w_conv3 = self.weight_variable([5, 5, 64, 64])
        b_conv3 = self.bias_variable([64])
        h_conv3 = tf.nn.relu(tf.nn.bias_add(self.conv2d(h_dropout2, w_conv3), b_conv3))
        h_pool3 = self.max_pool_2x2(h_conv3)

        h_dropout3 = tf.nn.dropout(h_pool3,keep_prob)
        conv_width = math.ceil(conv_width/2)
        conv_height = math.ceil(conv_height/2)

        # 前面进行了2次步长所以边只有4分之1了的长度了（假设是28*28 现在就变成了7*7 第二个卷积层有64个卷积核，那么就变成7*7*64）

        #后面的全连层是输出分类的结果，前面的主要是特征提取工作
        #first fully layer
        conv_width = int(conv_width)
        conv_height = int(conv_height)
        w_fc1 = self.weight_variable([64*conv_width*conv_height,1024])      #隐含节点1024
        b_fc1 = self.bias_variable([1024])
        h_dropout3_flat = tf.reshape(h_dropout3,[-1,64*conv_width*conv_height])
        #跟V5有点区别
        # dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])

        # w_fc1 也有区别
        #w_d = tf.Variable(w_alpha * tf.random_normal([8 * 32 * 40, 1024]))
        h_fc1 = tf.nn.relu(tf.nn.bias_add(tf.matmul(h_dropout3_flat, w_fc1), b_fc1))    #matmul 矩阵相乘
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        #second fully layer
        w_fc2 = self.weight_variable([1024,self.char_num*self.classes])
        b_fc2 = self.bias_variable([self.char_num*self.classes])
        y_conv = tf.add(tf.matmul(h_fc1_drop, w_fc2), b_fc2)

        return y_conv


# if __name__ == '__main__':
#     captchaModel = captchaModel()
#     print(captchaModel.create_model())
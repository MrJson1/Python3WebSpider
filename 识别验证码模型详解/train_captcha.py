#-*- coding:utf-8 -*-
import tensorflow as tf
import numpy as np
import string
import generate_captcha
import captcha_model
import time


if __name__ == '__main__':

    captcha = generate_captcha.generateCaptcha()
    width,height,char_num,characters,classes = captcha.get_parameter()

    #X是特征,placeholder作为存放输入数据的地方。这里维度也不一定要定义
    x = tf.placeholder(tf.float32, [None, height,width,1])
    #V5的特征是这样的,大写X是特征
    # x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    #y_是真实的label
    y_ = tf.placeholder(tf.float32, [None, char_num*classes])
    # keep_prob 减轻过拟合，预测时则保留全部的数据追求最好的预测性能
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width,height,char_num,classes)
    y_conv = model.create_model(x,keep_prob)
    #tf.reduce_mean 函数用于计算张量tensor沿着指定的数轴（tensor的某一维度）上的的平均值，
    # 主要用作降维或者计算tensor（图像）的平均值
    #定义自己的损失函数
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_,logits=y_conv))
    #优化器使用Adam，1e-4比较小的学习效率   optimizer 为了加快训练 learning_rate应该开始大，然后慢慢衰
    #反向传播算法
    optimizer = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    predict = tf.reshape(y_conv, [-1,char_num, classes])
    real = tf.reshape(y_,[-1,char_num, classes])

    #定义评测准确率的操作
    correct_prediction = tf.equal(tf.argmax(predict,2), tf.argmax(real,2))
    correct_prediction = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(correct_prediction)

    saver = tf.train.Saver()
    start_time = time.time()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        step = 1
        while True:
            batch_x,batch_y = next(captcha.gen_captcha(64))
            _,loss = sess.run([optimizer,cross_entropy],feed_dict={x: batch_x, y_: batch_y, keep_prob: 0.75})
            print ('step:%d,loss:%f' % (step,loss))
            if step % 100 == 0:
                batch_x_test,batch_y_test = next(captcha.gen_captcha(100))
                acc = sess.run(accuracy, feed_dict={x: batch_x_test, y_: batch_y_test, keep_prob: 1.})
                print ('###############################################step:%d,accuracy:%f' % (step,acc))
                if acc > 0.60:
                    saver.save(sess,"./models/capcha_model.ckpt")
                    print(time.time() - start_time)
                    break
            step += 1
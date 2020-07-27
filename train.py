import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

min_max_scaler = MinMaxScaler()

batch_size_list=[128,8,64,8,32,8,1,16,1,64]

def create_mode(category):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(32, input_shape=(3,), activation='relu'))
    model.add(tf.keras.layers.Dense(32, activation='relu'))
    model.add(tf.keras.layers.Dense(2, activation='sigmoid'))

    model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001), loss='mse', metrics=['accuracy'])
    # model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    a = x[(x["category"] == category)]
    a = a.drop(["category"], axis=1)
    id_list = a.index.values.tolist()    # 根据a的id获取相应y的行
    index_list = []
    for i in range(0, len(id_list)):  # 不然用y.iloc[2,5,7]给的是id为3，5，8的
        index_list.append(id_list[i] - 1)
    b = y.iloc[index_list]
    b = b.values

    min_max_scaler.fit(a)    # min-max归一化
    a = min_max_scaler.transform(a)
    min_max_scaler.fit(b)
    b = min_max_scaler.transform(b)

    history = model.fit(a, b, epochs=1000, batch_size=batch_size_list[category])
    # acc = history.history['accuracy']
    # loss = history.history['loss']
    #
    # epochs = range(len(acc))  # Get number of epochs
    #
    # # 画accuracy曲线
    # plt.plot(acc, 'b')
    # plt.title('Training accuracy')
    # plt.xlabel("Epochs")
    # plt.ylabel("Accuracy")
    # plt.legend(["Accuracy"])
    # plt.figure()
    # plt.show()
    #
    # # 画loss曲线
    # plt.plot(epochs, loss, 'r')
    # plt.title('Training loss')
    # plt.xlabel("Epochs")
    # plt.ylabel("Loss")
    # plt.legend(["Loss"])
    # plt.figure()
    # plt.show()

    return model

if __name__ == '__main__':
    FILENAME = "/Users/barney/Desktop/Video.csv"

    np.set_printoptions(suppress=True)

    ori_data=pd.read_csv(FILENAME,index_col="id")

    col_name = ori_data.columns.tolist()
    col_name.insert(0, "diff_time")
    ori_data = ori_data.reindex(columns=col_name)
    for i in range(1, len(ori_data) + 1):
        ori_data.loc[i, "diff_time"] = ori_data.loc[i, "now_time"] - ori_data.loc[i, "create_time"]
    ori_data = ori_data.drop(["now_time", "create_time"], axis=1)

    x = ori_data.iloc[0:1000, 0:4]
    y = ori_data.iloc[0:1000, 4:6]
    test_x=ori_data.iloc[1000:,0:4]
    test_y=ori_data.iloc[1000:,4:6]

    model_0=create_mode(0)
    model_1=create_mode(1)
    model_2=create_mode(2)
    model_3=create_mode(3)
    model_4=create_mode(4)
    model_5=create_mode(5)
    model_6=create_mode(6)
    model_7=create_mode(7)
    model_8=create_mode(8)
    model_9=create_mode(9)
    models=[model_0,model_1,model_2,model_3,model_4,model_5,model_6,model_7,model_8,model_9]

    test_categories=[]
    for i in range(0,len(test_x)):
        row=test_x.iloc[i:i+1]    # 不然会变成Series 很麻烦
        category=int(row.iloc[0].category)
        test_categories.append(category)

    test_x = test_x.drop(["category"],axis=1)

    min_max_scaler.fit(test_x)
    test_x = min_max_scaler.transform(test_x)

    for i in range(0,len(test_x)):
        row = test_x[i:i + 1]
        temp_result = models[test_categories[i]].predict(row)    # 选取特定分类的model去预测
        if i==0:
            result=temp_result
        else:
            result=np.vstack((result,temp_result))

    min_max_scaler.fit(test_y)
    result = min_max_scaler.inverse_transform(result)


    original=test_y.values


    # 画出来对比一下
    plt.plot(original[:, 0:1], "r", label="original")
    plt.plot(result[:,0:1],"b", label="prediction")
    plt.legend(loc=1)
    plt.show()


    plt.plot(original[:, 1:2], "r", label="original")
    plt.plot(result[:,1:2],"b", label="prediction")
    plt.legend(loc=1)
    plt.show()


    m=result[:,1:2].astype(int).flatten().tolist()
    n=original[:,1:2].flatten().tolist()
    from music.dispose.similarity import *
    print(pearsonrSim(m,n))

    # m=result[:,0:1].astype(int).flatten().tolist()
    # n=original[:,0:1].flatten().tolist()
    # print(pearsonrSim(m,n))
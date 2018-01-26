# GameTester
GameTester 是一个Android测试工具. 虽然这里写的是德州扑克的环境，但是稍加修改用作其他游戏的测试也是可以的.

### 环境配置

1. 使用python3
2. opencv
3. 配置Java环境
4. 下载[! Android SDK tools](http://www.androiddevtools.cn/)，按照自己的操作系统选择
5. 配置环境变量，使用ADB SHELL
6. windows下可能需要额外下载platform-tools，文件不大，我在env文件下放了一份，解压到和tools同一级即可。同样成功的标志是在终端下运行adb

### 代码文件

未提及的文件按照它的名字理解就可以了

1. MainTester.py

    在这个代码文件中，加入算法程序。下面的例子是每个两秒发送一次指令，并在指令为“1：截图指令”是使用opencv作图像识别
    ```python
        # here to add algorithm thread
        while True:  # random decision
            time.sleep(2)  # send a decision every second
            instruct = random.randint(1, 7)
            actor.handleInstruct(instruct)
            
            if instruct == 1:
                img_rgb = cv2.imread(self.rawSnapShot+'demo.png')
                hand_card = get_hand_card(img_rgb)
                public_card = get_public_card(img_rgb)
                print (hand_card)
                print (public_card)
    ```

2. Actor.py

    ADB SHELL 控制设备的具体实现

3. SnapShotProc.py

    这个代码，目前并没有使用。原来使用这个代码是为了做一个专门截图的线程，但是现在的话截图是算法主动触发的。

4. Vision

    使用opencv的图像识别模块

5. BehaviorUtils/Behavior.py

    保存动作信息

6. BehaviorUtils/PreSetter.py

    从TestSet/test.xml文件中，解析动作信息

7. RelatedFiles/ConfigXml/test.xml

    按照XML格式保存动作信息，需要其他动作，模仿范例即可。指令的数字也是按照这里的顺序来的。比如XML里面第2个动作是截图，那么对应的指令就是1


### 已知缺陷

1. 在这个德州扑克游戏中，没有做换桌之类的动作
2. 对多个设备同时测试的效果未知
3. 使用时需要注意路径
4. 
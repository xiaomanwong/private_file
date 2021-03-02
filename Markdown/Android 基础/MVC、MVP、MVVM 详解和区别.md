---
title: MVC、MVP、MVVM 的详解和区别
tag: 软件架构
category: Android
---



## MVC、MVP、MVVM  图示

### MVC

![MVC 结构](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/bg2015020105.png)

* 视图层（View） 对应 XML 布局和 Java 代码动态 View 部分
* 控制层（Controller） MVC 中 Android 的控制层是由 Activity 来承担的， Activity 本来主要是作为初始化页面，展示数据的操作，但是因为 XML 视图功能太弱，所以 Activity 既要负责视图的显示，又要加入控制逻辑，承担的功能过多
* 模型层（Model）针对业务模型，建立数据结构和相关的类，主要分则网络请求、数据库处理、I/O 操作

**总结：**

具有一定的分层， model 彻底解耦， controller  和 view 并没有解耦，层与层之间的监护尽量使用回调或者去使用消息机制去完成，尽量避免直接持有 controller  和 view 在 Android 中无法做到彻底分离，但在代码逻辑层面要分清业务逻辑被放在 model 层，能够更好的复用和修改、增加业务。

### MVP

![MVP](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/bg2015020108.png)

通过引用接口 `BaseView` ，让相应的试图组件如 Activity, Fragment 去实现 `BaseView` ，实现视图层的独立，通过中间层 Presenter 实现 Model 和 View 的完全解耦。使得更层级之间的通信都是双向的

MVP 彻底解决了 MVC 中 View 和 Controller 分不清楚的问题，但是随着业务的增加，一个页面可能会非常复杂，UI 的改变是非常多的，会有非常多的 case，这样会造成 View 的接口会很庞大。

### MVVM

![img](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/bg2015020110.png)

MVP 中我们说过随着业务逻辑的增加，UI 的改变多的情况下，会有很多的更 UI 相关的 case， 这样会造成 View 的接口很庞大。而 MVVM 就解决了这个问题，通过**双向绑定**的机制，实现数据和 UI 内容，只要想改其中一方，另一方都能够及时更新的一种设计理念，省区了很多在 View 中些很多 case 的情况。

DataBinding 是谷歌退出的方便实现 MVVM 的工具。由于数据和视图的双向绑定，导致出现问题时不好定位来源，有可能数据问题导致，也有可能业务逻辑中怼试图属性的修改导致。如果打算用 MVVM 的话，可以考虑 Jetpack 全家桶。



## 如何选择

* 如果项目简单，没有什么复杂性，未来改动也不大的话，那就不要用设计模式或者架构方法，只需要将每个模块封装好，方便调用就好，不要为了使用设计模式或者架构方法而使用
* 对于偏向展示行的 APP，绝大多数业务逻辑都在后端， app 的主要功能就是展示数据，交互等。建议使用 MVVM。
* 对于工具类或者需要些很多业务逻辑的app ，使用 mvp 和 mvvm 都可以。
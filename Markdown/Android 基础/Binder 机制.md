---
title: Binder 机制
tag: Binder
category: Android
---



## 为什么选用 Binder 作为进程间通信的工具

相比于传统的 IPC 机制，Binder 具有

1. 性能上只对数据进行一次 copy （mmap 关系映射）
2. 稳定性上基于 C/S 架构，使得业务上相互独立
3. 安全上Android 为每一个App 提供了 UID 和 PID， 有效防止流氓软件的侵袭
4. 语言层面上更符合 Java 的面向对象思想

## Binder 机制的构成

1. Client:

   负责发起请求，获取数据

2. Server

   负责接收请求，处理并返回数据

3. ServiceManager

   用来管理 Server , 并未 Client 提供查询 Server 接口的能力

4. Binder 驱动器：

   提供设备文件 “/dev/binder”与用户空间交互， Client Server 和 ServiceManager 通过 open 、mmap、 ioctl 文件操作等函数与 Binder 驱动程序进行通信。

## mmap 是什么

Binder 基于 mmap 内存映射来实现进程间通信。

**当发起一个 IPC 通信时**

1. 首先 Binder 驱动程序在内核空间上创建一个数据接收缓存区
2. 其次在内核空间上开辟一块内核缓存区，建立 **内核缓存区** 和 **内核数据接收缓存区** 的映射关系，已经 **内核数据接收缓存区** 和 **接收进程用户空间地址** 的映射关系
3. 发送方进程通过系统调用 `copy_from_user` 将数据从发送端 copy  到**内核缓存区**，由于内核缓存区和接收进程用户空间地址的映射关系，也就相当于把数据发送给了接收端用户空间，因此完成了一次进程间通信。

## 如何完成一次 IPC 开发

使用 AIDL 用到的几个类：

* IBinder： 是一个接口，代表了一种跨进程通信的能力，只要实现接口就可以通信
* IInterface: 代表的是 Server 进程对象具备的能力（可以提供方法，就是 AIDL 中的方法）
* Binder： Java 层的 Binder 类，代表本地 Binder 对象； BinderProxy 是 Binder 的内部类，代表远程进程的 Binder 对象的本地代理。都具有进程间通信能力，Binder 层会自动转换
* Stub：AIDL 时编译工具会自动生成一个名为 Stub 的静态内部类，其继承自 Binder 是一个 Binder 的本地对象，实现了 IInterface 接口，具有和 Server 给Client 的能力， Stub 是一个抽象类，具体实现由开发者完成
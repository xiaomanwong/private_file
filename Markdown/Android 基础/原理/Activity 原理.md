---
titile: 一篇让你认识不一样的 Activity
tag: Activity
category: Android
---

## 前言

前段时间面试被问到了一些 Activity 的基础的知识，同时也被问到了一些有关 Activity 很深的东西。对于初级工程师，可能您只需要掌握了 Activity 的生命周期变化，就能够胜任这份工作；但作为中级/高级工程师，Activity 的基础知识就不能仅仅是表面现象了。

## Activity 的启动

System_server 进程创建完成后，会分阶段创建不同的服务

1. 创建 AMS、PMS、LS、DMS 服务

2. 创建 PKMS、WMS、IMS、NMS

   …..

3. 调用 WMS,PMS,PKMS 的systemReady 方法，表示系统启动完成

4. 启动 SystemUI，剩余服务调用 systemReady, 启动 watchDog

5. 各服务调用 systemRunning， AMS 调用 finishBooting



## AMS(ActivityManagerService)

AMS 是 IBinding 接口的实现类，用来处理进程间通信，管理 Activity 的一个系统服务。

## SystemServer 的启动

SystemServer.main() 初始化对象，并调用 run 函数

SystemServer.run： 创建服务

1. createSystemContext 创建系统上下文
2. startBootScrapServices 创建引导服务  ==> 包含 AMS,PMS, PKMS, WMS 等
3. startCoreServices 创建核心服务
4. startOtherService 创建其他服务
5. Looper.loop() 

与 Activity 管理有关的数据结构

* ActivityRecord
  * Activity 栈，每一条记录都是一个 Activity 实例
  * 由 ActivityStater.startActivity 创建
* TaskRecord
  * 维护 List<ActivityRecord> 管理 ActivityRecord
* ActivityStack
  * 维护 List<TaskRecord> 管理 TaskRecord
* ActivityStackSupervior
  * 维护 ActivityStack
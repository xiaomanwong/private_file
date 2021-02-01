---
title: WorkManager 基础
tag: Jetpack
category: WorkManager
---



## 目标

`WorkManager` 是要给 API,  可让您轻松的调度那些**即使在退出应用或重启设备后仍可运行的可延期异步任务。**也就是说，只要是我们创建好了一个后台任务，交给 `WorkManager` 后，系统会保证它一定被执行。

<!-- more -->

## 基本操作

先来看一下 `WorkManager` 是如何使用的

```kotlin
WorkManager.getInstance(this.requireContext())
	.beginWith(listOf(workA, workB))
	.then(workC).enqueue()
```

这是一个最复杂的调用结构，基本上也是我们使用 `WorkManager` 最复杂的情况。

对于每项工作任务，我们都可以定义工作的输入和输出。并将工作串联在一起，`WorkManager` 会自动将输出从要给工作任务传递到下一个任务。

>  Note: WorkManager 适用于 **可延期** 工作，即不需要立即运行，但需要可靠执行的工作。即使退出应用或设备重启也不影响工作的执行。比如： 
>
> * 向后端服务发送日志或分析数据
> * 定期将应用数据与服务器同步

### 使用入门

#### 依赖库

先添加依赖库：

```groovy
dependencies {
    implementation "androidx.work:work-runtime-ktx:2.4.0"
}
```

#### 定义任务

使用 `Worker` 类定义，实现 `doWork()` 函数，为 `WorkManager` 提供的后台线程异步运行。

```kotlin
class WorkA(appContext:Context, workerParams: WorkerParameters): Worker(appContext, workerParams) {
    override fun doWork(): Result {
        // Do the work here
        
        return Result.success();
    }
}
```

从 `doWork()` 返回的 `Result` 会通知 `WorkManager` 服务工作是否成功，以及工作失败时是否应重试工作

* Result.success():  work 成功完成
* Result.failure(): work 失败
* Result.retry(): work 失败，根据重试策略在其他时间尝试

### 函数介绍

#### WorkRequest

定义好任务后，我们需要使用 `WorkManager` 服务进行调度该工作才可以运行。`WorkManager` 提供了两种方式，为我们安排任务的执行。**周期任务**  和 **一次性任务**

不论我们选择何种方式调度，都始终使用的时 `WorkRequest`。 `Worker` 定义工作单元， `WorkRequest(及子类)` 规定工作方式和时间， `WorkManager` 负责执行和调度。

```kotlin
val workRequest: WorkRequest = OneTimeWorkRequestBuilder<WorkerA>().build()

WorkManager.getInstance(mContext)
	.enqueue(workRequest)
```

任务的执行时间，取决于 `WorkRequest` 中使用的约束和系统优化方案。

##### **如何定义和自定义 `WorkRequest`** 

* 调度一次性工作和重复工作
* 设置工作约束条件，例如要求连接到 Wi-Fi 网络或者充电
* 确保至少延时一定时间在执行
* 设置重试和退避策略
* 将输入数据传递给 Worker
* 使用标记将相关工作分组在一起

`Worker` 通过 `WorkRequest` 在 `WorkManager` 中进行定义。为使 `WorkManager` 调度任何工作，必须创建一个 `WorkRequest` 对象，并加入到执行队列

```kotlin
val mWorkRequest: WorkRequst 
WorkManager.getInstance(mContext).enqueue(mWorkRequest)
```

##### 一次性任务

对于无需额外配置的简单工作，可使用静态方法 `from` 

```kotlin
val mWorkRequest = OneTimeWorkRequest.from(MyWork::class.java)
```

对于复杂的工作，可使用构建器

```kotlin
val mWorkRequst = OneTimeWorkRequestBuilder<MyWork>()
// 设置约束条件
.build()
```

##### 周期性任务

可能我们需要定期备份数据，定期下载应用中的新鲜内容或者定期上传日志到服务器

```kotlin
val saveRequest = PeriodicWorkRequestBuilder<SaveImageToFileWork>(1, TimUnit.HOURS)
		// 设置约束条件
		.build()
```

时间间隔定义为两次重复执行之间的最短时间，工作器的确切执行时间取决于您在 `WorkRequest` 对象中设置的约束及系统执行的优化。

值得注意的是，最短的重复间隔为 15 分钟，即使我们设置了一个小于 15 分钟的时间，那么系统也会默认帮我们修改为 15 分钟。系统考虑到对电量的优化给予我们的配置。

##### 灵活的周期性任务

灵活的重复任务是对周期性任务的扩展，其特点是要我们对 `Worker` 的运行时间比较敏感的情况。我们可以将 `PeriodicWorkRequest` 配置为在每个时间间隔的 **灵活时间段** 内运行

![PeriodicWork RepatInterval](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/definework-flex-period.png)

如图，我们定义了具有灵活时间段的定期任务，需要在创建 `PeriodicWorkRequest`  时传递 `flexInterval` 和 `repeatInterval` 。灵活时间段从 `repeatInterval - flexInterval` 开始，一直到间隔结束

```kotlin
// 设置每小时的最后 15 分钟内运行的周期任务
val myUploadWork = PeriodicWorkRequestBuilder<SaveImageToFileWOrk> (
	1, TimeUnit.HOURS, // repeatInterval
    15, TimeUnit.MINUTES // flexInterval
)
```

#### 约束

约束可以确保将工作延迟到满足最佳条件时运行。

* NetworkType: 约束隐形 Wroker 所需的网络类型，如 WiFi
* BatteryNotLow：设置为 true， 表示当设备处于 “电量不足模式”时，Worker 不会运行
* RequiresCharging：设置为 true，表示只能在充电状态下运行
* Deviceldle：设置为 true，表示用户的设备必须处于空闲状态，才能工作。如果要运行批量操作，二则可能会降低用户设备上正在运行的应用性能。
* StorageNotLow： 设置为 true，那么当用户设备上的存储空间不足时，不会工作。

##### 创建约束

```kotlin
val constraints = Constraints.Builder()
	.setRequiredNetworkType(NetworkType.UNMETERED)
	.setRequiresCharging(true)
	.build()

val myWorkRequest = OneTimeWorkRequestBuilder<MyWork>()
	.setConstraints(constraints)
	.build()
```

> 如果指定了多个约束，Work 将仅在所有约束同时满足时才会工作
>
> 如果 Worker 在运行时不满足某个约束， WorkManager 将停止工作器。系统将在满足所有约束后重试 Worker

##### 延时任务

如果没有添加约束，或者当其加入到队列是，所有约束都满足，系统就会选择立即执行该 Worker, 如果我们不希望他立即执行，可以将任务设置为在经过一段初始时间后再执行

```kotlin
val myWorkRequest = OneTimeWorkRequestBuilder<MyWork>()
	.setInitialDelay(10, TimeUnit.MINUTES)
	.build()
```

#### 重试和退避策略

```kotlin

val myWorkRequest = OneTimeWorkRequestBuilder<MyWork>()
   .setBackoffCriteria(
       BackoffPolicy.LINEAR,
       OneTimeWorkRequest.MIN_BACKOFF_MILLIS,
       TimeUnit.MILLISECONDS)
   .build()
```

如需要重试，可以让 `doWork()` 返回 `Result.retry()` 

#### 入参数据

当任务需要输入数据才能运行时，例如处理图片上传需要图片的 URI 作为输入数据。

输入数据以键值对的形式存储再 `Data` 对象中。Worker 可以通过 `Worker.getInputData()` 访问输入参数。

```kotlin
// Define the Worker requiring input
class UploadWork(appContext: Context, workerParams: WorkerParameters)
   : Worker(appContext, workerParams) {

   override fun doWork(): Result {
       val imageUriInput =
           inputData.getString("IMAGE_URI") ?: return Result.failure()

       uploadFile(imageUriInput)
       return Result.success()
   }
   ...
}

// Create a WorkRequest for your Worker and sending it input
val myUploadWork = OneTimeWorkRequestBuilder<UploadWork>()
   .setInputData(workDataOf(
       "IMAGE_URI" to "http://..."
   ))
   .build()
```

### 状态机

#### 一次性工作状态

初始态为 `ENQUEUED`, 在 `ENQUEUED` 下，当满足约束条件和初始延时要求后立即运行，转换为 `RUNNING` 状态，然后根据结果可转换为 `SUCCESSED`,`FAILED` 如果结果时 `retry`  可能会回到 `ENQUEUED`，随时可以取消进入 `CANCELLED` 状态

![一次性任务状态流转](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/one-time-work-flow.png)

`SUCCESSED, FAILED, CANCELLED` 均表示 `Worker` 的终止状态， `WorkInfo.State.isFinished() ` 都会返回 true。

#### 周期性任务工作状态

成功和失败仅时用于一次性和链式工作。周期性任务只有一个终止状态 `CANCELLED`。 这是因为周期任务永远不会结束。每次运行后，无论结果如何，都会重新对其进行调度。

![](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/periodic-work-states.png)

### 管理工作

#### 唯一性

- `WorkManager.enqueueUniqueWork()`（用于一次性工作）
- `WorkManager.enqueueUniquePeriodicWork()` (用于周期工作）

这两个方法接收 3 个参数

* `uniqueWorkName`: 唯一标识工作请求的 `String`
* `existingWorkPolicy`: 此 `enum` 可告知 WorkManager：如果已有使用该名称且尚未完成的唯一工作链，应执行什么操作。

```kotlin
val sendLogsWorkRequest =
       PeriodicWorkRequestBuilder<SendLogsWorker>(24, TimeUnit.HOURS)
           .setConstraints(Constraints.Builder()
               .setRequiresCharging(true)
               .build()
            )
           .build()
WorkManager.getInstance(this).enqueueUniquePeriodicWork(
           "sendLogs",
           ExistingPeriodicWorkPolicy.KEEP,
           sendLogsWorkRequest
)

```

#### 冲突解决策略

调用唯一工作是，必须告知 `WorkManager` 在发生冲突是要执行的操作。可以通过将工作加入到队列时传入一个枚举 `ExistingWorkPolicy` 和 `ExistingPeriodicWorkPolicy` 来实现

* REPLACE ：用新的任务替换现有任务。现有任务将取消

* KEEP： 保留现有任务，丢弃新任务
* APPEND：将新任务附加到现有任务的末尾，形成链式调用。新任务的执行条件取决于现有任务的状态
* APPEND_OR_REPLACE：类似于 APPEND ，不过不依赖现有任务的工作状态。

#### 获取状态

```kotlin
// WorkInfo 可通过 id，name，Tag 等方式获取，
workManager.getWorkInfoByIdLiveData(syncWorker.id)
               .observe(viewLifecycleOwner) { workInfo ->
   if(workInfo?.state == WorkInfo.State.SUCCEEDED) {
       Snackbar.make(requireView(),
      R.string.work_completed, Snackbar.LENGTH_SHORT)
           .show()
   }
}
```

### 观察任务进度

```kotlin
WorkManager.getInstance(applicationContext)
    // requestId is the WorkRequest id
    .getWorkInfoByIdLiveData(requestId)
    .observe(observer, Observer { workInfo: WorkInfo? ->
            if (workInfo != null) {
                val progress = workInfo.progress
                val value = progress.getInt(Progress, 0)
                // Do something with progress information
            }
    })
```


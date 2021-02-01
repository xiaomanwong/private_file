---
title: Android 架构组件
tag: Android
---



## 应用架构指南

* 当您在自己喜欢的社交网络应用中分享照片时会发生什么：
  1. 该应用将触发相机 Intent。 Android 操作系统随后会启动相机应用来处理请求。此时，用户已离开社交应用，但他们的体验仍然是无缝的
  2. 相机应用可能会触发其他 intent（如启动文件选择器），而这可能会再启动一个应用
  3. 最后，用户返回社交网络应用并分享照片

此过程中，用户随时可能会被电话或通知打断。处理之后，用户希望能够返回并继续分享照片。这种应用跳跃行为再移动设备上很常见，因此应用必须正确处理这些流程。


<!-- more -->
移动设备的资源也是有限的，因此操作系统可能会随时终止某些应用进程，一边为新的进程腾出空间

因此，不应该再应用组件中存储任何应用数据或状态，并且应用组件不应相互依赖

## 常见架构原则

### 分离关注点

常见错误是再 `activity` 和 `fragment` 中编写所有代码。这些基于界面的类应仅包含处理界面的操作系统交互的逻辑。您应使用这些类尽可能的保持精简，这样可以避免许多生命周期相关的问题

### 通过模型驱动界面

通过模型驱动界面（最好是持久性模型）。模型是负责处理应用数据的组件。独立于应用中的 View 对象和应用组件，因此不受应用生命周期以及相关的关注点影响。

持久性是思想之选，原因如下:

	1. 如果 Android 操作系统销毁应用以释放资源，用户不会丢失数据
	2. 当网络连接不稳定或不可用时，应用会继续工作

应用所基于的模型类应明确数据管理职责，这样使应用更可测试且更一致。



## 推荐应用架构

![img](https://developer.android.com/topic/libraries/architecture/images/final-architecture.png)

每个组件仅依赖于其下一级的组件。例如，Activity和Fragment 依赖于视图模型。存储区是唯一依赖于其他多个类的类；再本例中，存储区依赖于持久性数据模型和远程后端数据源。

这种设计打造了一致且愉快的用户体验。无论用户上次使用应用是再几分钟前还是几天前，现在回到应用时都会立即看到应用再本地保留的用户信息。如果此数据已过时，则应用的存储区模块将开始再后台更新数据。



## 构建界面

界面由Fragment `UserProfileFragment` 及其对应的布局文件 `user_profile_layout.xml` 组成

如需驱动该界面，数据模型需要存储以下数据元素

* 用户 ID： 用户的标识符。最好使用 Fragment 参数将此信息传递到相关的 Fragment中。如果 Android 系统销毁我们的进场，此类信息将保留，以便下次重启应用时 ID 可用。
* 用户对象：用于存储用户详细信息的数据类

> ViewModel 对象为特定的界面组件（如 Fragment 和 Activity）提供数据，并包含数据处理业务逻辑，以与模型进行通信。例如，View Model 可以调用其他组件来加载数据，还可以转发用户请求来修改数据。 View Model 不了解界面组件，因此不受配置更改（如再旋转设备时重新创建 Activity）的影响

* `user_profile.xml` : 屏幕的界面布局
* `UserProfileFragment`：显示数据的界面控制器
* `UserProfileViewModel` : 准备数据以便再 `UserProfileFragment` 中查看并对用户互动做出响应的类

**UserProfileViewModel**

```kotlin
class UserProfileViewModel: ViewModel(){
	val userId:String = TODO()
    val user: User = TODO()
}
```

**UserProfileFragment**

```kotlin
class UserProfileFragment: Fragment(){
    // 使用 ViewModels() 拓展函数，以及 "androidx.fragment:fragment-ktx:lastest-version" 在 模块下的 build.gradle 
    private val viewModel: UserProfileViewModel by viewModels()
    
    override fun onCreateView(
    inflater: LayoutInflater,
    container: ViewGroup?,
    savedInstanceState: Bundle?): View {
        return inflater.infalte(R.layout.main_fragment, container, false)
    }
}
```

现在，由了这些代码块，需要将他们串联起来，毕竟在 `UserProfileViewModel` 类中设置 `user` 字段时，我们需要一种方法来通知界面

要获取 `user` 我们的 `ViewModel` 需要访问 Fragment 参数。我们可以通过 fragment 传递，或者更好的办法时使用 `SaveState` 模块，我们可以让 View Model 直接读取参数

> SavedStateHandle 允许 ViewModel 访问相关 Fragment 或 Activity 的已保存状态和参数

```kotlin
// UserProfileViewModel
class UserProfileViewModel (savedStatedHandle: SavedStateHandle) :ViewModel(){
    val userId:String = savedStateHandle["uid"] ?: throw IllegalArgumentException("missing user id")
    val user: User = TODO()
}

// UserProfileFragment
private val viewModel: UserProfileViewModel by viewModels(
    factoryProducer = {SavedStateVMFactory(this)}
)
```




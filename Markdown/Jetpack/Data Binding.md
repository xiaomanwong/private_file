---
title: Android Data Binding
tag: Android
---

# Data Binding

## 概念

### 布局和绑定表达式 

借助表达式语言，可以编写将变量关联到布局中的视图的表达式。数据绑定库会自动生成将布局中的视图与数据对象绑定所需的类。该库提供了可在布局中使用的导入、变量和包含等功能。

<!-- more -->

该库的这些功能可与您的选优布局无缝共享。例如可以在表达式中使用的绑定变量在 `data` 元素（界面布局根元素的同级）内定义。这两个元素都封装在 `layout` 标记中。

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://scheams.android.com/apk/res-auto">
	<data>
    	<variable
                  name="viewModel"
                  type="com.myapp.data.ViewModel">
        </variable>
    </data>
    
    <ConstraintLayout>
    	<!-- UI layout`s root element-->
    </ConstraintLayout>
</layout>
```

### 使用可观察的数据对象



数据绑定库提供了可让您轻松地观察数据更改情况的类和方法。不必操心在底层始建于发生更改时刷新界面。可以将变量或其他属性设为可观察。借助该库，可以将对象、字段或集合设为可观察。

### 生成的绑定类

数据绑定库可以生成用于访问布局变量和视图的绑定类。此页面展示了如何使用和自定义所生成的绑定类。

### 绑定适配器

每一个布局表达式都又一个对应的绑定适配器，要求必须进行框架调用来设置响应的属性或监听。例如，绑定适配器负责调用 `setText()` 方法来设置文本属性，或者调用 `setOnClickListener()` 方法向点击事件添加监听器。最常用的帮i的那个适配器（例如针对本页面的示例中使用的 `android:text` 属性）可供您在 `android.databinding.adapters` 软件包中使用。也可以自定义适配器

``` kotlin
@BindingAdapter("app:goneUnless") 
fun goneUnless(view: View, visiable: Boolean) {
    view.visibility = if (visiable) View.VISIABLE else View.GONE
}
```


### 双向数据绑定

数据绑定库支持双向数据绑定。此类绑定使用的表示法支持以下操作：接收对属性的数据更改，同时监听用户对此属性的更新

<!-- more -->

## 使用入门

### 编译环境

要开始使用数据绑定，从 Android SDK 管理器中的 **支持代码库** 下载。要将应用配置为使用配置绑定，需要在应用模块的 `build.gradle` 文件中添加 `databinding` 元素

```groovy
android{
    ...
        dataBinding{
            enabled = true
        }
}
```

> 即使应用模块不直接使用数据绑定，也必须为依赖于与使用数据绑定库的应用模块配置数据绑定

### 布局和绑定表达式

借助表达式语言，可以编写表达式类处理视图分派的事件。事件绑定库会自动生成将布局中的视图与您的数据对象绑定所需的类。

数据绑定布局文件略有不同，以根标记`layout` 开头，后跟 `data` 和 `view` 根元素。此视图元素是非绑定布局文件的根

```xml
<?xml version="1.0" encodeing="utf-8"?>
<layout xmlns:android="http://scheams.android.comapk/res/android">
	<data>
    	<variable name="user"
                  type="com.example.User"/>
    </data>
    
    <LinearLayout android:orientation="vertical"
                  android:layout_width="match_parent"
                  android:layout_height="match_parent">
    	
        <TextView android:layout_width="wrap_content"
             	  android:layout_height="wrap_content"
	              android:text="@{user.fiestName}"/>
        
        <TextView android:layout_width="wrap_content"
                  android:layout_height="warp_content"
                  android:text="@{user.lastName}"/>
        
    </LinearLayout>
</layout>
```

`data` 中的 `user` 变量描述了可在此布局中使用的属性

```xml
<variable name="user" type="com.example.User"/>
```

布局中的表达式使用了 `@{}` 语法写入特性属性中，在这里， `TextView` 文本被设置为 `user.fistName` 和 `user.lastName`

```xml
<TextView android:layout_width="wrap_content"
          android:layout_height="warp_content"
          android:text="@{user.firstName}"/>

<TextView android:layout_width="wrap_content"
          android:layout_height="warp_content"
          android:text="@{user.lastName}"/>
```

### 数据对象

```kotlin
data class User(val firstName:String, val lastName: String)
```

### 绑定数据

系统会为每个布局文件生成一个绑定类。默认情况下，类名称基于布局文件的名称，它会转换为 Pascal 大小写姓氏并再末尾添加 Binding 后缀。以上布局文件名为 `activity_main.xml` ,因此生成的对应类为 `ActivityMainBinding`。 此类包含从布局属性（例如, user 变量）到布局视图的所有绑定，并且知道如何为绑定表达式指定值。建议的绑定创建方法是再扩充布局时创建。

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    val binding: ActivityMainBinding = DataBindingUtil.setContentView(this, R.layout.activity_main)
    
    binding.user= User('Test', "User")
}
```

再运行时，应用会再界面中显示 Test 用户。 或者，您可以使用 **LayoutInflater** 获取视图，

```kotlin
val binding: ActivityMainBinding= ActivityMainBinding.inflate(getLayoutInflater())
```

如果需要再 `Fragment` `ListView` 或 `RecyclerView` 适配器中使用数据绑定项，您可能更愿意使用绑定类或 `DataBindingUtil` 类的 `inflate()` 方法

```kotlin
val listItemBinding = ListItemBinding.inflate(layoutInflater, viewGroup, false)
// or
val listItemBinding = DataBindingUtil.inflate(layoutInflater, R.layout.list_item, viewGroup, false)
```

### 表达式语言

| 名称             | 符号                                |
| ---------------- | ----------------------------------- |
| 算数运算符       | +, -, /, *, %                       |
| 字符串连接运算符 | +                                   |
| 逻辑运算符       | &&, \|\|                            |
| 二元运算符       | &, \|, ^                            |
| 一元运算符       | +, -, !, ~                          |
| 移位运算符       | >> , <<, >>>                        |
| 比较运算符       | ==, >, <(需要转义为'&lt ;'), >=, <= |
|                  | instanceof                          |
| 分组运算符       | ()                                  |
| 字面运算符       | 字符，字符串，数字， null           |
| 类型转换         |                                     |
| 方法调用         |                                     |
| 字段访问         |                                     |
| 数组访问         | []                                  |
| 三元运算符       | ?:                                  |

```xml
<TextView
          android:text="@{String.valueOf(index+1)}"
          android:visibility="@{age > 13 ? View.GONE : View.VISIBLE}"
          android:transitionName="@{"image_"+id}"
```



### Null 合并运算符

> 如果左边运算不是 null, 则 Null 合并运算符(??) 选择左边运算数，如果左边为 null, 则选择右边

```
android:text="@{user.displayName ?? user.lastName}"
```

等效于

```
android:text="@{user.displayName != null ? user.displayName : user.lastName}"
```

### 视图引用

表达式可以通过以下语法按 ID  引用布局中的其他视图，并会将 ID 自动转换为驼峰法

```xml
<EditText
          android:id="@+id/example_text"
          android:layout_width="match_parent"
          android:layout_height="wrap_content"/>
<TextView
          android:id="@+id/example_output"
          android:layout_width="match_parent"
          android:layout_height="wrap_content"
          android:text="@{exampleText.text}"/>
```

### 集合

可以使用 `[]` 运算符访问常见集合，例如数组、列表、Hash 列表、和映射

```xml
<data>
	<import type="android.util.SparseArray"/>
    <import type="java.util.Map"/>
    <import type="java.util.List"/>
    <variable name="list" type="List$lt;String>"/>
    <variable name="sparse" type="Sparse$lt;String>"/>
    <variable name="map" type="Map$lt;<String, String>"/>
    <variable name="index" type="int"/>
    <variable name="key" type="String"/>
</data>

​```
android:text="@{list[index]}"
​```
android:text="@{sparse[index]}"
​```
android:text="@{map[key]}"
```

### 资源

表达式可以使用一下语法引用资源

```
android:padding="@{large?@dimen/largePadding : @dimen/smallPadding}"
```

某些资源需要显示类型求值

| 类型              | 常规引用  | 表达式引用         |
| ----------------- | --------- | ------------------ |
| String[]          | @array    | @stringArray       |
| int[]             | @array    | @intArray          |
| TypedArray        | @array    | @typedArray        |
| Animator          | @animator | @animator          |
| StateListAnimator | @animator | @stateListAnimator |
| color int         | @color    | @color             |
| ColorStateList    | @color    | @colorStateList    |

### 事件处理

可以编写从视图分派的表达式处理事件如：`onClick` 

#### 方法引用

事件可以直接绑定到处理脚本方法，类似于为 Activity 中的方法指定`android:onClick` 的方式。与 View d  onClick 特性相比，一个主要有点时表达式再编译时进行处理，因此，如果该方法不存在或其签名不正确，则会收到编译时错误。

方法引用和监听器绑定之间的主要却别在于实际监听器实现实在绑定数据时创建的，而不是再事件触发时创建的。

```kotlin
class MyHandler{
    fun onClickFriend(view:View){...}
}
```

绑定白哦大师可见视图的点击监听器分配给 `onClickFriend()` 方法

```xml
<layout xmlns:android="http://scheams.android.com/apk/res/android">
	<data>
    	<variable name="handlers" type="com.example.MyHandler"/>
        <variable name="user" type="com.example.User"/>
    </data>
    
    <LinearLayout
                  android:orientation="vertical"
                  android:layout_width="match_parent"
                  android:layout_height="match_parent">
    	<TextView
                  android:layout_width="wrap_content"
                  android:layout_height="wrap_content"
                  android:text="@{user.firstName}"
                  android:onClick="@{handlers::onClickFriend}"/>
    </LinearLayout>
              
</layout>
```

#### 监听器绑定

监听器绑定时再事件发生时运行的绑定表达式。类似于方法引用，但允许您运行任意数据绑定表达式。

在方法引用中，方法的参数必须与事件监听器的参数匹配。在监听器绑定中，只有您的返回值必须与监听器的预期返回值相匹配。

```kotlin
class Presenter {
    fun onSaveClick(task: Task)
}
```

将事件绑定到 `onSaveClick()` 方法

```xml
<layout xmlns:android="http://scheams.android.com/apk/res/android">
	<data>
    	<variable name="" type="com.example.Task"/>
        <variable name="presenter" type="com.example.Presenter"/>
    </data>
    
    <LinearLayout
                  android:orientation="vertical"
                  android:onClick="@{() -> presenter.onSaveClick(task)}"
                  android:layout_width="match_parent"
                  android:layout_height="match_parent"/>              
</layout>
```

在表达式中使用回调时，数据绑定会自动为事件创建并注册必要的监听器。当视图触发事件时，数据绑定会对给定表达式求值。与常规绑定表达式一样，在对这些监听器表达式求值时，仍会获得数据绑定的 Null 值和线程安全。

**避免使用复杂的监听器** 监听器表达式共嗯非常强大，可以使代码非常易于阅读。另一方面，包含复杂表达式的监听器会使布局难以阅读和维护。这些表达式应该像可用数据从界面传递到回调方法一样简单。



#### 导入、变量和 包含

导入：可以轻松的在布局文件中引用类

变量：可以描述可在绑定表达式中使用的属性

包含：可以在整个应用中重复使用复杂的布局

##### 导入

在 `data` 元素中使用多个 `import` 元素，也可以不用。

```xml
<data>
	<import type="android.view.View"/>
</data>
```

导入 View 类可以通过绑定表达式引用该类

```xml
<TextView
          android:text="@{user.name}"
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:visibility="@{user.isAdult ? View.VISIBLE : View.GONE}">
</TextView>
```

*类型别名*

当类名有冲突时，其中一个类可使用别名重命名。

```xml
<import type="android.view.View"/>
<import type="com.example.real.estate.View"
        alias="Visia"/>
```

##### 变量

`variable`  每个元素都描述了一个可以在布局上设置、并将在布局文件中的绑定表达式中使用的属性。

```xml
<data>
	<import type="android.graphics.drawable.Drawable"/>
    <variable name="user" type="com.example.User"/>
    <variable name="image" type="Drawable"/>
    <variable name="note" type="String"/>
</data>
```

变量类型在编译时进行检查，因此如果实现了  `Observable` 或者时 **可观察集合**，则因反应在类型中。

在生成的绑定类中，每个描述的变量都有一个对应的 setter 和 getter。在调用 setter 之前，这些变量一直采用默认的托管代码。

##### 包含

通过使用应用命名空间和特性中的变量名称，变量可以从包含的布局传递到被包含的布局绑定。

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
            xmlns:bind="http://schemas.android.com/apk/res-auto">
       <data>
           <variable name="user" type="com.example.User"/>
       </data>
       <LinearLayout
           android:orientation="vertical"
           android:layout_width="match_parent"
           android:layout_height="match_parent">
           <include layout="@layout/name"
               bind:user="@{user}"/>
           <include layout="@layout/contact"
               bind:user="@{user}"/>
       </LinearLayout>
    </layout>
```


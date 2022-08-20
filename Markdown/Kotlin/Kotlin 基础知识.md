

**[Kotlin 关键字](https://www.kotlincn.net/docs/reference/keyword-reference.html)**



`internal` : 模块内访问

`==` 和 `===` 

```text
`==` 等价于 Java 的 `a.equals(b)` ：值相等判断

`===` 等价于 Java 的 `a == b` ： 引用判断
```

`operator`： 讲一个函数标记为重载一个操作符或者实现一个约定(**解构**)

```kotlin
/// 定义解构
class User(var age:Int, var name:String) {
  operator fun component1() = age
  operator fun component2() = name
}
/// 定义操作符
public operator fun rangTo(other: Int):IntRange
```

`infix` 中缀表达式

``` kotlin
infix fun Int.vs(num: Int) : CompareResult = 
if(this - num > 0) {
  CompareResult.More
} else if (this - num  = 0) {
  CompareResult.Equal()
} else {
  CompareResult.More
}
print(5 vs 6)
```



反引号  : `` `

1. 解决关键字冲突问题

`typealias`: 别名，用于在跨平台上，做更好的平台兼容性

```kotlin
public typealias HashMap<String,Any> = java.lang.HashMap<>()
```



**DSL**

Domain Specific Language : 领域专用语言

外部 DSL： JSON, XML, CSS, Makefile

内部 DSL:	Anko， Kolley， build.gradle

优点： 极大的提高开发效率，减小沟通成本





Kotlin 中构建 DSL

* Lambda 语法
* 高阶函数
* 扩展函数
* 运算符重载
* 中缀表达式 



**Javap [options] *.class** 

* -l 输出行和变量表
* -public 只输出 public 方法和域
* -protected 只输出 public 和 protected 类和成员
* -package 只输出包， public 和 protected 类和成员，默认
* -p -private 输出所有类和成员
* -s 输出内部类型签名
* -c 输出分解后的代码，例如：类中每个方法内，包含 java 字节码的指令
* -verbose 输出栈大小，方法参数的个数
* -constants 输出静态 final 常量



**空安全实现**

Kotlin 空安全的实现分为两种

1. 运行时
2. 编译时

编译时 kotlin 将变量分为可空类型和非空类型，可空类型的变量，在编译期，编译器会自动检查，并插入检查代码，保证运行时不为空；

非空类型



**内联函数** inlinev



**泛型**

```kotlin
// Kotlin 对泛型进行约束
class Test<T> where T:Callback, T: Runnable {
  fun add(t: T) {
    t.run()
    t.callback()
  }
}

class A: Callback, Runnable{
  override fun run(){
    
  }
  
  override fun callback(){
    
  }
  
}

```

Kotlin 是真泛型

```kotlin
public <T> T fromJson(String json, Class<T> calssOfT) throws JsonSyntaxException{
  
}

inline fun <reified T> Gson.fromJson(json: String): T {
  return fromJson(json, T::class.java)
}
```

**Kotlin 扩展库**

* Kotlinx.coroutines
* Kotlinx-io
* Android KTX

协程：

协程和线程类似，但协程发生阻塞任务后，可主动交出 CPU 资源，交给其他的协程使用



**suspend**

协程挂起，被 suspend 修饰的函数智能被有 suspend 修饰的函数调用

suspend 修饰的函数或 lambda 被编译后悔多一个参数类型叫 Continuation

协程的异步调用本质上是一次回调（通过  Continuation 的 resume(value: T） 的回调

```kotlin 
fun test () {
  launch {
    val job = async {
				"hello"
    }
    println(job.await())
  }
}
```




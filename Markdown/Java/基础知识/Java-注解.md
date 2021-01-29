---
title: Java 注解
tag: Java
---

Java 注解又称标注。注解是元数据的一种形式，提供有关于程序但不属于程序本身的数据。注解对他们注解的代码的操作没有直接影响。

## 声明注解

Java 中所有的注解，默认实现接口 `Annotation` 接口

```java
public interface Annotation {
    boolean equals(Object obj);
    
    int hashCode();
    
    String toString();
    
    Class<? extends Annotation> annotationType();
}
```

与生命一个  Class 不同，注解的使用使用 `@interface` 管检测

```java
public @interface Login {}
```

## 元注解

在定义注解时，注解类也能够使用其他的注解声明，对注解类型进行注解的注解类。

## Target

注解标记另一个注解，以限制可以应用注解的 Java 元素类型。目标注解指定以下元素类型之一作为其值

* ElementType.ANNOTATION_TYPE 可以用于注解类型
* ElementType.CONSTRUCTOR 可以用于构造函数
* ElementType.FIELD 可以用于字段或属性
* ElementType.LOCAL_VARIABLE 可以用于局部变量
* ElementType.METHOD 可以应用于方法级注解
* ElementType.PACKAGE 可以应用于包生命
* ELementType.PARAMETER 方法参数
* ElementType.TYPE 用于类的任何元素

## Retention

注解指定标记注解的存储方式（作用域）：

* RetentionPolicy.SOUTRCE 标记注解仅保留在源码级别中，并被编译器忽略
* RetentionPolicy.CLASS 标记注解在编译时由编译器保留，但 Java 虚拟机会忽略
* RetentionPolicy.RUNTIME 标记的注解由 JVM 保留，因此运行时环境可以使用



## 应用场景

按照作用域来讲，注解可以被三种场景使用

### SOURCE

`RetentionPolicy.SOURCE` 作用于源码级别的注解，可提供给 IDE 语法检查， APT 等场景使用

**语法检查：**

在 `Adnroid `开发中，`support-annotations` 与 `androidx.annotation` 中均提供了 `@IntDef` 注解，

```java
@Retention(SOURCE)
@Target({ANNOTATION_TYPE}) 
public @interface IntDef {
    int[] value() default {};
    boolean flag() default false;
    boolean open() default false;
}
```

此注解的意义在于能够取代枚举，实现如方法入参限制

如：我们定义 test 方法，只接收 Teacher 参数，

```java
public enum Teacher {
    LILY, MARY
}

public void test(Teacher teacher) {}
```

而现在为了内存优化，我们现在不再使用枚举，则方法定义为

```java
public static final int LILY = 1;
public static final int MARY = 2;

public void test(int teacher){}
```

然而 `test` 方法由于采用基本数据类型 `int` ，讲无法进行类型限定。此时我们使用 `@IntDef` 增加自定义注解

```java
public static final int LILY = 1;
public static final int MARY = 2;

@IntDef(value = {LILY, MARY}) // 限定为 LILY, MARY
@Target(ElementType.PARAMETER) // 作用于参数的注解
@Retention(RetentionPolicy.SOURCE) 
public @interface Teacher{}

public void test(@Teacher int teacher) {}
```

此时，我们再去调用 `test` 方法，如果传递的参数不时 LILY, 和  MARY 则会显示 `Inspection` 警告

**APT 注解处理器**

apt 是 “Annotation Processor Tools” ，意为注解处理器。顾名思义，用于处理注解，编写好的 Java 源文件，需要经过 Javac 编译，翻译为虚拟机能够加载解析的字节码 class 文件。注解处理器是 Javac 自带的一个工具，用来编译时期扫描处理注解信息。



### Class

定义为 Class 的注解，会保留在 class 文件中，但是会被虚拟机忽略（无法在运行期反射获取注解）。此时需要符合此种注解的应用场景为字节码操作。像 AspectJ, 热修复等

所谓字节码操作，就是直接修改字节码 Class 文件以达到修改代码逻辑的目的，在程序中有多处需要进行是否登录判断。

我们借助 AOP （面向切面编程）的思想，将程序的功能点划分为：*需要登录* 和 *不需要登录* 即两个切面，对于切面的区分可采用注解

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.CLASS)
public @interface LoginAspect{}

@LoginAspect
public void jumpA(){
    startActivity(new Intent(this, AActivity.class));
}

public void jumpB(){
    startActivity(new Intent(this, BActivity.class));
}
```

### Runtime

注解保留到运行期，意味着我们能够在运行期间结合反射技术获取注解中的所有信息。
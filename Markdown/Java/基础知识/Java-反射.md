---
title: Java 反射
tag: Java

---



**什么是反射？**

反射使程序代码能够接入装载到 JVM 中的类的内部信息，允许在编写与执行时，而不是源代码中选定的类协作的代码，是以开发效率换运行效率的一种手段。

一般情况下，我们使用某个类时，必定知道它是什么类，用来做什么，于是我们直接实例化，之后使用这个类对象进行操作

反射则是一开始并不知道我们要初始化的类对象是什么，自然也无法通过 `new` 关键字来创建对象。

**反射的作用**

1. 实现跨平台兼容，比如 JDK 中的 SocketImpl 的实现
2. 通过 xml 或者注解，实现依赖注入（DI) ，注解处理，动态代理，单元测试等功能。如 Rotifit、 Spring 、Dagger 

**Java Class 的文件结构**

```c
typedef struct {
    u4 magic;
    u2 minor_version;
    u2 major_version;
    u2 constant_pool_count;
    cp_info constant_pool[constant_pool_count - 1 ];
    u2 access_flags;
    u2 this_class;
    u2 super_class;
    u2 interfaces_count;
    u2 interfaces[interfaces_count];
    // 重要
    u2 fields_count;
    field_info fields[field_count];
    // 重要
    u2 methods_count;
    method_info methods[methods_count];
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}ClassBlock
```

**field 字段结构**

```c
typedef struct fieldblock {
    char *name;
    char *type;
    char *signature;
    u2 access_flag;
    u2 constant;
    union {
        union {
            char data[8];
            uintptr_t u;
            long long l;
            void *p;
            int i;
        } static_value;
        u4 offset;
    }u;
}FieldBlock;
```

**method** 

提供了 descriptor, access_flags, Code 等索引，并指向常量池；

```c
method_info {
    u2 access_flags;
    u2 name_index;
    // the paramters that the method takes and the value that it return
    u2 descriptor_index;
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
```



### 类的加载顺序

**ClassLoader：**

 用于加载、连接、缓存 Class，可以通过纯  Java 或者 native 进行实现。在 JVM 的 native 中， ClassLoader 内部维护着一个线程安全的 `HashTable<String, Class>` 用于实现堆 Class 字节流节码后的缓存，如果 `HashTable` 中有缓存，则直接返回缓存；反之，在获得类名后，通过读取文件，网络上的 class 字节流反序列化为 JVM 中的 native 的 C 结构体，接着分配 ( malloc ) 内存，并将指针缓存在 HashTable 中。

**初始化过程**

当 ClassLoader 加载 Class 结束后，将进行 Class 的初始化工作，主要执行 `clinit()> ` 中的静态块与静态属性（取决于编码顺序）

```java
public class Smaple {
    // step 1
    static int b dddddddddddddddddddddddddddddddddddddddddddd= 2;
    // step 2
    static  {
       b = 3; 
    }
    
    public static void main (String[] args) {
        Sample s = new Sample();
        System.out.println(s.b);
        // b = 3
    }
}
```

**Class.forName**

`Class.forName()` 可以通过报名寻找到 Class 对象，比如： `Class.forName("java.lang.String")`

**getDeclaredFields**

`class.getDeclaredFields()` 方法实际调用的是 `native` 方法 `getDeclaredFields0()` 它在  JVM 主要实现步骤如下

1. 根据 Class 结构体信息，获取 `field_count` 和 `fields[]` 字段，这个字段在 load 过程就被放入了
2. 根据 `field_count` 的大小分配内存和创建数组
3. 将数组进行 `forEach` 循环，通过 `fields[]` 中的信息一次创建 Object 对象。
4. 返回数组指针

这个过程比较耗时：

1. 创建、计算、分配数组对象
2. 对字段进行循环赋值

**Method.invoke**

创建 Frame

如果对象 flag 为 native，交给 native_handler 进行处理

在 frame 中执行 Java 代码

弹出 Frame

返回执行结果的指针

主要慢在

1. 需要完全执行 ByteCode 而缺少 JIT 等优化
2. 检查参数非常多，本来可以在编译器或者加载时完成

**class.newInstance**

检测权限，预分配空间大小等参数

创建 Object 对象，并分配空间

通过`Method.invoke()` 调用构造函数

返回 Object 指针

主要慢在：

1. 参数检查不能优化或者一口
2. 构造函数 Method.invoke 本身耗时
---
title: Java 枚举
tag: Java
---



枚举是一种特殊类，他和普通类一样可以使用构造器、定义成员变量和方法，也嫩南瓜实现一个或多个接口，但枚举不能继承其他类。

**使用`enum` 来标识枚举类**

## 特点

1. 必须使用 `enum` 关键字声明
2. 除了初始化，不能通过任何方式手动创建枚举实例
3. 不可以被继承
4. JVM 保证线程安全
5. 无法继承其他类

## 原理分析

**常量枚举**

```Java
public enum Color {
    RED, GREEN, BLUE;
}

public class Test {
    public static void main(String[] args) {
        System.out.println(Color.RED);
    }
}

// 结果
// RED
```

上述代码是枚举的简单使用方法，不能看出枚举的特点和枚举的具体实现。

通过字节码分析 `Color.class`

```java
// final 修饰，不能被继承
public final class Color extends Enum {
        
    // 声明的变量，都对应一个枚举实例对象
    public static final Color RED;
    public static final Color GREEN;
    public static final Color BLUE;
    
    private static final Color $VALUES[];
    
    // 返回原数组的副本，防止数组的修改，引起内部 values 值的改变
    public static Color[] values(){
        return (Color[])$VALUE.clone();
    }
    
    // 按照名字获取枚举实例
    public static Color valueOf(String name) {
        return (Color)Enum.valueOf(com/example/Color, name);
    }
    
    // 私有构造
    private Color(String name, int ordinal) {
        super(name, ordinal);
    }

    
    // 静态初始化
    // 在类加载的 clinit 阶段就被实例化， JVM 能够保证类加载过程的线程安全
    static {
        RED = new Color("RED", 0);
        GREEN = new Color("GREEN", 1);
        BLUE =  new Color("BLUE", 2);
        
        $VALUES = (new Color[] {
            RED, GREEN, BLUE
        });
    }
}

```

从反编译的类中可以看出，`enum` 关键字编写的类，在编译阶段编译器会自动帮外卖生成一份真正在 `jvm` 中运行的代码

`Enum` 类接受一个继承自 `Enum` 的泛型（反编译阶段，`Java`中没有具体体现泛型，是应为泛型在编译阶段就会被 `JVM` 进行泛型擦除，替换为具体实现）

从枚举类以及反编译出来的字节码可以看出，枚举类第一个 `;` 前的变量，都会在字节码中体现为一个 `Color` 实例，且在 `clinit` 静态代码块中进行初始化。而静态块在类加载阶段，`JVM` 会保证枚举对象的线程安全。

生成的 `$VALUES[] ` 可通过 `values()` 方法被外部获取实例。

## 枚举 Enum 类分析

```java
public abstract class Enum<E extends Enum<E>> implements Comparable<E>, Serializable {
        
    private final String name;
    private final int ordinal;
    
    public final int compareTo(E var1) {
        if (this.getClass() != var1.getClass() && this.getDeclaringClass() != var1.getDeclaringClass()) {
            throw new ClassCastException();
        } else {
            return this.ordinal - var1.ordinal;
        }
    }
    
    public final boolean equals(Object var1) {
        return this == var1;
    }

}
```

`Enum` 类实现了 `Comparable` 接口，表明它是支持排序的，实现 `compareTo` ，方法定义为 `final` 且实现以来 `ordinal` 字段也是 `final` 类型，说明只能依据 `ordinal` 排序，排序规则不可变.

**ordinal:** 表示枚举的顺序，从 `Color` 类中可以看出他是从 0 开始自然顺序增长，且其值是 `final` 类型，外部无法改变。

**name:** 表示枚举的名字，它的值就是我们枚举实例的名称（自然，我们也可以通过构造方法进行修改）

**equals():**  使用 `==` 判断两个枚举是否相等

## 每个枚举类型及其定义的枚举变量在 JVM 中都是唯一的

枚举类型它拥有的实例在编写的时候，就已经确定，不能通过其他手段进行创建，且枚举变量在 `JVM` 中有且只有一个对应的实例

*为达到这种效果，枚举通过下面的方式来完成*

1. 类加载时创建，保证线程安全

   枚举对象在静态块中创建，由类加载时进行初始化，`JVM` 保证线程安全，这样就能保证枚举对象 不会因为并发请求同时请求而错误的创建多个实例

2. 对序列化进行特殊处理，防止反序列化时创建对象

   一旦实现 `Serializable` 接口之后，反序列化时每次调用 `readObject()` 方法返回的都是一个新创建出来的对象

   而枚举在序列化时，`Java` 仅仅是将枚举对象的 `name` 属性输出到结果中，反序列化时则是通过枚举的 `valueOf()` 方法来根据名字查找枚举对象。同时，编译器不允许任何对这种序列化进行定制

   ```java
   public static <T extends Enum<T>> T valueOf(Class<T> var0, String var1) {
           Enum var2 = (Enum)var0.enumConstantDirectory().get(var1);
           if (var2 != null) {
               return var2;
           } else if (var1 == null) {
               throw new NullPointerException("Name is null");
           } else {
               throw new IllegalArgumentException("No enum constant " + var0.getCanonicalName() + "." + var1);
           }
       }
   
   private void readObject(ObjectInputStream var1) throws IOException, ClassNotFoundException {
           throw new InvalidObjectException("can't deserialize enum");
       }
   private void readObjectNoData() throws ObjectStreamException {
           throw new InvalidObjectException("can't deserialize enum");
       }
   ```

3. 私有构造函数，无法正常 new 出对象

4. 无法通过 `clone()` 方法， 克隆对象

   ```java
   protected final Object clone() throws CloneNotSupportedException {
           throw new CloneNotSupportedException();
   }
   ```

5. 无法通过反射的方式创建枚举对象

   枚举类型在 `JVM` 层面上，禁止通过反射构造枚举实例的行为，如果尝试通过反射创建，会爆出 `Cannot reflectively create enum objects`

   ```java
   void reflectTest() throws Exception{
       // 获取类对象
       Class<?> cls = Class.forName("com.example.Color");
       // 获取构造函数
       Constructor<?> constructor = cls.getDeclaredConstructor(String.class, int.class);
       // 设置访问权限
       constructor.setAccessible(true);
       // 实例化对象
       Object refObj = constructor.newInstance("name", 0);
   }
   
   // Exception
   Exception in thread "main" java.lang.IllegalArgumentException: Cannot reflectively create enum objects
   ```

   

## 枚举的使用

### 枚举与单例模式

传统的单例模式通过饿汉式、懒汉式、双重检查、内部静态类等方式，都无法完全保证单例在 JVM 中保证唯一

```java
public enum Singleton {
    INSTANCE;
    public void func1(){
        // todo...
    }
}
```

枚举实现的单例，是非常完美和简洁的，但枚举初始化会由时间成本和空间成本。

在 `Android` 设备上，尽量避免选择使用枚举单例（当然现在的设备，已经很优秀了，这一点可以酌情考虑），除了枚举单例还是可以选择 **双重检查锁**，**静态内部类** 的方式实现单例
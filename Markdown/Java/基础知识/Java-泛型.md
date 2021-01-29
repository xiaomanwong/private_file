---
title: Java 泛型
tag: Java
---


泛型，即 **参数化类型**。我们比较熟悉的就是定义方法时有形参，然后调用方法时传递实参。

参数化类型，就是将类型由原来具体的类型参数化，类似于方法中的变量参数，此时类型也定义成参数类型，然后再调用/使用时传入具体的类型。

泛型再使用过程中，操作的数据类型被指定为一个参数，可以用在类、接口和方法中。分别被成为泛型类、泛型接口、泛型方法。

## 三种泛型方式

```java
// 泛型类
public class TypeClass<T> {
    private T data;
    public TypeClass(T data) {
        this.data = data;
    }
}

// 泛型接口
public interface TypeInterface<T> {
    T next();
}

// 泛型方法
// 
public <T> T typeMethod(T t){
    
}
```

## 泛型的作用

1. 使得代码更健壮
2. 代码更简洁
3. 更灵活、可复用

## 限定类型变量

有时候我们需要对类型变量加约束，比如计算量i盎格变量的最大，最小值。

```java
public static <T> T min(T a, T b) {
    if(a.compareTo(b) > 0) 
        return a; 
    else  
        return b;
}
```

那么如上代码，如果我们传入的两个变量没有实现 `Comparable` 会如何呢？那一定是调用不到 `compareTo()` 的，那么我们对其加上约束

```java
public static <T extends Comparable> T min (T a, T b){
    if(a.compareTo(b) > 0) 
        return a; 
    else  
        return b;
}
```

` T extends Comparable` 中，T 表示应该绑定的子类型， `Comparable` 则表示绑定类型，子类型和绑定类型可以是接口也可以是类。

如果我们传入一个没有实现 `Comparable` 接口的实例，则会发生编译错误。

**同时 `extends` 左右都允许有多个，比如 `T, V extends Comparable & serializable` ，限定类型中，只允许有一个类，而且如果有类，必须再限定列表的第一个**

#### 约束和局限性

* 不能使用基本类习数据类型做参数，只能使用包装器类型
* 运行时类型查询只时用于原始类型
* 反射对泛型擦除增加了风险
* 泛型类型中的方法冲突（同名方法，泛型参数做参数变量时，在泛型擦除后，会造成同名方法冲突）
* 静态块/静态方法中不能使用泛型
* 不能创建参数化类型的数组
* 不能实例化类型变量
* 不能捕获泛型类的实例

## 泛型的继承规则

```java
class Employee {}
class Worker exrends Employee{}

class Pair<T> {}

```

泛型类可以继承或者扩展其他泛型类，比如 `List` 和 `ArrayList`

### 通配符

```java
class Fruit {}

class Orange extends Fruit {}

class Apple extends Fruit {}

class HongFuShi extends Fruit{}

public static void println(GenericType<Fruit> p) {
    System.out.println(p.getData().getColor());
}

public void use () {
    GenericType<Fruit> a = new GenericType(); // 可以
    GenericType<Apple> b = new GenericType();// 不允许d 
}
```

因为上面的方案不被 SDK 允许，于是提出了一个通配符类型

* `? extends X` 表示类型的上界，类型参数是 X 的子类
* `? super X` 表示类型的下界，类型参数是 X 的父类

#### ? extends X，可读不可写

表示传递给方法的参数，必须是 X 的子类（包括 X 本身）

```java
public static void println(GenericType<? extends Fruit> p){
    System.out.println(p.getData().getColor());
}
```

但对于泛型类 `GenericType` 来说，如果其中提供了 get 和 set 类型参数变量的方法的话， set 方法是不允许调用的（只能查看，不能修改）

因为 `? extends X` 表示类型的上界，类型参数是 X 的子类，那么可定的说， get 方法返回的一定是 X (不管是 X 还是 X 的子类)，编译器是可以确定知道的。但是 set 方法只知道传入的是个 X，至于具体是哪一个子类，并不知道。

#### ? super X ，可写不可读

表示传递给方法的参数，必须是 X 的父类（包括 X 本身）

```java
public static void println(GenericType<? super Apple> p) {
    System.out.println(po.getData());
}
```

但对于泛型类 `GenericType` 来说，如果其中提供了 get 和 set  类型的变量方法的话，set 方法可以被调用， 且传入的参数只能是 X 或者 X 的子类。

get 方法只返回一个 Object 类型的值。
因为  `? super X` 表示类型的下界，参数类型是 X  的父类（包括其本身）那么可以肯定的说， get 方法返回的一定格式 X 的父类，那么具体是哪个父类，并不知道。但  Object 一定是它的父类，所以 get  方法返回的是一个 Object ，编译器可以确定知道。但是 set 方法，编译器不知道它需要的确切类型，但是 X 和 X 的子类可以安全的转换 X。

### 无限通配符 ?，只是为了说明用法

表示类型没有限制，可以把 `?` 看成所有类型的父类，如： Pair<?>

`ArrayList<T> al = new ArrayList<T>()` 指定集合元素只能是 T 类型

`ArrayList<?> al = new ArrayList<?>()` 集合元素可以是任意类型。

## 虚拟机是如何实现的

Java 语言中的泛型，再程序源码中存在，再编译后的字节码文件中，就已经替换为原来的远程类型（Raw Type）并且再相应的地方插入了强制转换代码，因此对于运行期间的 Java 语言来说，`ArrayList<int>` 与 `ArrayList<String>` 就是同一个类，所以泛型技术实际上是 Java 语言的语法糖， Java 语言中的泛型实现方法成为泛型擦除，基于这种方法实现的泛型称为**伪泛型**

## 泛型擦除

因为虚拟机实现原理，就是泛型擦除，因此 **泛型信息只能存在于代码的编译阶段，编译成子接码之后，与类型相关的信息会被擦除掉，变为 Object**

**步骤**

1. 检查泛型类型，获取目标泛型
2. 擦除类型变量，并替换为限定类型
   1. 如果泛型类型的类型变量没有限定`<T>` 则用 Object 原始类型表示
   2. 如果有限定类型`<T extends XClass> `则用，`XClass` 作为原始类型
   3. 如果有多个限定`<T extends XClass & XClass2>` 则使用第一个作为原始类型
3. 在必要时插入类型转换以保证类型安全
4. 生成**桥方法** 以再扩展时保持多态


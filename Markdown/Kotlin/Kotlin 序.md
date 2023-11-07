# Kotlin 序


## Kotlin 难在哪里?

* **不变性思维**，Java 也有 final 不变性；但 Kotlin 要求我们在定义一个变量的、集合的时候，就明确规定它的不变性。设计上希望在程序当中尽可能的消灭可变性。
* **空安全思维**，Kotlin 的类型系统分为可空和不可空类型。
* **表达式思维**，Kotlin 中，if else when 之类的语句，还能作为表达式来使用，语法特性可以帮助我们简化代码逻辑
* **函数思维**，Kotlin 中，函数是一等公民，Kotlin 也是一门积极拥抱函数式编程的语言，在一些语法设计上，能够看到函数的影子。命令式编程与函数式编程各有优缺点，也有各自擅长的领域。
* **协程思维**，Java 开发者是“线程思维”，对协程不解。想要真正地理解和掌握 Kotlin 的协程，我们需要从根本上改变我们脑子里的思维模型。



![Img](https://static001.geekbang.org/resource/image/f6/9d/f65548f66702b86a7aa4433aeeea319d.jpg?wh=1920x1315)
![Img](https://static001.geekbang.org/resource/image/32/67/32ab3d37cd7f9650f4cba17736305c67.jpg?wh=1920x1983)
![Img](https://static001.geekbang.org/resource/image/21/bf/21080a921b3aa73872bfd55f7c1cddbf.jpg?wh=1920x911)
![Img](https://static001.geekbang.org/resource/image/d6/0f/d67630808ee59a642b93d955ae8fa60f.jpg?wh=1920x1480)
![Img](https://static001.geekbang.org/resource/image/fd/24/fdfbcf0b8a293acc91b5e435c99cb324.jpg?wh=2000x1074)
![Img](https://static001.geekbang.org/resource/image/02/34/02702d48a28378817ed1598849bfbb34.jpg?wh=1920x912)
![Img](https://static001.geekbang.org/resource/image/cc/67/cc75cc62f08d1b4f2e604630499f8b67.jpg?wh=1920x1260)
![Img](https://static001.geekbang.org/resource/image/b4/10/b4a3ce7c3e0b2228161faa4769618a10.jpg?wh=1999x1333)



## Kotlin 语言特性
 * 支持类型推导
 * 代码末尾不需要分号
 * 字符串模版
 * 原始字符串，支持复杂文本格式
 * 单一表达式函数，简介且符合直觉
 * 函数支持参数默认值，替代 Builder 模式的同时，可读性还很强
 * if 和 when 可作为表达式
 * 强制区分“可空变量类型”和“不可空变量类型”，规避空指针异常
 * 推崇不可变性（val），对于没有修改需求的变量，IDE 会智能提示开发者将 var 改为 val
 * 基础类型不支持隐式类型转换，这样避免很多隐藏问题
 * 数组的访问行为和集合统一，不会出现 array.length, list.size 的情况
 * 函数调用自持命名参数，提高可读性，在后续维护代码的时候不容易出错
 * when 表达式，强制要求逻辑分支完整，写出来的逻辑永远不会有漏洞
 * 




```kotlin
// 变量在
    // Java/C 当中，如果我们要声明变量，我们必须要声明它的类型，后面跟着变量的名称和对应的值，然后以分号结尾。就像这样：
    // 变量声明
    // 关键字， 变量名，变量类型，变量值
    var price: Int = 100
    // Kotlin 支持类型推导，大部分情况下，变量类型可以省略不写
    var price2 = 1200

    // var(Variable) 可变变量
    // val(value) 不可变变量， 等价于 Java 中的 final ,它的值在初始化以后就无法再次被修改
    println(price)

    // 基本类型
    // 包括我们常见的数字类型、布尔类型、字符类型，以及前面这些类型组成的数组。这些类型是我们经常会遇到的概念，因此我们把它统一归为“基础类型”。
    // 在 Java 里面，基础类型分为原始类型（Primitive Types）和包装类型（Wrapper Type）。比如，整型会有对应的 int 和
    // Integer，前者是原始类型，后者是包装类型。
    // Java 之所以要这样做，是因为原始类型的开销小、性能高，但它不是对象，无法很好地融入到面向对象的系统中。而包装类型的开销大、性能相对较差，但它是对象，可以很好地发挥面向对象的特性。在
    // JDK 源码当中，我们可以看到 Integer 作为包装类型，它是有成员变量以及成员方法的，这就是它作为对象的优势。
    // 然而，在 Kotlin 语言体系当中，是没有原始类型这个概念的。这也就意味着，在 Kotlin 里，一切都是对象。
    // https://static001.geekbang.org/resource/image/yy/3b/yyd95b04616943878351867c4d1e063b.jpg?wh=2000x1077
    // Double: 64bit, Float: 32bit, Long: 64bit, Int: 32bit, Short: 16bit, Char: 16bit, Byte: 8bit,
    // Boolean: 8bit
    // 可以发现，由于在 Kotlin 中，整型数字“1”被看作是对象了，所以我们可以调用它的成员方法 toDouble()，而这样的代码在 Java 中是无法实现的。
    val i: Double = 1.toDouble()

    // 空安全
    // Kotlin 中一切皆对象，那么对象就有可能空，
    // val i1: Double = null // 编译器会报错 ==>  error: null can not be a value of a non-null type Double
    // Kotlin 强制要求开发者在定义变量的时候，指定这个变量是否可能为 null。对于可能为 null 的变量，我们需要在声明的时候，在变量类型后面加一个问号“?”
    val i2: Double? = null

    // "可能为空" 的变量，无法直接赋值给 "不可为空的变量",反向赋值是可以的
    var i22: Double = 1.0
    var j: Double? = null

    if (j != null) {
        i22 = j // 编译通过
    }

    // 数字类型
    val int = 1 // 整数默认被推导为 Int 类型
    val long = 12345678L // Long 需要后缀 L
    val double = 13.15 // 小数默认推导为 Double
    val float = 13.41f // Float 需要使用 F 后缀
    val hexadecimal = 0xAF // 0x 代表十六进制面量
    val binary = 0b01010101 // 0b 代表二进制面量

    // 布尔类型
    // true 和 false。布尔类型支持逻辑操作
    // & 代表 与运算
    // | 代表 或运算
    // ! 代表 非运算
    // && 和 || 分别代表 短路逻辑运算
    val k = 1
    val m = 2
    val n = 3

    val isTrue = k < m && m < n

    // 字符 Char
    // Char 代表单个字符 比如'A'、'B'、'C'，字符应该用单引号括起来

    val c: Char = 'A'
    val i3: Int = c.toInt() // 编译器报错

    // 字符串：String
    // 字符串（String），顾名思义，就是一连串的字符。和 Java 一样，Kotlin 中的字符串也是不可变的。在大部分情况下，我们会使用双引号来表示字符串的字面量，这一点跟 Java
    // 也是一样的。
    val s = "Hello Kotlin!"
    // Kotlin 还为我们提供了非常简洁的字符串模板
    val name = "Kotlin"
    print("Hello $name!")
    /*            ↑
        直接在字符串中访问变量
    */
    // 输出结果：
    // Hello Kotlin!

    val array = arrayOf("Java", "Kotlin")
    print("Hello ${array.get(1)}!")
    /*            ↑
        复杂的变量，使用${}
    */
    // 输出结果：
    // Hello Kotlin!

    // 原始字符串
    // 是用三个引号来表示的。它可以用于存放复杂的多行文本，并且它定义的时候是什么格式，最终打印也会是对应的格式。所以当我们需要复杂文本的时候，就不需要像 Java 那样写一堆的加号和换行符了。

    val originString = """
    当我们的字符串有复杂的格式时
    原始字符串非常的方便
    因为它可以做到所见即所得。 """
    print(originString)

    // 数组
    // 在 Kotlin 当中，我们一般会使用 arrayOf() 来创建数组，括号当中可以用于传递数组元素进行初始化，同时，Kotlin 编译器也会根据传入的参数进行类型推导

    val arrayInt = arrayOf(1, 2, 3) // 推导为 int 数组
    val arrayString = arrayOf("apple", "pear")  // 推导为字符串数组



     // 函数声明

    /*
    关键字    函数名          参数类型   返回值类型
    ↓        ↓                ↓       ↓      */
    fun helloFunction(name: String): String {
        return "Hello $name !"
    }
    /*   ↑
    * 花括号内为：函数体
    */
    /*
    * 可以看到，在这段代码中：
    * 使用了 fun 关键字来定义函数；函数名称，使用的是驼峰命名法（大部分情况下）；
    * 函数参数，是以 (name: String) 这样的形式传递的，这代表了参数类型为 String 类型；
    * 返回值类型，紧跟在参数的后面；
    * 最后是花括号内的函数体，它代表了整个函数的逻辑。
    */

    // 函数体实际上只有一行代码。那么针对这种情况，我们其实就可以省略函数体的花括号，直接使用“=”来连接，将其变成一种类似变量赋值的函数形式, 
    // 这种写法，我们称之为单一表达式函数。由于 Kotlin 支持类型推导，我们在使用单一表达式形式的时候，返回值的类型也可以省略.
    fun helloFunction2(name: String): String = "Hello $name !"


    // 流程控制
    // if when for while

    // if
    // if 语句，在程序当中主要是用于逻辑判断。Kotlin 当中的 if 与 Java 当中的基本一致：
    val i23 = 1
    if (i23 > 0) {
        print("Big")
    } else {
        print("Small")
    }
    // 输出结果：
    // Big

    // 不过 Kotlin 的 if，并不是程序语句（Statement）那么简单，它还可以作为表达式（Expression）来使用
    val i24 = 1
    val message = if (i24 > 0) "Big" else "Small"

    print(message)

    // 输出结果：
    // Big

    // Elvis 表达式, 简化 if else 逻辑判断。
    fun getLength(text: String?): Int {
        return text?.length ?: 0
    }

    // when
    // when 语句，在程序当中主要也是用于逻辑判断的。当我们的代码逻辑只有两个分支的时候，我们一般会使用 if/else，而在大于两个逻辑分支的情况下，我们使用 when。

    val i31: Int = 1

    when(i31) {
        1 -> print("一")
        2 -> print("二")
        else -> print("i 不是一也不是二")
    }

    // 输出结果：
    // 一

    // when 语句有点像 Java 里的 switch case 语句，不过 Kotlin 的 when 更加强大，它同时也可以作为表达式，为变量赋值

    val i32: Int = 1

    val message32 = when(i32) {
        1 -> "一"
        2 -> "二"
        else -> "i 不是一也不是二" // 如果去掉这行，会报错
    }

    print(message32)
    // 另外，与 switch 不一样的是，when 表达式要求它里面的逻辑分支必须是完整的。举个例子，以上的代码，如果去掉 else 分支，编译器将报错，原因是：i 的值不仅仅只有 1 和 2，这两个分支并没有覆盖所有的情况，所以会报错。

    // 循环迭代：while 与 for
    // 首先 while 循环，我们一般是用于重复执行某些代码，它在使用上和 Java 也没有什么区别
    // 在 Java 当中，for 也会经常被用于循环，经常被用来替代 while。不过，Kotlin 的 for 语句更多的是用于“迭代”。比如，以下代码就代表了迭代 array 这个数组里的所有元素，程序会依次打印出：“1、2、3”。
    val array31 = arrayOf(1, 2, 3)
    for (i33 in array31) { println(i33)}
    // 而除了迭代数组和集合以外，Kotlin 还支持迭代一个“区间”。
    //首先，要定义一个区间，我们可以使用“..”来连接数值区间的两端，比如“1..3”就代表从 1 到 3 的闭区间，左闭右闭
    val oneToThree = 1..3 // 代表 [1, 3]
    // 甚至，我们还可以逆序迭代一个区间，比如：

    for (i34 in 6 downTo 0 step 2) {
        println(i34)
    }
    // 输出结果：
    // 6
    // 4
    // 2
    // 0
    // 以上代码的含义就是逆序迭代一个区间，从 6 到 0，每次迭代的步长是 2，这意味着 6 迭代过后，到 4、2，最后到 0。需要特别注意的是，逆序区间我们不能使用“6..0”来定义，如果用这样的方式来定义的话，代码将无法正常运行。
```

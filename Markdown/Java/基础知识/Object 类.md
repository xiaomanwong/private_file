# Object 类

* Object 类是所有 Java 类的父类。每个类都使用  Object 作为 super 类，所有对象都实现这个类的方法

* 可以使用 Object 类型的变量指向任意类型的 super 类
* Object 类有一个默认构造方法 `public Object()` ，在构造子类实例时，都会先调用这个默认构造方法
* Object 类的变量只能用作各种值得通用持有者。要对他们进行任何专门操作，都需要知道他们得原始类型并进行转换

## API 

* Object () ： 默认构造方法
* clone() : 创建并返回此对象得一个副本
* equals(Object obj) :  指示某个其他对象是否与此对象相等（Object 判断的是内存地址）
* finalize() : 当垃圾回收器确定不存在该对象得更多引用时，由对象得垃圾回收器调用此方法
* getClass(): 返回一个对象得运行时类
* hashCode(): 返回该对象得 哈希值
* notify(): 唤醒在此对象监视器上等待得单个线程
* notifyAll() : 唤醒在此对象监视器上等待得所有线程
* toString(): 返回该对象得字符串标识
* wait(): 导致当前的线程等待，知道其他线程调用此对象的 notify 方法或 notifyAll() 方法
* wait(long timeout): 导致当前线程等待，直到其他线程调用此对象的 notify() 或 notifyAll() 方法，或者超过指定的时间量
* wait(long timeout, int nanos): 导致当前的线程等待， 直到其他线程调用此对象的 notify() 方法或 notifyAll() 方法， 或者其他某个线程中断当前线程， 或者已超过某个实际时间量  


# kotlin 修饰符


```kotlin
public / protected / private / internal
expect / actual
final / open / abstract / sealed / const
external
override
lateinit
tailrec
vararg
suspend
inner
enum / annotation / fun // 在 `fun interface` 中是修饰符
companion
inline
infix
operator
data
```
## 可见性修饰符

- private 只能类内部访问
- protected 和 private 一样 + 子类中可见
- internal 能见到类声明的本模块内的任何客户端可见其 internal 成员
- public 能见到类声明的任何客户端都可见其 public 成员
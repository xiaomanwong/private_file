# Flow

1. 冷流（只有消费时，才会生产数据）
1. 最小化协程依赖，结构化并发，上下文保护
1. 数据流串联

```kotlin
// 高阶函数
fun <T> flow(block: suspend FlowCollector<T>.() -> Unit): Flow
<T> = SafeFlow(block)


interface Flow<T> {
    fun collect(collector: FlowCollector)
}

class SafeFlow:  AbstractFlow<T> {

}

class AbstractFlow: Flow<T> {

}
```




## 操作符

filter: 过滤

map: 转换

take: 取值


# GooglePlay内购研发接入文档

## 添加依赖库
如需集成 Google Play 结算系统，需先在应用中添加对 Google Play 结算库的依赖。用于链接到 Google Play 的 API。
```kotlin
dependencies {
    val billing_version = "5.0.0"
    implementation("com.android.billingclient:billing:$billing_version")
}
```



# GooglePlay内购研发接入文档

> 介绍如何将 Google Play 结算库集成到应用中, 开始销售商品



## 提纲

* 介绍主要功能类的作用
* 介绍业务场景的实例创建
* 依照实际业务场景,绘制支付流转图
* 如有陌生名词,需进行解析

## 核心功能类介绍

* `BillingClient`  是 Google Play 结算库与应用进行通信的主接口
* `PurchaseUpdatedListener` 可接收应用中所有购买交易的更新
* `BillingResult` 通信结果,包含错误信息 `BollingResponseCode`
* `BillingClientStateListener` 链接 Google Play 状态监听
* `ProductDetailsResponseListener` 商品详情回调监听
* `QueryProductDetailsParams` 查询商品实例,针对管理中心内创建的商品
* `ProductDetails` 商品详情
* `PurchasesUpdatedListener` 支付结果回调监听

## 权限

`BILLING`

## 初始化与 Google Play 的连接


**交易流程概览**

![Img](/Markdown/调研/FILES/GooglePlay内购研发接入文档.md/img-20220823153939.png)


### 添加依赖库

如需集成 Google Play 结算系统，需先在应用中添加对 Google Play 结算库的依赖。用于链接到 Google Play 的 API。

```kotlin
dependencies {
    val billing_version = "5.0.0"
    implementation("com.android.billingclient:billing:$billing_version")
    // ktx 扩展库
    implementation "com.android.billingclient:billing-ktx:$billing_version"
}
```

### 初始化 BillingClient

初始化实例 `BillingClient` 实例.此对象是 Google Play 结算库与应用进行通信的主接口. `BillingClient` 提供了很多方便的方法,包含同步和异步操作.

官方建议一次打开一个 `BillingClient` 连接,避免对某一个时间多次`PurchasesUpdatedListener` 回调.

```kotlin
private val purchasesUpdatedListener =
   PurchasesUpdatedListener { billingResult, purchases ->
       // To be implemented in a later section.
   }
// 通过 newBuilder 方式创建 BillingClient
private var billingClient = BillingClient.newBuilder(context)
   .setListener(purchasesUpdatedListener)
   .enablePendingPurchases()
   .build()

```



### 链接到 Google Play

`startConnection()` 后,需要监听 `BillingClientStateListeneer`以获取请求回调.

```kotlin
billingClient.startConnection(object : BillingClientStateListener {
    override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode ==  BillingResponseCode.OK) {
            // The BillingClient is ready. You can query purchases here.
        }
    }
    override fun onBillingServiceDisconnected() {
        // Try to restart the connection on the next request to
        // Google Play by calling the startConnection() method.
    }
})
```

### 展示可购买的商品

查询可销售的商品并展示给用户

`queryProductDetailsAsync()` 异步查询本地化商品信息

ProductType.INAPP (针对一次性商品信息), ProductType.SUBS(针对订阅商品)

```kotlin
val queryProductDetailsParams =
    QueryProductDetailsParams.newBuilder()
        .setProductList(
            ImmutableList.of(
                Product.newBuilder()
                    .setProductId("product_id_example")
                    .setProductType(ProductType.SUBS)
                    .build()))
        .build()

billingClient.queryProductDetailsAsync(queryProductDetailsParams) {
    billingResult,
    productDetailsList ->
      // check billingResult
      // process returned productDetailsList
}
```

### 处理查询结果

`ProductDtails` 为查询返回的结构.可对每个对象调用方法,查看商品内的相关信息,如价格或说明.

在提供商品前,需要先检查用户是否拥有该商品.如果用户的消耗性商品仍在他们的商品库中,必须先消耗掉该商品,然后才能购买.

在提供订阅之前,验证用户是否尚未订阅.还应注意以下事项:

1. `queryProductDetailsAsync()`会返回订阅的商品详情,并且每项订阅最多包含 50 个优惠
2. `queryProductDetailsAsync()`仅返回用户有资格享受的优惠.如果用户尝试购买没有资格的优惠(如,应用显示的是过期的优惠列表),Play 会通知用户他们不符合优惠条件,并且用户可以改为选择购买基础方案.

## 开始购买流程

应用从主线程调用 `billingClient.launchBillingFlow()` 方法.

```kotlin
// An activity reference from which the billing flow will be launched.
val activity : Activity = ...;

val productDetailsParamsList = listOf(
    BillingFlowParams.ProductDetailsParams.newBuilder()
        // retrieve a value for "productDetails" by calling queryProductDetailsAsync()
        .setProductDetails(productDetails)
        // to get an offer token, call ProductDetails.subscriptionOfferDetails()
        // for a list of offers that are available to the user
			  // 优惠信息,可不传
        .setOfferToken(selectedOfferToken)
        .build()
)

val billingFlowParams = BillingFlowParams.newBuilder()
    .setProductDetailsParamsList(productDetailsParamsList)
    .build()

// Launch the billing flow
val billingResult = billingClient.launchBillingFlow(activity, billingFlowParams) 
```

`launchBillingFlow()`返回 `BillingClient.BillingResponseCode` ,需检查结果,确保购买流程没有错误.

<img src="https://developer.android.com/static/images/google/play/billing/purchase-screen.png" width="420" height="780" alt="拉起 Google Play 支付">

**ResponseCode Table**
| code | value | 
| -- | -- |
| SERVICE_TIMEOUT | -3 |
|FEATURE_NOT_SUPPORTED|-2|
|SERVICE_DISCONNECTED|-1|
|OK|0|
|USER_CANCELED|1|
|SERVICE_UNAVAILABLE|2|
|BILLING_UNAVAILABLE|3|
|ITEM_UNAVAILABLE|4|
|DEVELOPER_ERROR|5|
|ERROR|6|
|ITEM_ALREADY_OWNED|7|
|ITEM_NOT_OWNED|8|

通过 `PurchasesUpdatedListener`回调`onPurchasesUpdated()` 将操作结果回传给客户端.

```kotlin
override fun onPurchasesUpdated(billingResult: BillingResult, purchases: List<Purchase>?) {
   if (billingResult.responseCode == BillingResponseCode.OK && purchases != null) {
       for (purchase in purchases) {
           handlePurchase(purchase)
       }
   } else if (billingResult.responseCode == BillingResponseCode.USER_CANCELED) {
       // Handle an error caused by a user cancelling the purchase flow.
   } else {
       // Handle any other error codes.
   }
}
```

如果购买成功,示意图:

<img src="https://developer.android.com/static/images/google/play/billing/purchase-success.png?hl=zh-cn" width="420" height="780" alt="购买成功示意图">

购买成功后,系统生产购买令牌(一个唯一标识符),表示用户及所购商品的商品 ID.此 ID 需上传给后端服务器存储及校验购买交易和防欺诈行为.

消费用户会收到包含收据的电子邮件,其中包含订单 ID 或交易唯一 ID.用户没购买一次性商品时,都会收到电子邮件.订阅类商品也会收到邮件.可以在 Google Play 管理中心内使用订单 ID 来管理退款.



### 订单状态流转
![Img](
    https://p5.music.126.net/obj/wonDlsKUwrLClGjCm8Kx/13211034378/455e/3689/d4d5/3a169de7485c7e2bdced5c2631fe708e.png
)

![Img](/Markdown/调研/FILES/GooglePlay内购研发接入文档.md/img-20220822171810.png)

### 支付结构设计
![Img](/Markdown/调研/FILES/GooglePlay内购研发接入文档.md/img-20220823090021.png)接口层：支付组件对外提供的能力，支付发起和订单补偿
管理层：控制器下有数据管理和连接管理。数据管理是管理订单和商品相关的数据；连接管理是管理 Google 提供的 BillingClient，断开连接等。
核心层：处理业务的核心逻辑，包括建立连接、获取商品等。并包含日志监控。
支撑层：依托于 APP 现有的底层基础能力。


## 支付与 web3 的关系

根据真是业务场景，使用 Google Play 内购的方式，是在向啫喱 APP 充值**啫喱积分**，发生支付的行为属于 web2 逻辑。与传统的充值业务属于一个类型。

经济系统中的 web3 钱包，是在用户使用**啫喱积分**进行交易的行为。
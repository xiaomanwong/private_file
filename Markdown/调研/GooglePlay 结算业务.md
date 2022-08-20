# GooglePlay 结算业务

[toc]{type: "ul", level: [2,3,4]}

## 提纲：

1. in-app 内购名词解析
1. 前期准备
1. 支付流程图
1. 横向业务对比（常规，国内支付流程）
1. 结算
1. 退款
1. 介入流程
1. 实时开发者通知

## 名词解析

### In-app purchase 
**app 内购**： 用来在系统生态内购买 app 相关产品的功能。每一笔交易会提取固定的手续费。内购的商品一般指虚拟商品或服务。

### 内购商品分类
* 消耗性商品：只可使用一次的产品，使用后立即失效，必须再次购买，如：游戏币，虚拟道具
* 非消耗性商品：只需购买一次，不会过期或随着使用而减少的商品，如：电子书
* 自动续期订阅：允许用户在固定时间段内购买动态内容的产品。除非用户选择取消，否则此类订阅会自动续期，如：Apple Music这类按月订阅的商品，会员服务等。
* 非续期订阅：允许用户购买有时限性服务的产品，此 App 内购买项目的内容可以是静态的。此类订阅不会自动续期。

## 前期准备
在应用中销售商品之前，需要创建开发者账号、创建和配置要销售的商品，以及启用和配置用于销售和管理商品的 API。

### 设置 Google Play 开发者账号
> 部分和财务相关
* 在 [Google Play 管理中心](https://developer.android.google.cn/distribute/console) 中设置 [Google Play 开发者账号](https://support.google.com/googleplay/android-developer/answer/6112435)
* [Google Play 管理中心](https://developer.android.google.cn/distribute/console) 用来管理和结算相关的商品和设置
* [Google 付款中心](https://pay.google.com/) 设置付款资料，**并与 Google Play 开发者账号关联**

### 在 Google Play 中启用结算功能

设置好开发者账号后，必须发布包含 Google Play 结算库的应用版本。

#### 添加依赖库

[Google Play In-app Purchase 研发接入文档](./GooglePlay内购研发接入文档.md)

#### 上传应用

将该库添加到您的应用后，构建并发布您的应用。在此步骤中，创建您的应用，然后将其发布到任何轨道，包括内部测试轨道。

### 创建和配置商品
启动结算服务功能后，需要配置要销售的商品.

创建商品需要为每个商品提供唯一的商品 ID、商品名、说明和定价信息。
订阅服务类，如需定期、您是否提供免费试，已经订阅是否有初次体验优惠。

Google Play 提供了可用于管理商品的网页界面,
* [创建受管理的商品](https://support.google.com/googleplay/android-developer/answer/1153481)， Google Play 管理中心将一次性商品称为“受管理商品”
*[创建订阅商品](https://support.google.com/googleplay/android-developer/answer/140504?hl=zh-CN&ref_topic=3452890)

可使用 Google Play Developer API（服务器到服务器的 API） 中的[inappproducts](https://developers.google.cn/android-publisher/api-ref/rest/v3/inappproducts) REST 资源管理商品。

### Google Play Developer API 

服务器到服务器的 API，与 Android 平台的 Google Play 结算库相辅相成。提供了如安全验证够爱交易以及为用户办理退款。

Google Play 结算系统集成后，必须通过 Google Play 管理中心配置对 Google Play Developer API 的访问权限，确保已授予**查看财务数据**权限，[添加开发者账号用户并管理权限](https://support.google.com/googleplay/android-developer/answer/2528691)

### 配置实时开发者通知
实时开发者通知（RTDN）机制，当用户权益发生变化时，会收到 Google 的通知。允许立即对订阅状态做出反应。
此通知只会告知购买状态发生了变化，不会提供有关购买交易的完整信息。可通过调用[Google Play Developer API](https://developers.google.cn/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2/get) 来获取完整状态并更新自己的后端状态。

#### 确定定价和配额

[定价和配额相关文档](https://cloud.google.com/pubsub/pricing)




---
APP 合规检测
tag： Android
category: 三方框架
---

## **背景**

依据《中华人民共和国国家安全法》《中华人民共和国网络安全法》《中华人民共和国数据安全法》等法律法规，网信办同有关部门修订了《网络安全审查办法》。

根据《网络安全审查办法》介绍，网络安全审查重点评估采购活动、数据处理活动以及国外上市可能带来的国家安全风险，主要考虑因素有：核心数据、重要数据或大量个人信息别窃取、泄漏、毁损以及分发利用或出境的风险；国外上市后关键信息基础设施，核心数据、重要数据或大量个人信息被国外政府影响、控制、恶意利用风险等。

[《关于侵害用户权益行为的APP通报》](https://www.miit.gov.cn/jgsj/xgj/gzdt/art/2021/art_8eada0a58662420e816487ceded5d3fa.html)

[《工业和信息化部关于开展纵深推进APP侵害用户权益专项整治行动的通知》](https://www.miit.gov.cn/jgsj/xgj/gzdt/art/2020/art_c5f69af7882247198657b2ac6777ad62.html)

[《App违法违规收集使用个人信息行为认定方法》](https://link.juejin.cn/?target=https%3A%2F%2Fwww.miit.gov.cn%2Fjgsj%2Fwaj%2Fwjfb%2Fart%2F2020%2Fart_8663d2afe61b40c3beb7c65bf6ec2a64.html)



**滴滴事件**

2020 年 7 月 9 日，国家网信办发布通报成，“滴滴企业版”等 25 款 APP 存在严重违法违规收集使用个人信息问题，网信办通知应用商店下架 25 款 app。

值得注意的是，滴滴、满帮集团、BOSS直聘都是今年6月份在美国上市，被实施网络安全审查后，股价均遭遇大跌。

掌握超100万用户个人信息的运营者赴国外上市，必须申报网络安全审查。

![](https://n.sinaimg.cn/spider2021710/749/w1080h2069/20210710/7830-ksmehzt1663026.png)

**欧盟 GDPR**

欧盟的《一般资料保护规范》（GDPR）已取代了原先的欧盟《个人资料保护纲领》(Directive 95/46/EC)，其旨在协调欧洲各国的个人资料保密法令，从而对所有欧盟公民的个人资料隐私进行保护和赋权，重塑地区内机构实施数据保密的方式。

GDPR极大改变了欧盟的资料保护监管样貌，其设定了更为严格的要求，涵盖了更多的公司，并实施更为严厉的惩罚。所有公司必须实施以下规定

- 实施计划性的措施来确保合规性，并积极加以展示
- 在设计处理系统和处理资料时，采取恰当的技术和组织措施以确保个人资料得到保护
- 在进行高风险数据处理的运作时，必须作出数据保护影响评估
- 在任何情况下均需要设计和实施有效措施以保护隐私
- 实行资料泄漏通告

**Google**

[Android 10 中隐私权限变更](https://developer.android.google.cn/about/versions/10/privacy/changes?hl=zh-cn)

* Android M 增加隐私权限动态申请
* Android 10 沙盒访问机制；后台运行时访问设备位置权限
* Android 12 增加隐私控制面板，推出隐私计算核心技术
* 拆分原权限组，不断细化隐私权限
* 限制 Ads ID 追踪
* 移除了联系人亲密程度信息
* 对不可重置的设备标识符实施了限制
* 限制了对剪贴板数据的访问权限
* 保护 USB 设备序列号
* ...

## 解决方案

### 痛点

* 基于目前 App、SDK 等产品不断迭代、积累、人员流动等因素，导致代码**维护难**，**检索难**，**定位难**

* 政策的变化、Google 对权限的限制以及更新等因素对合规检测的困难不断增加

* 互联网的高速发展，用户对隐私数据的认知不断提升

**Cannibal**

基于 aapt，apktool，keytool 工具，通过 Python 实现对 apk、aar、jar 等 Android 二进制产物进行扫描及安全检查。大致工作流程：

![工作流程图](https://i.loli.net/2021/11/11/hqbC7n2JaHioWrF.png)

主要对 Android 产物中最终要的字节码进行扫描，基于 `apktool` 反编译得到 `smail` 文件，先反编译，然后逐行对 `smail` 文件进行扫描，并检查是否存在合规问题。

**smail** 示意图

```smail
.class public final Lcom/getui/gtc/dim/c/a;
.super Ljava/lang/Object;
.source "SourceFile"


# static fields
.field public static final a:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field public static final b:Landroid/content/BroadcastReceiver;

.field public static final c:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field public static final d:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map<",
            "Ljava/lang/String;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field
```

`smail` 扫描流程

![smail 扫描流程](https://i.loli.net/2021/11/11/ey6fdAtuPmlwn7E.png)

**packinfo check**

`aapt dump badging xxx.apk`

```
> admin$ tools/adb/aapt-mac/aapt dump badging ./resource/yidian-yidian-release.apk
> package: name='com.hipu.yidian' versionCode='59600' versionName='5.9.6.0'
> sdkVersion:'21'
> targetSdkVersion:'26'
```

**permission check**

`aapt d permissions xxx.apk`

```
admin$ tools/adb/aapt-mac/aapt dump permissions ./resource/yidian-yidian-release.apk
package: com.hipu.yidian
uses-permission: name='android.permission.CHANGE_WIFI_STATE'
uses-permission: name='android.permission.CHANGE_NETWORK_STATE'
permission: com.hipu.yidian.permission.JPUSH_MESSAGE
uses-permission: name='android.permission.INTERACT_ACROSS_USERS_FULL'
uses-permission: name='android.permission.ACCESS_WIFI_STATE'
uses-permission: name='android.permission.INTERNET'
uses-permission: name='android.permission.READ_PHONE_STATE'
uses-permission: name='android.permission.GET_TASKS'
uses-permission: name='android.permission.ACCESS_NETWORK_STATE'
uses-permission: name='android.permission.INTERNET'
uses-permission: name='android.permission.READ_PHONE_STATE'
uses-permission: name='android.permission.WRITE_EXTERNAL_STORAGE'
uses-permission: name='android.permission.ACCESS_NETWORK_STATE'
uses-permission: name='android.permission.ACCESS_WIFI_STATE'
uses-permission: name='android.permission.WRITE_SETTINGS'
uses-permission: name='android.permission.AUTHENTICATE_ACCOUNTS'
uses-permission: name='android.permission.INTERNET'
```

**API check**

```json
{
    "name": "获取imei",
    "summary": "sdk获取imei信息，需谨慎处理，否则APP可能被要求整改",
    "desc": "1.工信部要求2.android10及以上获取不到了3.imei权限部分需要注意兼容",
    "javacode": "",
    "smalicode": {
      "0": "Landroid/telephony/TelephonyManager;->getDeviceId()Ljava/lang/String",
      "1": "Landroid/telephony/TelephonyManager;->getImei(I)Ljava/lang/String",
      "2": "Landroid/telephony/TelephonyManager;->getDeviceId(I)Ljava/lang/String"
    },
    "level": "2",
    "sol": "联系sdk开发负责人或针对此进行处理，说明使用原因。工信部要求，不得向第三方提供用户设备IMEI号、地理位置等个人信息，及sdk不得私自传输。若必须，请经用户同意，且做匿名化处理，并附有隐私政策说明。且若用户拒绝，不能影响app正常业务使用。"
  }
```

**Report**

```xml
<api>
<name>获取android id</name>
<summary>sdk获取android id信息，需谨慎处理，否则APP可能被要求整改</summary>
<desc>1.工信部要求，android id也属于个人信息，2.厂商定制系统的Bug：不同的设备可能会产生相同的ANDROID_ID 3.厂商定制系统的Bug：有些设备返回的值为null。 设备差异：对于CDMA设备，ANDROID_ID和TelephonyManager.getDeviceId() 返回相同的值。</desc>
<code>invoke-static {p1, v1}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p1, v2}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v0}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p1, v1}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {v1, v2}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v1}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v2}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v0}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v0}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {v1, v2}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<code>invoke-static {p0, v1}, Landroid/provider/Settings$Secure;-&lt;getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;</code>
<classname>/tr.smali</classname>
<classname>/tr.smali</classname>
<classname>/tt.smali</classname>
<classname>/vr.smali</classname>
<classname>/cn/jiguang/verifysdk/h/a/a.smali</classname>
<classname>/cn/jiguang/f/a.smali</classname>
<classname>/cn/com/chinatelecom/account/api/e/d.smali</classname>
<classname>/android/support/v4/app/NotificationManagerCompat.smali</classname>
<classname>/com/getui/gtc/dim/c/a.smali</classname>
<classname>/com/bytedance/embedapplog/am.smali</classname>
<classname>/com/bytedance/sdk/openadsdk/core/j.smali</classname>
<level>1</level>
<slu>联系sdk开发负责人或针对此进行处理，说明使用原因。工信部要求，不得向第三方提供用户设备IMEI号、地理位置等个人信息，及sdk不得私自传输。若必须，请经用户同意，且做匿名化处理，并附有隐私政策说明。且若用户拒绝，不能影响app正常业务使用。</slu>
</api>
```

## 收益

1. 覆盖 Android 端代码合规检测

   基于 apk， aar，jar 包，通过反编译手段覆盖包体积内全部源码，通过配置文件，对包内全部文件扫描，精准定位不合规 API 的使用，隐私权限的获取等，辅助工程师在茫茫码海中快速定位不合规问题和三方 SDK 使用场景。

2. 可扩展性

   基于配置文件，可动态配置新增合规规范，安全漏洞规范，敏感词汇规范及后续可能出现的其他规范。
   
## 总结与展望

### 总结

* 从网信办发出整改通知，到我们为 App 合规通宵达旦，历经 3 个通宵紧急方案及半月的努力，总结出了不符合规范的 API 调用，违反《用户安全隐私协议》的具体场景。

* 结合业务安全合规检测背景，技术背景入手及未来可能出现的场景，覆盖 Android 代码检测，实现检出问题自动精准定位与问题聚合，提升了合规问题定位的消费效率；

* 业务合规检测还存在一些不足之处，比如检测工具的效能、差分比较、引用链建设、指标建设等，针对这些不足，后续将逐步进行完善、改进，持续为 Android 端应用安全合规地运营保驾护航。

### 展望

* 检测效能：寻找 `smail` 扫描的替代方案，提升工具的检测效率
* 差分比较：合规检测集成 `Jenkins` ，与 `CI`协同完成，对增量代码进行合规检测，避免重复检测、重复比较
* 引用链建设：针对不合规 `API` 生成对应调用链，提升不合规代码的定位精准度
* 平台化建设，做成一个审计平台，赋能其他的业务线




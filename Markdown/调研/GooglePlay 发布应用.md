# GooglePlay 发布应用
## 什么是 aab
Android App Bundle 是一种发布格式，其中包含应用的所有经过编译的代码和资源，它会将 apk 生成及签名交给 GooglePlay 来完成
GooglePlay 会根据 APP Bundle 针对每种设备配置生成并提供经过优化过的 apk， 因此只会下载特定设备所需的代码和资源来运行应用。
开发者不必再构建、签名和管理多个 apk 来优化对不同设备的支持， 而用户也可以获得更小且更优化的文件包。

**构建 app bundle**
通过 `./gradlew bundleRelease` 以及 `build.gralde` 中的签名配置，即可构建出 Android App Bundle ，并将其上传到 Google Play.

**压缩大小限制**
使用 Android App Bundle 发布 GooglePlay,需要压缩下载大小上限最大 150Mb。安装应用所需的压缩 apk (基本 apk + 配置 apk)的总大小。后续下载内容（如按需下载功能模块及其他配置Apk）也必须满足此压缩大小下载限制。Asset Pack 不受此限制，但他们有其他的大小限制

> Asset Pack 因具有较高的大小上限而成为大型游戏的理想之选：
> 每个 fast-follow 和 on-demand Asset Pack 的下载大小上限为 512 MB。
> 所有 install-time Asset Pack 的总下载大小上限为 1 GB。
> 一个 Android App Bundle 中的所有 Asset Pack 的总下载大小上限为 2 GB。
> 一个 Android App Bundle 中最多可以使用 50 个资源包。
> 如果您使用的是纹理压缩格式定位，那么这些下载限制会分别应用于每个独一无二的纹理格式。

请注意，Android App Bundzzle 不支持 APK 扩展 (*.obb) 文件。因此，如果您在发布 App Bundle 时遇到此错误，请使用以下某种资源来缩减压缩的 APK 下载大小：

* 请务必为每种类型的配置 APK 设置 enableSplit = true 以启用所有配置 APK。这样可以确保*用户只下载在其设备上运行您的应用所需的代码和资源。
* 请务必移除不用的代码和资源以[缩减应用大小](https://developer.android.com/studio/build/shrink-code)。
* 遵循最佳做法以进一步[缩减应用大小](https://developer.android.com/topic/performance/reduce-apk-size)。
* 考虑将只有部分用户使用的功能转换为应用可以在日后按需下载的功能模块。请注意，这可能需要对您的应用稍微进行重构，因此请务必先尝试上述其他建议。

## 总结
**aab 包内容**
![Img](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202206251333798.png?token=ADXVIORTZYBSKHCN75RPKI3CW2PIE)

**apk 包内容**
![Img](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202206251336527.png?token=ADXVIOSH6MGIT7MGKMGPJDTCW2PRW)

**注意事项**
<p style="color:RGB(255,0,0)">国内的黑科技不要用.</p>

## [Play Feature Delivery (pfd) 功能特性分发](https://developer.android.com/guide/app-bundle/dynamic-delivery)
模块化开发项目，可按条件分发或按需下载应用的某些功能
* 可减小应用的初始下载大小，后续按照功能配置按需下载，或特定设备下载。
* 在安装应用时需要某些功能，但之后又不需要了，您可以请求[从设备上移除相关功能来减小安装大小](https://developer.android.com/guide/playcore/play-feature-delivery#manage_installed_modules)。
   ::: tip 
   通过策略请求卸载部分功能，有助于减小 app 在设备中占用的空间，当用户设备存储不足时，降低 app 被卸载的风险
   :::
* 模块化需要的工作量大,可能需要重构目前的代码结构
### 清单文件汇总


### 模块化处理
将应用项目的逻辑组件拆分成独立的模块的过程
* **并行开发**：通过拆分成不同的模块，团队或个人认领负责不同的模块，减少代码合并的冲突以及其他团队的干扰。公共部分逻辑，可以使用库模块来促进重用和封装
* **缩短构建时间**： Gradle 对划分成模块的项目进行了优化，可并行构建多个模块，缩短构建时间。模块化越高，构建性能的改进越明显
* **自定义 Feature Delivery**：

| 属性 | 说明 |
| -- | -- | 
| \<manifest> | 标签与普通 module 标签没有区别 |
|xmlns:dist="http://schemas.android.com/apk/distribution"|指定一个新的 dist: XML 命名空间，如下所述。|
|split="split_name"|无需手动添加，用来标识模块的名称|
|android:isFeatureSplit="true \| false">|用来指定当前为功能模块。 base 模块和配置模块忽略此项或置 FALSE|
|\<dist:module|这一新的 XML 元素定义了一些属性，这些属性可确定如何打包模块并作为 APK 分发。|
|dist:instant="true \| false"|指定是否应通过 Google Play 免安装体验为模块启用免安装体验。|
|dist:title="@string/feature_name"|为模块指定一个面向用户的名称。例如，当设备请求确认下载时，便可能会显示该名称。    您需要将此名称的字符串资源包含在基本模块的 module_root/src/source_set/res/values/strings.xml 文件中。|
|\<dist:fusing dist:include="true \| false" />\</dist:module>|指定是否在面向搭载 Android 4.4（API 级别 20）及更低版本的设备的 multi-APK 中包含此模块。|
|\<dist:delivery>|封装自定义模块分发的选项，如下所示。请注意，每个功能模块必须只配置这些自定义分发选项的一种类型。|
|\<dist:install-time>|指定模块应在[安装时可用](https://developer.android.com/guide/app-bundle/at-install-delivery)。对于未指定自定义分发选项的其他类型的功能模块，这是默认行为。|
|\<dist:removable dist:value="true \| false" />|当未设置或设置为 false 时，bundletool 会在根据 bundle 生成拆分 APK 时将安装时模块整合到基本模块中。 由于整合会使拆分 APK 的数量减少，因此此设置可以提升应用的性能。|
|\<dist:conditions>|[按条件分发](https://developer.android.com/guide/app-bundle/conditional-delivery)|
|\</dist:install-time>||
|\<dist:on-demand/>|指定应以[按需下载](https://developer.android.com/guide/app-bundle/on-demand-delivery)的形式分发模块。也就是说，模块在安装时不会下载，但应用可以稍后请求下载。|
|\</dist:delivery>||
{.small}

### 测试 Play Feature Delivery
通过 GooglePlay 商店测试。 Play Feature Delivery 的优势都依赖 Play 商店完成。

* 通过网址分享。可快速上传 app bundle 并通过 GooglePlay 商店中的连接将应用分享给受信任的测试人员。同时测试自定义提供选项（按需下发）的最快方法。
* 设置开放式、封闭式或内部测试。通过提供结构话的测试通道，可以面向外部用户发布应用之前，充分地测试应用发布版本。


### 注意事项
* 通过按条件分发或按需分发方式在一台设备上安装 50 个或更多功能模块可能会导致性能问题。未配置为可移除的安装时模块会自动包含在基本模块中，并在每台设备上仅算作一个功能模块。
* 将您为安装时分发配置的可移除模块数量限制为不超过 10 个。否则，应用的下载和安装时间可能会增加。
* 只有搭载 Android 5.0（API 级别 21）及更高版本的设备才支持按需下载和安装功能。如需使功能适用于更低版本的 Android，请在创建功能模块时启用融合功能。
* 启用 SplitCompat，这样应用才能访问下载的按需分发功能模块。
* 在将 android:exported 设置为 true 的情况下，功能模块不得在其清单中指定 Activity。这是因为，当其他应用尝试启动相应 Activity 时，无法保证设备已下载相应的功能模块。此外，应用在尝试访问功能的代码和资源之前，应该先确认该功能已下载。如需了解详情，请参阅管理已安装的模块。
* 由于 Play Feature Delivery 要求使用 app bundle 发布应用，因此请确保您了解 app bundle 的已知问题。

### 模块配置
#### base
**build.gradle**
```groovy
apply plugin: 'com.android.application'

android {
    dynamicFeatures = [":dynamic_feature", ":dynamic_feature2"]
}

```
此模块内包含的所有代码和资源都在应用的基本 apk 中，要注意大小控制。
基本模块除了提供核心功能外，还提供许多影响整个项目的构建配置和清单条目。比如：
1. app bundle 的签名
2. version code

#### 清单配置

```xml

    <!-- This line makes the "app" module instant enabled, which means this bundle can be uploaded
        to the instant track on the Google Play Developer Console -->
    <dist:module dist:instant="true" />
```

GooglePlay 在生成 apk 应用时，会将所有模块的清单合并到基本 apk 的清单中。
* 因为始终会先安装 base apk，因此 base apk 应该为应用提供主入口点，即使用下面的 intent  过滤声明 Activity
   ```xml
    <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
   ```
* 清单文件中需要增加对 `SplitCompat` 库的支持，才能访问已下载模块的代码和资源。
    ```kotlin
    class MyApplication : Application() {

        override fun attachBaseContext(base: Context) {
            LanguageHelper.init(base)
            val ctx = LanguageHelper.getLanguageConfigurationContext(base)
            super.attachBaseContext(ctx)
            SplitCompat.install(this)
        }  
    }
    ```
    
#### 基本模块构建配置
* 应用签名：您无需在构建配置文件中包含签名信息，除非您想从命令行构建 app bundle。不过，如果包含了签名信息，则*应仅将其包含在基本模块的构建配置文件中。如需了解详情，请参阅配置 Gradle 来为您的应用签名。
* 代码缩减：如果需要为整个应用项目（包括其功能模块）启用代码缩减，您必须从基本模块的 build.gradle 文件实现。也就是说，您可以在功能模块中包含自定义 ProGuard 规则，但是功能模块构建配置中的 minifyEnabled 属性将被忽略。
* 忽略 splits 块：构建 app bundle 时，Gradle 会忽略 android.splits 块中的属性。如果您想控制 app bundle 所支持的配置 APK 的类型，请改为使用 android.bundle 来停用配置 APK 的类型。
* 应用版本控制：基本模块将确定整个应用项目的版本代码和版本名称。如需了解详情，请转到介绍如何管理应用更新的部分。

#### 开关 apk 配置
```gradle
android {
    // When building Android App Bundles, the splits block is ignored.
    splits {...}

    // Instead, use the bundle block to control which types of configuration APKs
    // you want your app bundle to support.
    bundle {
        language {
            // Specifies that the app bundle should not support
            // configuration APKs for language resources. These
            // resources are instead packaged with each base and
            // feature APK.
            enableSplit = false
        }
        density {
            // This property is set to true by default.
            enableSplit = true
        }
        abi {
            // This property is set to true by default.
            enableSplit = true
        }
    }
}
```

### Feature 模块

**build.gradle**
```gradle
apply plugin: 'com.android.dynamic-feature'
````

**清单文件**

```xml

<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:dist="http://schemas.android.com/apk/distribution"
    package="com.google.android.samples.dynamicfeatures.ondemand.kotlin">

    <dist:module
        dist:title="@string/module_feature_kotlin">
        <dist:fusing dist:include="true" />
        <dist:delivery>
            <dist:on-demand />
        </dist:delivery>
    </dist:module>

    <application>
        <activity android:name="com.google.android.samples.dynamicfeatures.ondemand.KotlinSampleActivity">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
            </intent-filter>
        </activity>
    </application>

</manifest>

```

#### 不应包含在功能模块构建配置中的内容
由于每个功能模块都依赖于基本模块，因此它还会继承某些配置。因此，您应该在功能模块的 build.gradle 文件中省略以下内容：

* 签名配置：使用您在基本模块中指定的签名配置对 app bundle 进行签名。
* minifyEnabled 属性：您只能在基本模块的构建配置中为整个应用项目启用代码缩减。因此，您应该在功能模块中省略此属性。不过，您可以为每个功能模块指定其他 ProGuard 规则。
* versionCode 和 versionName：构建 app bundle 时，Gradle 会使用基本模块提供的应用版本信息。您应该在功能模块的 build.gradle 文件中省略这些属性。

#### 与基本模块之间的关系

**base -> feature**
```gradle
// In the base module’s build.gradle file.
android {
    ...
    // Specifies feature modules that have a dependency on
    // this base module.
    dynamicFeatures = [":dynamic_feature", ":dynamic_feature2"]
}
```
**feature -> base**

```gradle
// In the feature module’s build.gradle file:
...
dependencies {
    ...
    // Declares a dependency on the base module, ':app'.
    implementation project(':app')
}
```

#### 部署应用
在开发支持功能模块的应用时，您可以像往常一样，从菜单栏中依次选择 Run > Run（或点击工具栏中的 Run 图标 ），将该应用部署到连接的设备。

如果您的应用项目包含一个或多个功能模块，您可以通过修改现有的运行/调试配置以选择需要在部署应用时包含的功能，具体操作步骤如下：

1. 从菜单栏中依次选择 Run > Edit Configurations。
2. 在 Run/Debug Configurations 对话框的左侧面板中，选择所需的 Android App 配置。
3. 在 General 标签页中的 Dynamic features to deploy 下，选中需要在部署应用时包含的每个功能模块旁边的复选框。
4. 点击 OK。

默认情况下，Android Studio 不会使用 app bundle 部署您的应用，而是由 IDE 构建针对部署速度（而非 APK 大小）进行了优化的 APK，并将其安装到设备中。如需将 Android Studio 配置为通过 app bundle 构建和部署 APK 以及免安装体验，请修改运行/调试配置。


### Play Feature Delivery 实操
[官方 Play Feature Delivery 操作指南](https://developer.android.com/guide/playcore/play-feature-delivery)


## [Play Assets Delivery (pad) 资源分发](https://developer.android.com/guide/app-bundle/asset-delivery)
发布游戏应用，可用于分发大量游戏资产的解决方案，为开发者提供了灵活的分发方式和极高的性能








##  APP bundle 的测试

### Android Studio Run
在研发阶段， Android  Studio 还是以 apk 的方式，并携带全部内容，可直接 run 在设备上。
当有调试需要时，可通过 `edit configuration` 进行相关配置, 如下图：
![Img](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/202206261448882.png?token=ADXVIOQ5MKJVVY73RZCEF4LCXAAYG)

再次从菜单栏中依次选择 Run > Run 时，Android Studio 会构建 app bundle，并使用它来仅部署连接的设备和您选择的功能模块所需的 APK。

### 命令行构建
命令行工具构建 app bundle，可用于对 `CICD` 支持

这些本地测试工具对于执行以下操作很有用：

* 将可配置的 app bundle build 集成到持续集成 (CI) 服务器或其他自定义构建环境中。
* 自动将应用从 app bundle 部署到连接的一个或多个测试设备。
* 模拟从 Google Play 将应用下载到连接的设备。

从命令行构建应用，可以使用 `bundletool` 或 Android Gradle 插件来执行操作
[bundletool](https://github.com/google/bundletool/releases/tag/1.10.0)： Android Gradle 和 Google Play 都是通过此命令工具构建 app bundle,具体实施可参考 [从命令行构建应用](https://developer.android.com/studio/build/building-cmdline)。

bundletool 提供了专门为了帮助您测试 app bundle 并模拟通过 Google Play 分发而设计的命令。

您可以使用 bundletool 测试下面这些不同类型的场景：

* 生成 APK 集，其中包含应用支持的所有设备配置的拆分 APK。通常需要先构建 APK 集，然后 bundletool 才能将应用部署到连接的设备。
* 如果您不希望构建包含应用的所有拆分 APK 的 APK 集，可以根据连接的设备或设备规范 JSON 生成设备专用的 APK 集。
* 从 APK 集将应用部署到连接的设备。bundletool 会使用 adb 确定各种设备配置所需的拆分 APK，并且只将这些 APK 部署到设备。如果您有多台设备，还可以将设备 ID 传递给 bundletool，以将特定设备作为部署目标。
* 在本地测试功能分发选项。您可以使用 bundletool 模拟设备从 Google Play 下载和安装功能模块的过程，而无需实际将应用发布到 Play 管理中心。如果您要在本地测试应用如何处理按需模块下载请求和失败情况，那么这会很有帮助。
* 针对给定的设备配置估算应用的下载大小。这有助于更好地理解下载应用的用户体验，以及检查应用是否符合 app bundle 的压缩下载大小限制或启用免安装体验。


### 在 Play 上测试 app bundle
使用 Play 管理中心进行测试可以最准确的反映用户体验。可供 QA 团队，限定人数的 alpha 版测试人员。
使用 Play 管理中心测试的优势
1. 希望最准确地反映下载应用以及按需安装功能的用户体验
2. 希望让一组测试人员轻松访问
3. 将测试方位限定到 QA, alpha 版和 beta 版测试人员
4. 访问在设备上测试的应用上传的历史记录。

### 将应用上传到测试轨道
当您在 Play 管理中心内上传应用并创建版本时，可以让版本先经过多个测试阶段，然后再发布为正式版：

* 内部测试：创建内部测试版本，快速分发应用以进行内部测试和质量保证检查。
* 封闭式测试：创建封闭式测试版本，让更多测试人员测试应用的预发布版本。在让少量的员工或受信任的用户测试应用后，便可以扩展测试范围，进行开放式版本测试。“应用版本”页面中将提供一个 Alpha 版轨道，供您首次进行封闭式测试时使用。您还可以视需要创建其他封闭式测试轨道，并为其命名。
* 开放式测试：完成封闭式测试版本的测试后，创建开放式测试版本。您可以让更广泛的用户参与开放式测试版本的测试，然后再发布应用的正式版。

### 使用发布前测试报告找出问题
将 APK 或 app bundle 上传到开放式测试或封闭式测试轨道后，您可以检查自己的应用在搭载不同版本 Android 系统的各种设备上运行时是否存在问题。

Play 管理中心的发布前测试报告可帮助您发现以下几方面的潜在问题：

* 稳定性
* Android 兼容性
* 性能
* 无障碍功能
* 安全漏洞

在您上传 app bundle 后，测试设备会自动启动您的应用并执行几分钟的抓取操作。抓取工具每隔几秒钟对您的应用执行一次基本操作，如输入、点按和滑动。

测试完成后，您可以在 Play 管理中心的发布前测试报告部分中查看测试结果。如需了解详情，请参阅关于如何使用发布前测试报告找出问题的 Play 管理中心帮助主题。



## 核心库

[play core 核心库](https://developer.android.com/guide/playcore#license)

[命令行构建 app bundle](https://developer.android.com/studio/build/building-cmdline#build_bundle)

[Bundletool 工具小插件](https://github.com/google/bundletool/releases/tag/1.10.0)

[pad Unity 插件](https://docs.unity3d.com/Manual/AssetBundles-Browser.html)

[samples code](https://github.com/android/app-bundle-samples)
[扶正 aab，再见 apk](https://juejin.cn/post/6984588418554527774#heading-8)

## 指令集

[bundletool](https://developer.android.com/studio/command-line/bundletool)


## 疑问
1. pfd 和 pad 是否可以同时使用
2. 是否可以从 pfg 切换到 pad 互换。
3. pfd feature 之间如何通信
4. 
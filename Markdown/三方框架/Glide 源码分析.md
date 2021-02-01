---
title: Glide
tag: 三方框架
---



Glide 作为广为熟知的图片加载框架，在开发工作中出现的频率非常高，同比的还有 `Picasso` 和 `ImageLoader` 两套框架。 都各有特色。这里主要还是讲一下 `Glide` 。

**基础用法：**

```java
Glide.with(this).load(url).into(imageView);
```

<!-- more -->

在 Android 开发中，我们通常最简单的使用 `Glide` 的 代码如上面一样，如此简单的 api, 就可以帮助我们实现加载本地图片，本地 Drawable ， Gif 图，以及 网络图片，那么在这样简单的 API 的背后，其实它帮助了我们完成了很多工作。

从简单的使用我们入手，可以看到，要想加载一张图片，我们需要一个当前上下文对象，一个图片地址，一个承载图像的 ImageView 容器。那中三个要求，又同时对应着三个函数，`with` `load` 和 `into`，阅读源码，那就是从源码暴漏给我们最直观的地方进入，不然就是一只没头的苍蝇—到处乱飞。

| 函数 |                           主要功能                           |
| :--: | :----------------------------------------------------------: |
| with | 1. 初始化Glide对象<br />2. 创建空白的 Fragment 管理生命周期机制<br />3. 创建一个 RequestManager 管理任务 |
| load |          最终构建出 RequestBuilder ，记录传入的数据          |
| into | 1. runRequest 运行队列/等待队列，执行队列 Reqeust 对象<br />2. 活动缓存<br />3. 内存缓存<br />4. HttpUrlConnection |

## 工作流程

`Glide` 通过 `with` 函数，给自己的实例化，并创建一个空白的 `Fragment` 来管理生命周期并绑定 `ReqeustManager` 。继续通过 `load() ` 函数构建一个 `RequestBuilder()` 并缓存我们的参数，继续通过 `into` 创建一个 `Request` 对象，并记录宽高、采样数据等。继续，在发起请求之前，先检查一下缓存数据, 活动缓存 `ActivityResources` 有没有数据，再检查内存缓存 `LRUResourceCache` ，如果两级缓存都未命中，则启动一个异步任务 `DecodeJob`, 去检查 `DiskCache` 中有没有本地磁盘缓存数据，如果没有，通过网络请求数据 `HttpUrlConnection` ，解析 `InputStream` 进行采样，最终拿到 `Bitmap`，将 `Bitmap` 转换成 `Drawable` 并讲数据缓存到磁盘中。

## with

从上面的表格中，我们可以看出来 `with` 函数，就是用来帮我创建 `Glide` 对象，并创建一个空白的 `Fragment` 来管理生命周期。其具体的工作流程如图：

![Glide with 时序图](https://github.com/xiaomanwong/static_file/blob/master/images/glide_with_sequence.jpg?raw=true)

由上面的时序图，我们可以顺序的分析，我们一步步去分析。

**Glide.with()**

`Glide.with()` 为提供了多种重构函数，目的是为我们提供它强大的作用域以及满足我们开发过程中各种复杂的情况。同时适配不同版本以及不同的应用场景。

```java
@NonNull
public static RequestManager with(@NonNull Context context) {
    return getRetriever(context).get(context);
}

@NonNull
public static RequestManager with(@NonNull Activity activity) {
    return getRetriever(activity).get(activity);
}

@NonNull
public static RequestManager with(@NonNull FragmentActivity activity) {
    return getRetriever(activity).get(activity);
}

@NonNull
public static RequestManager with(@NonNull Fragment fragment) {
    return getRetriever(fragment.getContext()).get(fragment);
}

@NonNull
public static RequestManager with(@NonNull android.app.Fragment fragment) {
    return getRetriever(fragment.getActivity()).get(fragment);
}

@NonNull
public static RequestManager with(@NonNull View view) {
    return getRetriever(view.getContext()).get(view);
}
```

**getRetriever**()

`getRetriever()` 通过 Glide 的 get 函数，帮我们初始化了一个 `Glide` 对象。

```java
@NonNull
private static RequestManagerRetriever getRetriever(@Nullable Context context) {
    return Glide.get(context).getRequestManagerRetriever();
}
```

**get(context)**

可以看出，Glide 是一个单例的，向下看时，我们也可看到，对 Glide 的检查很严谨。

```java
private static volatile Glide glide;
@NonNull
public static Glide get(@NonNull Context context) {
    if (glide == null) {
        synchronized (Glide.class) {
            if (glide == null) {
                checkAndInitializeGlide(context, annotationGeneratedModule);
            }
        }
    }
    return glide;
}
```

**checkAndInitializeGlide() & initializeGlide()**

最终通过构造者模式，完成了对 `Glide` 对象的初始化，同时在构造者中，也对很多 `Glide` 工作时需要的对象进行了初始化。我们这里只研究主线业务，其它的可以私下看。

```java
private static void checkAndInitializeGlide(
    if (isInitializing) {
        throw new IllegalStateException(
            "You cannot call Glide.get() in registerComponents(),"
            + " use the provided Glide instance instead");
    }
    isInitializing = true;
    initializeGlide(context, generatedAppGlideModule);
    isInitializing = false;
}
private static void initializeGlide(Context context, GlideBuilder builder, GeneratedAppGlideModule annotationGeneratedModule) {
    Glide glide = builder.build(applicationContext);
    Glide.glide = glide;
}
```

到这里， `Glide` 的初始化工作已经完成，具体初始化了什么信息，细节的东西，自己需要去认真的阅读源码。

并且代码按照流程，`get()` 的深度代码已经完成，程序会逐步回到 `getRetriever()` 函数中，去执行 `getRequestManagerRetriever` ， `getRequestManagerRetriever` ` 是通过 `Glide 的构造器完成的初始化工作，此时直接返回已经创建好的对象。并继续执行 `with()`函数 的 `get()` 去创建 `RequestManager`

**get(Fragment fragment)**

这时候，我们发现，现在代码已经跳转到 `RequestManagerRetriever` 类中

**RequestManagerRetriever**

`RequestManagerRetriever` 是一个管理类，负责生产 `Fragment` 对象，根据我们传入的 `Context` 上下文的定义不同，最终会帮我们创建不同的生命周期管理。

```java
  @NonNull
  public RequestManager get(@NonNull Fragment fragment) {
    if (Util.isOnBackgroundThread()) {
        // 创建一个全局作用域的 RequestManager，生命周期很长，容易出现内存问题
      return get(fragment.getContext().getApplicationContext());
    } else {
      FragmentManager fm = fragment.getChildFragmentManager();
      return supportFragmentGet(fragment.getContext(), fm, fragment, fragment.isVisible());
    }
  }

  public RequestManager get(@NonNull Context context) {
    if (context == null) {
      throw new IllegalArgumentException("You cannot start a load on a null Context");
    } else if (Util.isOnMainThread() && !(context instanceof Application)) {
      if (context instanceof FragmentActivity) {
        return get((FragmentActivity) context);
      } else if (context instanceof Activity) {
        return get((Activity) context);
      } else if (context instanceof ContextWrapper
          && ((ContextWrapper) context).getBaseContext().getApplicationContext() != null) {
        return get(((ContextWrapper) context).getBaseContext());
      }
    }
         // 创建一个全局作用域的 RequestManager，生命周期很长，容易出现内存问题
      return getApplicationManager(context);
  }
```

> **Note:**
>
> 1. **如果当前任务工作在后台线程或者传入的 `Context` 对象是一个 `Application` 级别的，那 `Glide` 就会帮我们创建一个和 `Application` 同生命周期的 `RequestManager` 对象，这个对象生命周期很长， 如果我们不规范使用的话，这里很容易造成<font color=red>内存的泄漏</font>**。 因此我们使用时，尽量不要传入里类似的。
>
> 2. 如果我们传入的是一个 Fragment 对象， Activity 对象等等，那 `Glide` 就会帮我们创建个空白的 `Fragment`， `supportFragmentGet` 和  `fragmentGet` 两种方案是用来做 `androidX` 和 `android.app`中不同 `fragment` 的适配

**supportFragmentGet**

创建管理生命周期的 Fragment, `androidx` 对应的是 `supportFragmentGet()` ， `android.app` 对应的是 `fragmentGet()`， 这里以 `supportFragmentGet()` 为例：

```java
  @NonNull
  private RequestManager supportFragmentGet(
      @NonNull Context context,
      @NonNull FragmentManager fm,
      @Nullable Fragment parentHint,
      boolean isParentVisible) {
      // 创建/获取当前空白的 Fragment
    SupportRequestManagerFragment current =
        getSupportRequestManagerFragment(fm, parentHint, isParentVisible);
      // 获取空白 Fragment 中的 RequestManager 对象
      // 如果为空，那么就通过工厂创建一个，并绑定回空白的 Fragment 中
    RequestManager requestManager = current.getRequestManager();
    if (requestManager == null) {
      Glide glide = Glide.get(context);
      requestManager =
          factory.build(
              glide, current.getGlideLifecycle(), current.getRequestManagerTreeNode(), context);
      current.setRequestManager(requestManager);
    }
      // 返回 reqeustManager 对象
    return requestManager;
  }

  @NonNull
  private SupportRequestManagerFragment getSupportRequestManagerFragment(
      @NonNull final FragmentManager fm, @Nullable Fragment parentHint, boolean isParentVisible) {
      // 从 FragmentManager 中获取当前已经初始化好，并添加到 Fragment/Activity 中我们空白的 SupportRequestFragment 
    SupportRequestManagerFragment current =
        (SupportRequestManagerFragment) fm.findFragmentByTag(FRAGMENT_TAG);
      // 如果为空，说明空白的 Fragment 还没有被添加进去
    if (current == null) {
        // pendingSupportRequestManagerFragments 是一个 HashMap 集合，用来暂存空白 Fragment 对象
        // 由于 Glide 是一个单例对象，在 Glide 的 builder 中，间接的创建了 RequestManagerRetriever 对象，
        // 因此 RequestManagerRetriever 也是一个单例，不同的 Activity/Fragment, 会有多个，因此这里用一个 HashMap 来存储空白 Fragment，
        // 同时，为了保证每个页面只会有一个空白 Fragment，并可以快速定位，所以使用了 HashMap
      current = pendingSupportRequestManagerFragments.get(fm); // 第一保障
        // 如果当前缓存的数据中，仍然没有创建好 Fragment， 那就说明当前的空白 Fragment 还没有被创建
      if (current == null) {
          // 创建一个新的空白 Fragment
        current = new SupportRequestManagerFragment();
        current.setParentFragmentHint(parentHint);
        if (isParentVisible) {
            // 调用生命周期方法，让所有的监听者开始任务（后面会说）
          current.getGlideLifecycle().onStart();
        }
          // 将创建好的 Fragment 存入到集合中
        pendingSupportRequestManagerFragments.put(fm, current);
          // Handler 通知父容器，这里添加了一个 Fragment
        fm.beginTransaction().add(current, FRAGMENT_TAG).commitAllowingStateLoss();
          // 发送一个 handler 消息，将数据从集合中移除，节省内存空间。（第二保障）
        handler.obtainMessage(ID_REMOVE_SUPPORT_FRAGMENT_MANAGER, fm).sendToTarget();
      }
    }
    return current;
  }
```

> **Note:**
>
> 这里有一个比较困惑的地方就是，将已经创建好的 `Fragment` 添加到集合中去后，又通过 `Handler` 消息，将这个 `Fragment` 从集合中移除，这是为什么呢？
>
> 其实最终的目的是节省内存空间做的一个优化，通过 Handler来处理是因为，`fragment` 的添加也是通过 `Handler` 来完成的，但 `Handler` 消息的执行时间不能保证，因此通过 `Handler` 再发一次消息，让移除操作在 `Fragment` 添加完成之后去执行，就一定能够得到保障。
>
> 只有当 `Fragment` 被添加进入父容器之后， `fm.findFragmentByTag` 才能获取到对象。这也是为了保证每个父容器都只有一个空白 `Fragment` 的两次保障。

## 类关系图

至此，with 函数的所有主线业务已经说完了，但究竟 Fragment 是如何监听生命周期变化的呢？我们来看下面这张关系图

![Glide lifecycle](https://github.com/xiaomanwong/static_file/blob/master/images/glide_struct.jpg?raw=true)

**SupportRequestManagerFragment** 

内部绑定了 `ActivityFragmentLifecycle` ，通过 Fragment 生生命周期变化，来引导 `RequestManager` 完成图片的请求和后续的显示

我们查看下源码：

```java
public class SupportRequestManagerFragment extends Fragment {
  private static final String TAG = "SupportRMFragment";
  private final ActivityFragmentLifecycle lifecycle;

  @SuppressLint("ValidFragment")
  public SupportRequestManagerFragment(@NonNull ActivityFragmentLifecycle lifecycle) {
      // 构造器创建了 ActivityFramgentLifecycle
    this.lifecycle = lifecycle;
  }
    
  // 在前面初始化 SupportRequestManagerFragment 的代码中，我们还记得他手动的调用了一下 start 方法吧
  @Override
  public void onStart() {
    super.onStart();
    lifecycle.onStart();
  }

  @Override
  public void onStop() {
    super.onStop();
    lifecycle.onStop();
  }

  @Override
  public void onDestroy() {
    super.onDestroy();
    lifecycle.onDestroy();
    unregisterFragmentWithRoot();
  }
    
  @NonNull
  ActivityFragmentLifecycle getGlideLifecycle() {
    return lifecycle;
  }
}
```



当 Fragment / Activity 已经不可见时，通过生命周期变化，通知业务功能类去停止请求或调用，防止内存泄漏和崩溃。



## load

![Glide load](https://github.com/xiaomanwong/static_file/blob/master/images/glide_load.jpg?raw=true)

我们将 `Glide.with(this).load(url).into(view);` 拆分开来写，如下：

```java
RequestManager requestManager = Glide.with(this);
RequestBuilder requestBuilder = requestManager.load(url);
requestBuilder.into(view);
```

可以看出， load 函数，我们传入了一个 `String` 类型的 `Url`， 最终返回给我们一个 `RequestBuilder` 对象。按照上面的时序图，我们简单分析一下可以看出，实际上 `RequestBuilder` 就是一个构造者，记录我们传入的参数，最终将我们传入的内容转化为一个 `Drawable` 。

`Glide` 也为我们提供了丰富的 `load api`， 我们可以传入 `url, bitmap, byte[], Drawable, Uri, File, Integer` 等等， `RequestBuilder` 就是来记录我们传入的具体是一个什么样子的数据，并将他们在展示的时候，最终转化成一个 `Drawable` 给图片容器，也就是后面我们要说的 `into` 函数。



## into

into 的流程相当复杂，流程图已经展示不下，也不清晰。这是一张不完整的时序图。并没有体现网络请求的部分，和缓存的部分。

![](https://github.com/xiaomanwong/static_file/blob/master/images/glide_into.jpg?raw=true)

但我们先按照这个残图先分析一下。

当 `into(imageview)` 被调用后

```java
public ViewTarget<ImageView, TranscodeType> into(@NonNull ImageView view) {
    Util.assertMainThread();
    Preconditions.checkNotNull(view);

    BaseRequestOptions<?> requestOptions = this;
    if (!requestOptions.isTransformationSet()
        && requestOptions.isTransformationAllowed()
        && view.getScaleType() != null) {
      switch (view.getScaleType()) {
        case CENTER_CROP:
          requestOptions = requestOptions.clone().optionalCenterCrop();
          break;
        case CENTER_INSIDE:
          requestOptions = requestOptions.clone().optionalCenterInside();
          break;
        case FIT_CENTER:
        case FIT_START:
        case FIT_END:
          requestOptions = requestOptions.clone().optionalFitCenter();
          break;
        case FIT_XY:
          requestOptions = requestOptions.clone().optionalCenterInside();
          break;
        case CENTER:
        case MATRIX:
        default:
          // Do nothing.
      }
    }
```

Glide 显示对图片进行了解析，获取图片的尺寸等信息。

```java
  private <Y extends Target<TranscodeType>> Y into(
      @NonNull Y target,
      @Nullable RequestListener<TranscodeType> targetListener,
      BaseRequestOptions<?> options,
      Executor callbackExecutor) {
    Preconditions.checkNotNull(target);
    if (!isModelSet) {
      throw new IllegalArgumentException("You must call #load() before calling #into()");
    }
    Request request = buildRequest(target, targetListener, options, callbackExecutor);
    Request previous = target.getRequest();
    requestManager.clear(target);
    target.setRequest(request);
    requestManager.track(target, request);

    return target;
  }
```

继续，创建了一个 `Request` ，这个 `Request` 的真实对象是 `SingleRequest` ，并通过 `requestManager` 执行了这个请求任务。利用三层缓存策略，最终展示了一张图片。






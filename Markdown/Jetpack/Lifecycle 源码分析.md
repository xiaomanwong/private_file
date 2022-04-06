---
title: Android Lifecycle
tag: Android

---

## 开始是废话（翻译自源码）

定义了一个 Android 生命周期的对象。 `Fragment`和`FragmentActivity`类实现`LifecycleOwner`接口， 并可以通过 `getLifecycle()` 方法来访问生命周期。 我们也可以实现`LifecycleOwner`在自己的类。

<!-- more -->

```Java
// 在此类事件后分发 LifecycleOwner 的相关方法的返回时。 
Lifecycle.Event.ON_CREATE ， Lifecycle.Event.ON_START ， Lifecycle.Event.ON_RESUME
// 在此类事件在之前分派LifecycleOwner被称为的相关方法。 例如， Lifecycle.Event.ON_START后会被分派onStart回报， Lifecycle.Event.ON_STOP之前将派出onStop被调用。 这给你一定的保证在其国家的主人在不在。
Lifecycle.Event.ON_PAUSE ， Lifecycle.Event.ON_STOP ， Lifecycle.Event.ON_DESTROY
```


如果您使用Java 8 语言 ，然后使用`DefaultLifecycleObserver` 观察事件。 需要将`"androidx.lifecycle:common-java8:<version>"` 增加到你的 `build.gradle` 文件中。

```java
class TestObserver implements DefaultLifecycleObserver {
    @Override
    public void onCreate(LifecycleOwner owner) {
        // your code
    }
}
```

  

如果你使用的Java 7 语言 ，使用的注解观察生命周期事件。 一旦Java的8语言成为在Android上的主流，注释将被弃用，所以`DefaultLifecycleObserver`和注释之间，则须偏向 `DefaultLifecycleObserver `。

   ```java 
class TestObserver implements LifecycleObserver {
    @OnLifecycleEvent(ON_STOP)
    void onStopped() {}
}
   ```

观测方法可以接收零个或一个参数。 如果使用，第一个参数的类型必须为`LifecycleOwner` 。 带注释的方法`Lifecycle.Event.ON_ANY` 可以接收第二个参数，它必须是类型的`Lifecycle.Event `。

  ```java
class TestObserver implements LifecycleObserver {
    @OnLifecycleEvent(ON_CREATE)
    void onCreated(LifecycleOwner source) {}
    @OnLifecycleEvent(ON_ANY)
    void onAny(LifecycleOwner source, Event event) {}
}
  ```

提供这些额外的参数可以让您方便地观察到多个供应商和事件，而无需手动跟踪他们。

##  那我能做什么呢

说到这里，我们就应该想到一些在开发中常常不被我们忽视，但又不怎么使用的东西 **友盟统计**

在友盟统计中，我们经常会在 `BaseActivity` 中插入友盟对页面流转的统计, `onStart()` `onResume()` `onPause()` `onStop()` 等，然而这里有一点不好的是，我们的业务和公共组件耦合在了一起。

干货~~~来了

那么解决上述问题的方案就来了，我们通过实现 `LifecycleObserver` ，通过标识声明周期方法之后，仅需一句 `addObserver(this)` ，就可以将 `Activity` 或 `Fragment ` 的声明周期方法与我们定义的 `Observer` 方法关联起来。通过感知 `Activity` 或 `Fragment` 的声明周期方法，实现友盟统计，此时就将业务整体与 `BaseActivity` 抽离开，是的公共组件变得更简洁一些。

当然，这只是 `Lifecycle` 的一种简单应用，其他的使用方法还是需要我们不断的去探索。

## 源码分析

### **`Lifecycle UML`**

![Lifecycle UML](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/Lifecycle%20UML.png?token=GHSAT0AAAAAABTDT2CDUK2BEJXEUJAKZ5HAYSNOQ4Q)

**想理解一个东西，最好的方式就是去阅读它**， 这是开发多年总结出的一句话。

那么通过上面的 UML 类图关系，我们能够看出， `Lifecycle` 的内容并不是很多。但它怎么就会这么强大呢。

### **`ComponentActivity` & `ReportFragment`**

就算没看过源码，知道`Lifecycle` 的人，也应该听说个，这是要给声明周期监控类，那么既然和生命周期有关，那自然是和 `Activity` 有关，通过`AppCompatActivity` 类，我们向上查找，我们可以看到 `ComponentActivity` 这个类，实现了 `LifecycleOwner` 接口，并返回了一个 `mLifecycleRegistry`

```java
// ComponentActivity 类初始化是，创建了一个 LifecycleRegistry，并将自己传入过去
private final LifecycleRegistry mLifecycleRegistry = new LifecycleRegistry(this);

// LifecycleOwner 接口，提供了一个 getLifecycle() 方法
@Override
public Lifecycle getLifecycle(){
    return mLifecycleRegistry;
}
```

在 `ComponentActivity` 的构造方法里，适配了不同的平台版本。

```java
public ComponentActivity() {
    Lifecycle lifecycle = getLifecycle();
    //noinspection ConstantConditions
    if (lifecycle == null) {
        throw new IllegalStateException("getLifecycle() returned null in ComponentActivity's "
                                        + "constructor. Please make sure you are lazily constructing your Lifecycle "
                                        + "in the first call to getLifecycle() rather than relying on field "
                                        + "initialization.");
    }
    if (Build.VERSION.SDK_INT >= 19) {
        getLifecycle().addObserver(new LifecycleEventObserver() {
            @Override
            public void onStateChanged(@NonNull LifecycleOwner source,
                                       @NonNull Lifecycle.Event event) {
                if (event == Lifecycle.Event.ON_STOP) {
                    Window window = getWindow();
                    final View decor = window != null ? window.peekDecorView() : null;
                    if (decor != null) {
                        decor.cancelPendingInputEvents();
                    }
                }
            }
        });
    }
    getLifecycle().addObserver(new LifecycleEventObserver() {
        @Override
        public void onStateChanged(@NonNull LifecycleOwner source,
                                   @NonNull Lifecycle.Event event) {
            if (event == Lifecycle.Event.ON_DESTROY) {
                if (!isChangingConfigurations()) {
                    getViewModelStore().clear();
                }
            }
        }
    });

    if (19 <= SDK_INT && SDK_INT <= 23) {
        getLifecycle().addObserver(new ImmLeaksCleaner(this));
    }
}
```

通过构造方法，有没有发现一个很重要的信息， `addObserver()`， 由此，我们不难看出 ，`LifecycleRegister` 的一个重要的方法就是 `addObserver()` 。翻阅类结构了解到 `LifecycleRegister` 是 `Lifecycle` 派生的一个子类，有关所有和声明周期有关的内容，都和这个类有关。

我们先不着急看 `LifecycleRegister`，继续看 `CompontentActivity` 类，既然是个 `Activity` 那么一定会有创建过程，回看 `onCreate()` 方法，我们可以观察到一个有趣的东西：

```java
/**
     * {@inheritDoc}
     *
     * If your ComponentActivity is annotated with {@link ContentView}, this will
     * call {@link #setContentView(int)} for you.
     */
@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    mSavedStateRegistryController.performRestore(savedInstanceState);
    ReportFragment.injectIfNeededIn(this);
    if (mContentLayoutId != 0) {
        setContentView(mContentLayoutId);
    }
}
```

`ReportFragment.injectIfNeededIn(this)` 咦？？？？？？？？？？？ 你是谁，你在这儿做什么。

别慌，进去看。

#### `ReportFragment`

```java
public static void injectIfNeededIn(Activity activity) {
    // ProcessLifecycleOwner should always correctly work and some activities may not extend
    // FragmentActivity from support lib, so we use framework fragments for activities
    android.app.FragmentManager manager = activity.getFragmentManager();
    if (manager.findFragmentByTag(REPORT_FRAGMENT_TAG) == null) {
        manager.beginTransaction().add(new ReportFragment(), REPORT_FRAGMENT_TAG).commit();
        // Hopefully, we are the first to make a transaction.
        manager.executePendingTransactions();
    }
}
```

咦？？？？为什么要在我的 `Activity` 上添加一个 `Fragment`， 翻遍代码，我们也未见到任何布局，你是一个**空的** ，😱😱😱， 太可怕了！

按照 `Fragment` 的生命周期，我们继续看

##### `dispatch()`

```java

@Override
public void onActivityCreated(Bundle savedInstanceState) {
    super.onActivityCreated(savedInstanceState);
    dispatchCreate(mProcessListener);
    dispatch(Lifecycle.Event.ON_CREATE);
}

@Override
public void onStart() {
    super.onStart();
    dispatchStart(mProcessListener);
    dispatch(Lifecycle.Event.ON_START);
}

@Override
public void onResume() {
    super.onResume();
    dispatchResume(mProcessListener);
    dispatch(Lifecycle.Event.ON_RESUME);
}

@Override
public void onPause() {
    super.onPause();
    dispatch(Lifecycle.Event.ON_PAUSE);
}

@Override
public void onStop() {
    super.onStop();
    dispatch(Lifecycle.Event.ON_STOP);
}

@Override
public void onDestroy() {
    super.onDestroy();
    dispatch(Lifecycle.Event.ON_DESTROY);
    // just want to be sure that we won't leak reference to an activity
    mProcessListener = null;
}
```

有没有发现， 又有一个方法被重复的利用，没错，就是`dispatch(Lifecycle.Event event)` 而且传入的参数，又和 `Activity` 的生命周期一致。那么我们来看看它.

##### `handleLifecycleEvent()`

```java
private void dispatch(Lifecycle.Event event) {
    Activity activity = getActivity();
    if (activity instanceof LifecycleRegistryOwner) {
        ((LifecycleRegistryOwner) activity).getLifecycle().handleLifecycleEvent(event);
        return;
    }

    if (activity instanceof LifecycleOwner) {
        Lifecycle lifecycle = ((LifecycleOwner) activity).getLifecycle();
        if (lifecycle instanceof LifecycleRegistry) {
            ((LifecycleRegistry) lifecycle).handleLifecycleEvent(event);
        }
    }
}
```

虽然经过了两个判断，但这没关系，因为这是系统帮助我们做的适配工作，无论如何，他们队中都调用了 `handleLifecycleEvent(event)` 方法，又蒙蔽了不，这里啥也没干，就跑了。

你跑，那我就追！

### **`LifecycleRegister`** 

```java
/**
     * Sets the current state and notifies the observers.
     * <p>
     * Note that if the {@code currentState} is the same state as the last call to this method,
     * calling this method has no effect.
     *
     * @param event The event that was received
     */
public void handleLifecycleEvent(@NonNull Lifecycle.Event event) {
    State next = getStateAfter(event);
    moveToState(next);
}

private void moveToState(State next) {
    if (mState == next) {
        return;
    }
    mState = next;
    if (mHandlingEvent || mAddingObserverCounter != 0) {
        mNewEventOccurred = true;
        // we will figure out what to do on upper level.
        return;
    }
    mHandlingEvent = true;
    sync();
    mHandlingEvent = false;
}
```

两个方法，我们翻译下注释

> 设置当前状态，并通知观察者
>
> 注意，如果当前状态和上一次方法调用时相同，那么这次调用则无效

#### `getStateAfter()`

现在我们来分析源码，`getStateAfter(event)` 这个方法，我们先进去看下做了什么：

```java
static State getStateAfter(Event event) {
    switch (event) {
        case ON_CREATE:
        case ON_STOP:
            return CREATED;
        case ON_START:
        case ON_PAUSE:
            return STARTED;
        case ON_RESUME:
            return RESUMED;
        case ON_DESTROY:
            return DESTROYED;
        case ON_ANY:
            break;
    }
    throw new IllegalArgumentException("Unexpected event value " + event);
}
```

原来是一个静态方法，通过传入的 `Event` 事件，找到当前事件对应的下一个生命周期状态 `State`



我们还有一个方法没有分析 `moveToState(State next)`, 从函数名上，可以看出，这是一个状态移动的方法，具体是什么呢，我们进入方法内可以看到 

``` java
if (mState == next) {
	return;
}
```

如果当前状态和下一个（操作后的）状态一致，则直接 `return` 这也映照了注释中的那句话。

#### `sync()`

继续就是将操作的下一个状态做了一次记录，中间的一些判断条件我们不看，顺序的会看到一个 `sync()` 方法，咦，这又是什么呢？===> 状态同步

```java
/**
     * Custom list that keeps observers and can handle removals / additions during traversal.
     *
     * Invariant: at any moment of time for observer1 & observer2:
     * if addition_order(observer1) < addition_order(observer2), then
     * state(observer1) >= state(observer2),
     */
private FastSafeIterableMap<LifecycleObserver, ObserverWithState> mObserverMap =
    new FastSafeIterableMap<>();
// happens only on the top of stack (never in reentrance),
// so it doesn't have to take in account parents
private void sync() {
    LifecycleOwner lifecycleOwner = mLifecycleOwner.get();
    if (lifecycleOwner == null) {
        throw new IllegalStateException("LifecycleOwner of this LifecycleRegistry is already"
                                        + "garbage collected. It is too late to change lifecycle state.");
    }
    while (!isSynced()) {
        mNewEventOccurred = false;
        // no need to check eldest for nullability, because isSynced does it for us.
        if (mState.compareTo(mObserverMap.eldest().getValue().mState) < 0) {
            backwardPass(lifecycleOwner);
        }
        Entry<LifecycleObserver, ObserverWithState> newest = mObserverMap.newest();
        if (!mNewEventOccurred && newest != null
            && mState.compareTo(newest.getValue().mState) > 0) {
            forwardPass(lifecycleOwner);
        }
    }
    mNewEventOccurred = false;
}
```

这里出现了一个新东西 `mObserverMap` 向上我们找他的它类型，这里对数据结构不做研究，简单说一下，它是一个双向链表，并提供了一个 map 做缓冲区，且提供了一个可以快速迭代的结构。

继续分析源码

`mState.compareTo(mObserverMap.eldest().getValue().mState) < 0` 从缓存的观察者中拿出最旧的状态，与当前状态进行比较，如果小于 0， 说明观察者的状态提前于当前状态，那么就执行一个`backwardPass(lifecycleOwner)` 方法，让观察者的状态回退到当前状态上

` mState.compareTo(newest.getValue().mState) > 0` 这个判断正好和上面相反，说明当前的观察者状态落后于当前状态，那么就让观察者的状态追上当前状态，执行 `forwardPass(lifecycleOwner)`

#### **`Lifecycle State Sequence`**

通过分析 `forwardPass` 和 `backwardPass` 方法，我们看到其内部又调用了两个方法, `downEvent` 和 `upEvent`，我们称呼为升级事件和降级事件

```java
 private static Event downEvent(State state) {
        switch (state) {
            case INITIALIZED:
                throw new IllegalArgumentException();
            case CREATED:
                return ON_DESTROY;
            case STARTED:
                return ON_STOP;
            case RESUMED:
                return ON_PAUSE;
            case DESTROYED:
                throw new IllegalArgumentException();
        }
        throw new IllegalArgumentException("Unexpected state value " + state);
    }

    private static Event upEvent(State state) {
        switch (state) {
            case INITIALIZED:
            case DESTROYED:
                return ON_CREATE;
            case CREATED:
                return ON_START;
            case STARTED:
                return ON_RESUME;
            case RESUMED:
                throw new IllegalArgumentException();
        }
        throw new IllegalArgumentException("Unexpected state value " + state);
    }
```

通过上面两个方法，我们总结出 `Lifecycle` 中 `State` 和 `Event` 的时序关系，如下图

![Lifecycle State Sequence](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/Lifecycle%20State%20secquece.png?token=GHSAT0AAAAAABTDT2CDBOU4HSB3VVATEM5GYSNOROQ)

同时我们也回顾一下，`getStateAfter()` 方法，对事件和状态的判断，也就明白了状态和事件的关系。

#### `dispatchEvent`

```java
private void forwardPass(LifecycleOwner lifecycleOwner) {
    Iterator<Entry<LifecycleObserver, ObserverWithState>> ascendingIterator =
        mObserverMap.iteratorWithAdditions();
    while (ascendingIterator.hasNext() && !mNewEventOccurred) {
        Entry<LifecycleObserver, ObserverWithState> entry = ascendingIterator.next();
        ObserverWithState observer = entry.getValue();
        while ((observer.mState.compareTo(mState) < 0 && !mNewEventOccurred
                && mObserverMap.contains(entry.getKey()))) {
            pushParentState(observer.mState);
            observer.dispatchEvent(lifecycleOwner, upEvent(observer.mState));
            popParentState();
        }
    }
}

private void backwardPass(LifecycleOwner lifecycleOwner) {
    Iterator<Entry<LifecycleObserver, ObserverWithState>> descendingIterator =
        mObserverMap.descendingIterator();
    while (descendingIterator.hasNext() && !mNewEventOccurred) {
        Entry<LifecycleObserver, ObserverWithState> entry = descendingIterator.next();
        ObserverWithState observer = entry.getValue();
        while ((observer.mState.compareTo(mState) > 0 && !mNewEventOccurred
                && mObserverMap.contains(entry.getKey()))) {
            Event event = downEvent(observer.mState);
            pushParentState(getStateAfter(event));
            observer.dispatchEvent(lifecycleOwner, event);
            popParentState();
        }
    }
}
```

迟到的两个方法终于来了，这里也没有什么可以复杂的。只是通过循环找到所有的观察者，并进行事件的分发`observer.dispatchEvent(lifecycleOwner, event)`

```java
void dispatchEvent(LifecycleOwner owner, Event event) {
    State newState = getStateAfter(event);
    mState = min(mState, newState);
    mLifecycleObserver.onStateChanged(owner, event);
    mState = newState;
}
```

哈哈， 又是一个方法进入了我们的视线 `onStateChanged(owner, event)`，再次点击去后，发现是一个接口。查询可以看到有很多实现类，困惑吗？？？？

但我们只需要关注 `ReflectiveGenericLifecycleObserver` , 想知道为什么吗？ 我也是看了源码才总结出来的。

#### `ReflectiveGenericLifecycleObserver`

```java
/**
 * An internal implementation of {@link LifecycleObserver} that relies on reflection.
 */
class ReflectiveGenericLifecycleObserver implements LifecycleEventObserver {
    private final Object mWrapped;
    private final CallbackInfo mInfo;

    ReflectiveGenericLifecycleObserver(Object wrapped) {
        mWrapped = wrapped;
        mInfo = ClassesInfoCache.sInstance.getInfo(mWrapped.getClass());
    }

    @Override
    public void onStateChanged(LifecycleOwner source, Event event) {
        mInfo.invokeCallbacks(source, event, mWrapped);
    }
}
```

哎，`mInfo.invokeCallbacks(source,event,mWrapped);` 这又是什么，捋下来还从没见过，我们也没见过这个类的初始化和加载过程，对不对😨😨😨

既然是类嘛，那肯定是要创建的，那就看下构造器呗。

`wrapped` 这东西，经过了缓存，Emmm ，我也是点进去 `ClassesInfoCache` 之后，都了它的注释才明白的。

那 `wrapped` 又是什么呢？通过 `ClassesInfoCache` 和我们追踪 `ReflectiveGenericLifecycleObserver` 可以看出， `ClassesInfoCache` 缓存了 `LifecycleObserver` 的类对象，`ReflectiveGenericLifecycleObserver` 也是向下传递一个 `LifecycleObserver`。由此我们可以判断出，其实这个 `LifecycleObserver` 就是我们自己定义的观察者。

而系统帮我做的事儿，就是使用反射技术，通过我们自己标注的注解，并根据当前生命周期的状态，反射执行我们的方法 `mInfo.invokeCallback(source event, mWrapped);`

#### `reflect invoke method`

```java
void invokeCallback(LifecycleOwner source, Lifecycle.Event event, Object target) {
    //noinspection TryWithIdenticalCatches
    try {
        switch (mCallType) {
            case CALL_TYPE_NO_ARG:
                mMethod.invoke(target);
                break;
            case CALL_TYPE_PROVIDER:
                mMethod.invoke(target, source);
                break;
            case CALL_TYPE_PROVIDER_WITH_EVENT:
                mMethod.invoke(target, source, event);
                break;
        }
    } catch (InvocationTargetException e) {
        throw new RuntimeException("Failed to call observer method", e.getCause());
    } catch (IllegalAccessException e) {
        throw new RuntimeException(e);
    }
}
```

还记得文章开头对 `Lifecycle` 注解的翻译吗？ 这里的判断就是依据其注解标注，并回调对应的参数方法

至此，似乎我们已经不能再追下去了，代码执行到这里已经结束了。

但是！！！！！！！！！！！！！！！！

我们还有一大块没有分析！！！！！！！！！！！！！！！！！！！！！！！！

#### `addObserver()`

前面我们说了一大堆，都是对 `Lifecycle` 如何处理，并监听我们的生命周期的方法，也就是 `Lifecycle`是如何处理监听的。那么我们前面一直都没有说过，观察者那里来的？？？？？？？？？

好，我们继续观察 `LifecycleRegister` 中的 `addObserver(LifecycleObserver)` 这个也是我们自定义观察者后，需要调用的方法

```java
@Override
public void addObserver(@NonNull LifecycleObserver observer) {
    State initialState = mState == DESTROYED ? DESTROYED : INITIALIZED;
    ObserverWithState statefulObserver = new ObserverWithState(observer, initialState);
    ObserverWithState previous = mObserverMap.putIfAbsent(observer, statefulObserver);

    if (previous != null) {
        return;
    }
    LifecycleOwner lifecycleOwner = mLifecycleOwner.get();
    if (lifecycleOwner == null) {
        // it is null we should be destroyed. Fallback quickly
        return;
    }

    boolean isReentrance = mAddingObserverCounter != 0 || mHandlingEvent;
    State targetState = calculateTargetState(observer);
    mAddingObserverCounter++;
    while ((statefulObserver.mState.compareTo(targetState) < 0
            && mObserverMap.contains(observer))) {
        pushParentState(statefulObserver.mState);
        statefulObserver.dispatchEvent(lifecycleOwner, upEvent(statefulObserver.mState));
        popParentState();
        // mState / subling may have been changed recalculate
        targetState = calculateTargetState(observer);
    }

    if (!isReentrance) {
        // we do sync only on the top level.
        sync();
    }
    mAddingObserverCounter--;
}
```

哈哈，看起来代码并不是很多丫！！！！   哼，天真的你！但它就是这么多

我们这里要逐行清点

`State initialState = mState == DESTROYED ? DESTROYED : INITIALIZED;` 嗯，一上来就初始化了一个 `INITIALIZED` 状态的状态，哈哈哈，好拗口。

随后创建了一个 `ObserverWithState` ，这是一个有状态的观察者，从名字上我们就可以看出来。两个参数分别是我们传入的观察者和我们刚刚创建好的状态。这是个装饰器模式，目的是给原对象，增加一个新属性，但又不改变原数据结构的方案。

紧接着又把这个观察者和带有状态的观察者，放进了事先已经创建好的 `Map` 中，也就是 `mObserverMap` 然后返回了个东西， 阅读后发现，又和 `Lifecycle` 的注释对上了。

之后，计算出当前 `Activity` 或 `Fragment` 的状态，并判断，如果当前观察者的状态落后于 `Activity` 或 `Fragment` 的状态，则立即执行`dispatchEvent()` 方法，执行回调。



## 总结

认真阅读源码后，我们能够看出，其实 `Lifecycle` 的技术很简单，只有**反射**，**观察者**，**装饰器**，它将这三个东西应用的很神。

总结一下，分析源码我们从两方面入手

1. `addObserver()`

    这个方法是对用户最直接的内容，当我们创建一个 `Observer` 后，都会通过 `add` 的方式，将我们自己定义的观察者传入，那么从这个突破口我们进入源码分析观察到

   1. 给要添加的`Observer` 一个初始的状态（装饰器模式，包装数据）
   2. 将数据存储再本地缓存中 （`mObserverMap`）
   3. 立即进行状态判断，决定是否处理生命周期变化

2. `ReportFragment`

   作用是，附着再 `Activity` 上，用来感知 `Activity` 的生命周期变化，也起到将业务从 `Activity` 中分离出来。通过生命感知生命周期的变化，执行 `dispatch()` 方法，将生命周期事件分发给它所有的观察者去处理消息 `handleLifecycleEvent`

3. **反射**

   这里的东西比较抽象，没有任何内容是能看出来和我们有什么关系的， 只要你熟悉反射，那么你就能明白它再做什么。

4. `sync()`

   这个方法是用来快速同步观察者状态与 `Activity` 和 `Fragment`  ，目的也是能够让观察者执行到它所有观察的数据。两个方法 `forwardPass()` 和 `backwardPass()`  是其实现的原理。
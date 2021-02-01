---
title: Handler 消息机制
tags: Android
category: Handler
---



Handler 消息机制，在整个 Android 系统中，有着很重要的地位。

他可以帮助我们实现，子线程和主线程的跨线程通信；可以帮助我们发送一些延时任务，帮助我们很好的实现一个 App.

本文旨在对源码进行预览分析。

## UML 类图

先来一张结构图，让我们清晰的了解一下，我们下面都会分析到哪些内容；也了解一下 `Handler` 机制的核心秘密。

![Handler 类图](https://github.com/xiaomanwong/static_file/blob/master/images/Handler%20%E6%9C%BA%E5%88%B6.png?raw=true)

<!-- more -->

#### **类图分析**

从上面的类图我们可以看出，整个 Handler 消息机制，所涉及到的核心内容，只有 3 个类

**Message：** 消息，这个是我们要执行任务的载体，当我们需要 Handler 帮我做事的时候，就会向 Handler 发送一个 Message。

**Handler:**     这个是对我们比较直观的一个类，通常都会在代码中创建一个新的 Handler 来使用

**Looper:** 	  这个类，如果不点进去，我们也是看不到这，它也是整个 Handler 消息通信机制的*大心脏*

## ActivityThread

看过源码后我们能知道，一个 App 的启动流程的入口就在 ActivityThread 的 `main()` 方法中。

在这里系统帮我做了系统进程的 fork 工作，为我们的 app 开辟了一块空间。并帮我们初始化了  `application` 和 `activity` 的工作,接下来我们看一下源码：

```java
public static void main(String[] args) {
    Trace.traceBegin(Trace.TRACE_TAG_ACTIVITY_MANAGER, "ActivityThreadMain");

    // Install selective syscall interception
    AndroidOs.install();

    // CloseGuard defaults to true and can be quite spammy.  We
    // disable it here, but selectively enable it later (via
    // StrictMode) on debug builds, but using DropBox, not logs.
    CloseGuard.setEnabled(false);

    Environment.initForCurrentUser();

    // Make sure TrustedCertificateStore looks in the right place for CA certificates
    final File configDir = Environment.getUserConfigDirectory(UserHandle.myUserId());
    TrustedCertificateStore.setDefaultUserDirectory(configDir);

    Process.setArgV0("<pre-initialized>");

    Looper.prepareMainLooper();

    // Find the value for {@link #PROC_START_SEQ_IDENT} if provided on the command line.
    // It will be in the format "seq=114"
    long startSeq = 0;
    if (args != null) {
        for (int i = args.length - 1; i >= 0; --i) {
            if (args[i] != null && args[i].startsWith(PROC_START_SEQ_IDENT)) {
                startSeq = Long.parseLong(
                    args[i].substring(PROC_START_SEQ_IDENT.length()));
            }
        }
    }
    ActivityThread thread = new ActivityThread();
    thread.attach(false, startSeq);

    if (sMainThreadHandler == null) {
        sMainThreadHandler = thread.getHandler();
    }

    if (false) {
        Looper.myLooper().setMessageLogging(new
                                            LogPrinter(Log.DEBUG, "ActivityThread"));
    }

    // End of event ActivityThreadMain.
    Trace.traceEnd(Trace.TRACE_TAG_ACTIVITY_MANAGER);
    Looper.loop();

    throw new RuntimeException("Main thread loop unexpectedly exited");
}
```

通过上面的代码，我主要分析 `Looper.prepareMainLooper()` 和 `Looper.loop()`

## Looper

### Looper.prepare()

这里的标题虽然不是 `prepareMainLooper()`  的一个主要原因是他们的核心内容是一样的，只不过，`prepareMainLooper()` 是系统帮我们创建了要给不可退出的`Looper`，而 `prepare()` 方法创建的 `Looper` 是可以退出的。

```java
/**
     * Initialize the current thread as a looper, marking it as an
     * application's main looper. The main looper for your application
     * is created by the Android environment, so you should never need
     * to call this function yourself.  See also: {@link #prepare()}
     */
public static void prepareMainLooper() {
    prepare(false);
    synchronized (Looper.class) {
        if (sMainLooper != null) {
            throw new IllegalStateException("The main Looper has already been prepared.");
        }
        sMainLooper = myLooper();
    }
}
/** Initialize the current thread as a looper.
      * This gives you a chance to create handlers that then reference
      * this looper, before actually starting the loop. Be sure to call
      * {@link #loop()} after calling this method, and end it by calling
      * {@link #quit()}.
      */
public static void prepare() {
    prepare(true);
}

private static void prepare(boolean quitAllowed) {
    if (sThreadLocal.get() != null) {
        throw new RuntimeException("Only one Looper may be created per thread");
    }
    sThreadLocal.set(new Looper(quitAllowed));
}
```

### ThreadLocal

说到 `Looper` 的创建工作，这里就需要讲一下 `ThreadLocal` ， 它的意思是**帮助我们在自己线程中保存一份它自己的本地变量**

```java
@UnsupportedAppUsage
static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
```

也就是说，在 Looper 创建的过程中，我们将 Looper 对象，保存到当前线程中，并做到每个线程中只有一个 Looper 对象，起到线程之间隔离作用。

面试中经常会问到一个线程有且只有一个 Looper 的问题，原因也在这里。系统通过 ThreadLocal 帮我们限制了。

### loop()

继续看源码，` Looper.loop();` 的出现，标志了系统开启了一个循环开始处理消息，跑到这里，基本上我们的 app 已经可以正常运行

这部分的源码比较长，捡主要的看和说：

```java
/**
     * Run the message queue in this thread. Be sure to call
     * {@link #quit()} to end the loop.
     */
public static void loop() {
    final Looper me = myLooper();
    if (me == null) {
        throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
    }
    //..............
    final MessageQueue queue = me.mQueue;
    for (;;) {
        Message msg = queue.next(); // might block
        if (msg == null) {
            // No message indicates that the message queue is quitting.
            return;
        }
        //..............
        try {
            msg.target.dispatchMessage(msg);
        } catch (Exception exception) {
            throw exception;
        } finally {
          
        }
        // ...............
        msg.recycleUnchecked();
    }
}
```

ActivityThread 中的 `main()` 方法，在最后一行，执行了我们的 `Looper.loop()` 方法， 进入后，我们可以看到 `loop()` 方法内部是一个死循环，当然，这里我们需要回顾一下 ActivityThread 帮我们初始化的 `prepareMainLooper()`  ，这也是系统帮我们创建的一个主线程`main` 。

接下来就慢慢分析一下 `loop` 都做了什么事情

![looper.loop()](https://github.com/xiaomanwong/static_file/blob/master/images/loop%20for.png?raw=true?raw=true)

从流程图上，我们简述了一下 `loop()` 方法，都做了些什么事情，下面就展开讲都做了什么

1. 首先获取当前线程的 looper 对象，如果不存在，则抛出异常
2. 接着获取当前 Looper 绑定的消息队列` MessageQueue`
3. 进入循环，开始获取消息 `queue.next()`
4. 调用 `msg.target.dispathMessage(msg)` 分发消息
5. msg.recycleUnchecked()

## Handler

**作用：**

`Handler` 暴露给开发这的功能一共就两块

* 发送消息
* 处理消息

### 发送消息

* sendMessage(Message msg)
* sendMessageEmpty()
* sendMessageAtTime(Message msg, long uptimeMillis)
* sendMessageDelay(Message msg, long delay)
* post(Runnable r)
* ...

所有的发送消息的方法，最终都会去执行`sendMessageAtTime(Message msg, long uptimeMillis)`, 当我们创建一个`Handler` 对象时, 会从当前线程的 Looper 中获取当前的消息队列`mQueue`

```java
public Handler(@Nullable Callback callback, boolean async) {
        if (FIND_POTENTIAL_LEAKS) {
            final Class<? extends Handler> klass = getClass();
            if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
                    (klass.getModifiers() & Modifier.STATIC) == 0) {
                Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                    klass.getCanonicalName());
            }
        }

        mLooper = Looper.myLooper();
        if (mLooper == null) {
            throw new RuntimeException(
                "Can't create handler inside thread " + Thread.currentThread()
                        + " that has not called Looper.prepare()");
        }
        mQueue = mLooper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }
```

当我们开始发送一条消息时，调用 `sendMessageAtTime` ，会将消息压入到消息队列中，

```java
final MessageQueue mQueue;

public boolean sendMessageAtTime(@NonNull Message msg, long uptimeMillis) {
        MessageQueue queue = mQueue;
        if (queue == null) {
            RuntimeException e = new RuntimeException(
                    this + " sendMessageAtTime() called with no mQueue");
            Log.w("Looper", e.getMessage(), e);
            return false;
        }
        return enqueueMessage(queue, msg, uptimeMillis);
    }

private boolean enqueueMessage(@NonNull MessageQueue queue, @NonNull Message msg,
            long uptimeMillis) {
        msg.target = this;
        msg.workSourceUid = ThreadLocalWorkSource.getUid();

        if (mAsynchronous) {
            msg.setAsynchronous(true);
        }
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```

通过源码我们看到，在压入队列前，我们会将当前的 `Handler` 对象赋值给 `Message` 中的 `target` ，这也就是为什么 `message` 中会持有 `Handler` 的引用的原因。

### 处理消息

在说处理消息之前，我们先看一下 `Handler` 对**消息的分发**

```Java
 /**
     * Handle system messages here.
     */
    public void dispatchMessage(@NonNull Message msg) {
        if (msg.callback != null) {
            handleCallback(msg);
        } else {
            if (mCallback != null) {
                if (mCallback.handleMessage(msg)) {
                    return;
                }
            }
            handleMessage(msg);
        }
    }
```

* 当我们给 `Message` 设置了 `callback` 时，会直接触发 `Message` 的 `callback` 逻辑
* 如果我们在创建 `Handler` 时，有设置过 `Callback` ，则会调用由我们传入进来的 `Callback` 方法
* 如果以上两种情况都没有设置，那么会触发 `Handler` 自己 `handleMessage()` 方法

```java
/**
     * Subclasses must implement this to receive messages.
     */
    public void handleMessage(@NonNull Message msg) {
    }
```

通过源码的注解我们可以看出，当我们继承/创建一个 `Handler` 时，需要我们必须去实现的一个方法（前提是你需要它）

`dispatchMessage` 最终时由 `loop()` 方法在拿取消息队列中的信息时，获取到 `Message` 对象， 通过 `Message` 持有的 `target` 调用。

### 移除消息

这里我们需要注意，当我们使用 `Handler` 处理消息时，通常都是一些异步任务，这时创建 `Handler` 一般都为内部类，此时需要注意的是，在 Java 中，内部类是会持有外部类的引用， 那么在 Handler 中处理的消息如果长时间无法得到释放， 那么会造成 `Activity` 无法被回收的情况。处理这种情况的方案就是，在 `Activity` 销毁时，我们需要将 `Handler` 中的消息进行释放

```java
    public final void removeCallbacksAndMessages(@Nullable Object token) {
        mQueue.removeCallbacksAndMessages(this, token);
    }
```



## Message

一种消息的载体，其中包含 `handler` 对象和一个任意类型的对象以及两个 int 型的参数

```java
public final class Message implements Parcelable {
    /**
     * 用户自定义的消息身份代码，每一个 Handler 都有它自己的命名空间，因此我们不需要担心会和其他的 Handler 混淆 
     */
    public int what;

    /**
     * arg1 and arg2 是一个低成本的替代方案，当我们只需要发送一些 int 型的数据时，可以使用， 避免使用 Object 增加内存的开销
     */
    public int arg1;

     /**
     * arg1 and arg2 是一个低成本的替代方案，当我们只需要发送一些 int 型的数据时，可以使用， 避免使用 Object 增加内存的开销
     */
    public int arg2;
    
    /**
     * 任意的消息类型载体，如果是序列化的数据，则一定不能为 null，其他的数据类型，可以使用 setData(Bundle bundle) 
     */
    public Object obj;
    /**
     * 消息的执行时间
     */
    public long when;
}
```

`Message` 本身是一个**链表** 的数据结构，这种数据结构，在`MessageQueue` 中获取消息时，可以有效的针对 `Handler` 发送进来的消息进行排序。

```java
    @UnsupportedAppUsage
    /*package*/ Handler target;

    @UnsupportedAppUsage
    /*package*/ Runnable callback;

    // sometimes we store linked lists of these things
    @UnsupportedAppUsage
    /*package*/ Message next;
```

`Message` 持有了一个 `Handler` 对象，因此即使我们在同一个线程里面创建了多个 `Handler` 的对象， 也不会出现消息错乱的现象。

**Callback**

同时 Message 也支持设置 `Callback` 方便开发者在处理消息时可以快速的查看处理方案，但这种方法其实个人认为在开发阶段不适合使用。这会导致消息处理到处飞，不利于代码的管理。

#### 构造器

```java
 	private static Message sPool;
    private static int sPoolSize = 0;

    private static final int MAX_POOL_SIZE = 50;   

	/** Constructor (but the preferred way to get a Message is to call {@link #obtain() Message.obtain()}).
    */
    public Message() {
    }

	public static Message obtain() {
        synchronized (sPoolSync) {
            if (sPool != null) {
                Message m = sPool;
                sPool = m.next;
                m.next = null;
                m.flags = 0; // clear in-use flag
                sPoolSize--;
                return m;
            }
        }
        return new Message();
    }
```

`Message` 为我们提供了一个空的构造器去创建一个对象，但这种方案系统却不建议我们使用，而是建议我们通过 `obtain()` 函数去获取。通过 `obtain()` 函数我们可以看出， `Message` 自身维护了一个对象池，池的最大值为 50。因此我们不难看出，当我们通过空构造器去创建一个 `Message` 对象时，反而是增加了系统的内存开销，而 `Message` 为我们提供的利器得不到发挥。

#### 回收

```java
    public void recycle() {
        if (isInUse()) {
            if (gCheckRecycle) {
                throw new IllegalStateException("This message cannot be recycled because it "
                        + "is still in use.");
            }
            return;
        }
        recycleUnchecked();
    }
```

当一个消息处于不在被使用（Handler 触发 remove 时），或已经使用完成（MessageQueue 触发），那么系统会清空 `Message` 中的全部内容，并将对象丢向消息池中，等待再次被使用( obtain())，当消息被回收时，我们不能在去调用它，否则会出现空指针的情况。

## MessageQueue

存放所有消息的容器，既然是 `Queue` 命名，那自然就是一个队列，拥有先入先出的特性，但消息的存放，并不是由其自己操作，而是通过与 `Looper` 关联的 `Handler` 添加

### 入队

由 `Handler` 触发，将数据压入到队列中

```java
boolean enqueueMessage(Message msg, long when) {
    

        synchronized (this) {
            msg.markInUse();
            msg.when = when;
            Message p = mMessages;
            boolean needWake;
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                msg.next = p;
                mMessages = msg;
                needWake = mBlocked;
            } else {
                // Inserted within the middle of the queue.  Usually we don't have to wake
                // up the event queue unless there is a barrier at the head of the queue
                // and the message is the earliest asynchronous message in the queue.
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                Message prev;
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }

            // We can assume mPtr != 0 because mQuitting is false.
            if (needWake) {
                nativeWake(mPtr);
            }
        }
        return true;
    }
```

通过源码看出，在消息压入队列中时，发生了排序操作，

当一条消息进来时，判断了如果当前队列内没有消息，或者传入的消息延时执行时间为0，或者传入的消息执行时间小于队列的第一条消息时，将 `Message` 放置在链表头部位置。否则则循环取出每条消息，依据消息的执行时间进行排序，将新消息压入到适当的位置。

### 出队

```java
Message next() {
   
    for (;;) {
        if (nextPollTimeoutMillis != 0) {
            Binder.flushPendingCommands();
        }

        nativePollOnce(ptr, nextPollTimeoutMillis);

        synchronized (this) {
            // Try to retrieve the next message.  Return if found.
            final long now = SystemClock.uptimeMillis();
            Message prevMsg = null;
            Message msg = mMessages;
            // 开启同步屏障，直到找到下一个异步消息结束，目的是优先执行异步消息
            if (msg != null && msg.target == null) {
                // Stalled by a barrier.  Find the next asynchronous message in the queue.
                do {
                    prevMsg = msg;
                    msg = msg.next;
                } while (msg != null && !msg.isAsynchronous());
            }
            if (msg != null) {
                if (now < msg.when) {
                    // 为到执行时间，设置下一次系统唤醒消息需要的时间
                    // Next message is not ready.  Set a timeout to wake up when it is ready.
                    nextPollTimeoutMillis = (int) Math.min(msg.when - now, Integer.MAX_VALUE);
                } else {
                    // Got a message.
                    mBlocked = false;
                    if (prevMsg != null) {
                        // prevMsg ，即是同步消息，
                        prevMsg.next = msg.next;
                    } else {
                        mMessages = msg.next;
                    }
                    msg.next = null;
                    if (DEBUG) Log.v(TAG, "Returning message: " + msg);
                    msg.markInUse();
                    return msg;
                }
            } else {
                // No more messages.
                nextPollTimeoutMillis = -1;
            }
        }
    }
}
```

#### 同步屏障

一般是由系统发出，多数情况是用来处理`View` 的刷新，由`ViewRootImpl` 调用 `postSyncBarrier`，将消息插入到链表的头部，我们可以注意到 `msg` 的 `target` 对象为空，因为 每一个 `Message` 对象都持有一个 target 对象，因此这里很不合常理，但这里就是系统的黑魔法，专门用来处理同步消息，因为同步消息的优先级高于所有异步消息。

```java
private int postSyncBarrier(long when) {
        // Enqueue a new sync barrier token.
        // We don't need to wake the queue because the purpose of a barrier is to stall it.
        synchronized (this) {
            final int token = mNextBarrierToken++;
            // 创建一个同步消息
            final Message msg = Message.obtain();
            msg.markInUse();
            msg.when = when;
            msg.arg1 = token;

            Message prev = null;
            Message p = mMessages;
            if (when != 0) {
                // 队列中的消息执行时间，排序，找到消息执行时间大于当前系统时间
                while (p != null && p.when <= when) {
                    prev = p;
                    p = p.next;
                }
            }
            if (prev != null) { // invariant: p == prev.next
                // 断开链表，将同步消息，插入到要立即执行的消息后面
                msg.next = p;
                prev.next = msg;
            } else {
                // 没有要立即执行的消息，将同步消息插入到链表第一个节点
                msg.next = p;
                mMessages = msg;
            }
            return token;
        }
    }
```



当我们创建一个 Handler 时，默认创建的都是一个异步的（当然也可以创建同步的，调用对应的构造器就可以），因此在这里当收到一个同步消息时，`ViewRootImpl` 会，并给 msg 的 `target` 重新赋值，优先执行。直到找到一个异步消息为止

当从队列中获取一条异步消息后，我们将消息取出来，并将消息的 next 置空断开链表，标记当前消息正在使用，并且返回。如果消息还没有到达执行的时间，则会通知系统去等待，设置下一次唤醒的时间。

### 退出

由 `loop` 调用，当一个 loop 被销毁时，会触发该方法，用来清空内部所有消息,并回收

```java
void quit(boolean safe) {
        if (!mQuitAllowed) {
            throw new IllegalStateException("Main thread not allowed to quit.");
        }

        synchronized (this) {
            if (mQuitting) {
                return;
            }
            mQuitting = true;

            if (safe) {
                removeAllFutureMessagesLocked();
            } else {
                removeAllMessagesLocked();
            }

            // We can assume mPtr != 0 because mQuitting was previously false.
            nativeWake(mPtr);
        }
    }
```


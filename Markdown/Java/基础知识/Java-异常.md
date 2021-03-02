---
title: Java 异常
tag: Java
categories: Java
---

**Crash** 应用崩溃，是由于代码异常而导致 APP 非正常退出，导致应用程序无法正常使用，所有工作都停止的现象。

发生 **Crash** 后需要重新启动应用（有些情况也会自动重启），而且不管应用在开发阶段做得多么优秀，也无法避免 **Crash** 的放生，在 **Android** 系统中，系统碎片化比较严重，各 **Rom** 之间的差异，设置系统的 BUG ，都可能导致 **Crash** 的发生。

在 **Android** 应用 中发生 **Crash** 有两种类型： Java 层的 Crash 和 Native 的 Crash。这两种 **Crash** 的监控和获取堆栈信息有所不同。

<!-- more -->

## Java Crash

Java 的 Crash 监控非常简单，**Java 中的 Thread 定义了一个接口： `UncaughtExceptionHandler` , 用于处理未捕获的异常导致线程的终止（catch 了的是捕获不到）**，当应用发生了 Crash 的时候，就会走 `UNcaughtExceptionHandler.uncaughtException` ，该方法中可以获取到异常的信息，我们通过 `Thread.setDefaultUncaughtExceptionHandler` ，该方法来设置线程的默认异常处理器，我们可以将异常信息保存到本地或者上传到服务器，方便我们快速定位问题。

```java
public class CrashHandler implements Thread.UncaughtExceptionHandler {
    private static final String FILE_NAME_STUFFIX = ".trace";
    private static Thread.UncaughtExceptionHandler mDefaultCrashHandler;
    private static Context mContext;
    
    private CrashHandler(){}
    
    public static void init(Context context) {
        mDefaultCrashHandler = Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler(this);
        mContext = context.getApplicationContext();
    }
    
    /**
     * 当程序中有未捕获异常，系统将会调用这个方法
     */
    @Override
    public void uncaughtException(Thread t, Throwable e) {
        try {
            // 自行处理，可以保存到本地，也可以上传到后台
            File file = dealException(e);
            
        } catch (Exception e1) {
            e1.printStackTrace();
        } finally {
            // 交给系统默认程序处理，否则会重复自启动
            if(mDefaultCrashHandler != null) {
                mDefaultCrashHandler.uncaughtException(t, e);
            }
        }
    }
    
    /**
     * 导出异常到 SD 卡
     */
     private File dealException(Thread t, Throwable e) throw Exception {
         String time = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
         File f = new File(mContext.getExternalCacheDir().getAbsoluteFile(), "crash_info");
         if(!f.exists()) {
             f.mkdirs();
         }
         File crashFile = new File(f, time+ FILE_NAME_SUFFIX);
         // 向文件中写入数据,可以自定义存储内容，尽量详细方便我们快速定位问题
         PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(f)));
         pw.println(time);
         pw.println("Thread:" + t.getName());
         e.printStackTrace(pw);// 写入 crash 堆栈
         pw.flush();
         pw.close();
         return f;
     }
}
```

## NDK Crash

### Linux 信号机制

信号机制是 Linux 进程间通信的一种重要方式，Linux 信号一方面用于正常的进程间通信和同步，另一方面还负责监控系统异常及中断。当应用程序运行异常是， Linux 内核将产生错误信号并通知当前进程。当前进程在接收到该错误信号后，可以有三种不同的处理方式：

* 忽略该信号
* 捕捉该信号并执行对应的信号处理函数（信号处理程序）
* 执行该信号的缺省操作（如终止进程）

当 Linux 应用程序在执行时发生严重错误，一般会导致程序崩溃。其中 Linux 专门提供了一类 crash 信号，在程序接收到该信号时，缺省操作时将崩溃的线程信息记录到核心文件，然后终止进程。

常见的崩溃信号列表：

* **SIGSEGV: ** 内存引用无效
* **SIGBUS: ** 访问内存对象的未定义部分
* **SIGFPE: ** 算数运算错误
* **SIGILL: ** 非法指令，如执行垃圾或特权指令
* **SIGSYS: ** 糟糕的系统调用
* **SIGXCPU: ** 超过 CPU 时间限制
* **SIGXFSZ: ** 文件大小限制

一般出现崩溃信号， Android 系统会默认缺省操作时直接退出程序。但是系统允许我们给某一个进程的某一个特定信号注册一个相应的处理函数（singal） ，即对该信号的默认处理动作进行修改。因此 NDK Crash 的监控可以采用这种信号机制，捕获崩溃信号执行我们自己的信号处理函数，从而捕获 NKD Crash。



### BreakPad

[Google breakpad](https://github.com/google/breakpad) 是一个跨平台的崩溃转储和分析框架和工具的集合。 breakpad 在 Linux 中的实现就是借助了 Linux 信号捕获机制实现的。因为其实现为  C++, 在 Android 中必须要借助 NDK 工具。

 [Crash监控.pdf](..\..\技术文档\Crash监控.pdf) 
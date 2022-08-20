# Android 拦截 Push 通知

## 注意事项

* 是否真的有使用场景

* 注册系统服务，Service 只能存活 5s，时间有限，尽量不要做太多和耗时任务

* service 中存在 context 对象，可获取当前进程上下文

* 每次当通知栏有消息变化时，当前 Service 都会被动唤醒一次，也拉活了进程，存活时间在 5s。是否能够符合隐私及合规检测。

## 注册系统 NotificationListenerService

继承 `NotificationListenerService`, 在这里设置通知栏上的应用包名，根据自己需要拦截的目标**包名**，做好区分。

```java
class NotifyService : NotificationListenerService() {

    private val TAG = "NotifyService"

    var context:Context? = null
    override fun attachBaseContext(base: Context?) {
        super.attachBaseContext(base)
        this.context = base
        Log.d("wangxu3", "NotifyService ===> attachBaseContext() called with: base = $base")
    }
    
    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        super.onNotificationPosted(sbn)
    }

   /**
    * 收到状态栏通知
    */
    override fun onNotificationPosted(sbn: StatusBarNotification?, rankingMap: RankingMap?) {
        super.onNotificationPosted(sbn, rankingMap)

        val appWidgetManager = AppWidgetManager.getInstance(context)
        val componentName = context?.let { ComponentName(it, TrulyClockCustom::class.java) }
        val remoteViews =
            RemoteViews(sbn?.packageName, R.layout.widget_clock_custom)
        remoteViews.setTextViewText(R.id.tv_name, "${sbn?.notification?.tickerText}" + System.currentTimeMillis())
        appWidgetManager.updateAppWidget(componentName, remoteViews)
    }
    /**
     * 状态栏通知被移除
     */
    override fun onNotificationRemoved(sbn: StatusBarNotification?) {
        super.onNotificationRemoved(sbn)
        Log.d("wangxu3", "NotifyService ===> onNotificationRemoved() called with: sbn = $sbn")
    }

    override fun onNotificationRemoved(sbn: StatusBarNotification?, rankingMap: RankingMap?) {
        super.onNotificationRemoved(sbn, rankingMap)
        Log.d(
            "wangxu3",
            "NotifyService ===> onNotificationRemoved() called with: sbn = $sbn, rankingMap = $rankingMap"
        )
    }

    override fun onNotificationRemoved(sbn: StatusBarNotification?, rankingMap: RankingMap?, reason: Int) {
        super.onNotificationRemoved(sbn, rankingMap, reason)
        Log.d(
            "wangxu3",
            "NotifyService ===> onNotificationRemoved() called with: sbn = $sbn, rankingMap = $rankingMap, reason = $reason"
        )
    }
}
```

## 向系统注册监听服务
```xml
        <!--通知监听服务-->
        <service
            android:name=".NotifyService"
            android:enabled="true"
            android:label="测试通知服务"
            android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE">
            <intent-filter>
                <action android:name="android.service.notification.NotificationListenerService" />
            </intent-filter>
        </service>
```

## 打开通知服务监听
使用这个服务，需要用户授权应用允许监听通知栏，在设备上是一个开关。

```java
	/**
     * 是否启用通知监听服务
     * @return
     */
    public boolean isNLServiceEnabled() {
        Set<String> packageNames = NotificationManagerCompat.getEnabledListenerPackages(this);
        if (packageNames.contains(getPackageName())) {
            return true;
        }
        return false;
    }

    	/**
     * 切换通知监听器服务
     *
     * @param enable
     */
    public void toggleNotificationListenerService() {
        PackageManager pm = getPackageManager();
        pm.setComponentEnabledSetting(new ComponentName(getApplicationContext(), NotifyService.class),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED, PackageManager.DONT_KILL_APP);

        pm.setComponentEnabledSetting(new ComponentName(getApplicationContext(), NotifyService.class),
                PackageManager.COMPONENT_ENABLED_STATE_ENABLED, PackageManager.DONT_KILL_APP);
    }

    private static final int REQUEST_CODE = 9527;
	/**
     * 请求权限
     *
     * @param view
     */
    public void requestPermission(View view) {
        if (!isNLServiceEnabled()) {
            startActivityForResult(new Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"), REQUEST_CODE);
        } else {
            showMsg("通知服务已开启");
            toggleNotificationListenerService(true);
        }
    }
```




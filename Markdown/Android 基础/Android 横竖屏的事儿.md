---
title: *Activity* 横竖屏
tag: Android View
---


## 设置屏幕的方向

| 值               | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| unspecified      | 默认值，系统自动选择屏幕方向                                 |
| behind           | 跟 Activity 堆栈中的下面一个 activity 方向一致               |
| landscape        | 横屏方向，                                                   |
| portraint        | 竖屏方向                                                     |
| sensor           | 由设备的物理方向传感器决定，如果用户旋转设备，着屏幕就会横竖切换 |
| nosensor         | 忽略物理传感器，这样就会不会随着用户旋转设备而横竖屏切换了   |
| user             | 用户当前首选方向                                             |
| reverseLandscape | 反向横屏                                                     |
| reversePortrait  | 反向竖屏                                                     |
| sensorLandscape  | 横屏，但可以根据物理传感器方向来切换正反向横屏               |
| sensorPortraint  | 竖屏，但可以根据物理传感器方向来切换真反向竖屏               |
| fullSensor       | 上下左右四个方向，由物理方向传感器决定                       |
| locked           | 锁死当前屏幕方向                                             |

<!-- more -->

**第一种**

在 `AndroidManifest` 清单文件中设置 `Activity` 的方向

```xml
<activity
          android:name=".view.main.MainActivity"
          android:screenOrientation="portrait">
		<intent-filter>
    		<action android:name="android.intent.action.MAIN"/>
             <category android:name="android.intent.category.LAUNCHER"/>
    	</intent-filter>
</activity>
```

这样在横竖屏切换时，不会重新创建 `Activity`

**第二种**

```java
setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
```

**Android  android:configChanges**

如果我们不配置 `configuration` ，当 `configuration` 发生变化时， activity 会自动处理它。反之，如果我们配置了响应的 `configuration` ，当新的 `configuration` 发生变化时，会回调 Activity  的 `onConfigurationChanged()` 方法

| 值             | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| keyboardHidden | 键盘的可访问性发生变化--例如：用户发现了硬件键盘             |
| orientation    | 屏幕方向发生变化--用户旋转了屏幕。<br />注意：如果应用程序的目标 API 级别是 13 或更高，也需要生命配置项 screenSize ，因为这将在设备选择肖像和屏幕方向是发生变化 |
| screenLayout   | 屏幕布局发生变化-- 这回导致显示不同的 Activity。<br />屏幕方向发生变化-- 用户旋转了屏幕 |
| screenSize     | 当前可用屏幕大小发生变化。代表当前可用大小发生变化，和当前比率相关。这个变化不会影响 Activity 重启。 |
|                |                                                              |

在 Android 3.2 之后，进行下列配置，横竖屏切换时不会创建新的 Activity，但是回调用 `onConfigurationChanged()` 方法

```xml
<activity
          android:name=".view.main.MainActivity"
          android:configChanges="keyboardHidden|orientation|screenSize">
	<intent-filter>
    	<action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>
```

在 3.2 以前，我们需要这样配置

`android:configChagnes="keyboardHidden|orientation"`

```xml
<activity
          android:name=".view.main.MainActivity"
          android:configChanges="keyboardHidden|orientation">
	<intent-filter>
    	<action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>
```

## 小结

当我们配置了上面的内容

* 竖屏 —> 横屏 `onConfigurationChanged()` 调用一次
* 横屏 —> 竖屏 `onConfigurationChanged()` 调用一次

因此我们要进行相应的处理

```java
public void onConfigurationChaged(Configuration newConfig) {
    super.onConfigurationChanged(newConfig);
    if(this.getResource(0.getConfiguration().orientation == Configuration.ORIENTATION_LANDSCAPE)) {
        // 加入横屏要处理的代码
    } else if(this.getResource().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT){
        // 加入竖屏处理代码
    }
}
```

**如果同时设置了 `android:configChanges="keyboardHidden|orientation|screen" 和 android:screenOrientation="portrait"` 会如何呢？**

> 如果我们打开系统的自动旋转屏幕，旋转屏幕系统不会发生变化，也不会调用 Activity 的 `onConfigurationChanged` 方法
>
> 当我们手动调用 setRequestedOrientation() 方法去改变屏幕方向的时候，还是会调用 onConfigurationChanged() 方法的

## 扩展

### 设置全屏模式

```java
// 去掉ActionBar
requestWindowFeature(Window.FEATURE_NO_TITLE);
// 设置全屏
getWindow().setFlag(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
```

**在实际项目中，我们通常都会固定我们应用的屏幕方向，只对一些特定的需要切换屏幕的 Activity 做处理。那么如何统一设置屏幕方向呢**

1. 复制粘贴，在 `AndroidManifest` 清单文件中为每一个 Activity 标签增加设置

   ```xml
   <activity android:name=".MainActivity"
             android:screenOrientation="portrait"/>
   ```

2. 以为在 `AppTheme` 里面设置 `android:screenOrientation` ，但是没有效果，查阅官方文档才看到

   > Specify the orientation an activity should be run in. If not specified, it will run in the current preferred orientation of the screen. This attribute is supported by the <activity> element.
   >
   > 也就是说， android:screenOrientation 只对 activity 标签生效

3. 在 BaseActivity里面动态设置

   ```java
   public class BaseActivity extends AppCompatActivity {
       @Override
       public void onCreate(BUndle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
       }
   }
   ```

### 利用系统的加载机制自动帮我们加载相应布局

如果我们在 `res` 中添加 `layout-land` (横向布局文件) 和 `layout-port` （竖向布局文件) ，重启 Activity 模式的横竖屏切换

**当我们设置了 Activity 的方向为竖屏或者横屏的时候，旋转屏幕并不会重新调用 Activity 的各个生命周期，那么要如何检测？**

那我们就利用我们的传感器，然后根据传感器旋转的方向做相应的处理

```java
// 注册重力传感器， 屏幕旋转
mSm = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
mSensor = mSm.getDefaultSensor(Sensor.TYPE_ACCELLEROMETER);
mSm.registerListener(mOrientationSensorListener, mSensor, SensorManager.SENSOR_DELAY_UI);
```

```java
public class OrientationSensorListener implements SensorEventListener {
    private static final int _DATA_X = 0;
    private static final int _DATA_Y = 1;
    private static final int _DATA_Z = 2;
    
    public static final int ORIENTATION_UNKNOWN = -1;
    private boolean sensor_flag = true;
    
    public static final String TAG = "XUJUN";
    
    int mLastAngle = -1;
    
    AngleChangeListener mAngleChangleListener;
    
    public OrientationSensorListener(AngleChangleListener angleChangeleListener) {
        mAngleChangeleListener = andleChangleListener;
    }
    
    @Override
    public void onAccuracyChanged(Sensor arg0, int arg1) {
        // TODO Auto-generated method stub
    }
    
	@Override
    public void onSensorChanged(SensorEvent event) {
        float[] values = event.values;
        int orientation = ORIENTATION_UNKNOWN;
        float x = -values[_DATA_X];
        float y = -values[_DATA_Y];
        float z = -values[_DATA_Z];
        
        
        /**
         * 这一段是 Android 源码里面拿出来的计算屏幕旋转的
         */
        float magnitude = X * X + Y * Y;
        if(magnitude * 4 >= Z * Z) {
            // 屏幕旋转时
            float oneEightyOverPi = 57.29577956855f;
            float angle = (float) Math.atan2(-Y, Z) * oneEightOverPi;
            orientation = 90 - (int)Math.round(angle);
            
            while(orientation >= 360) {
                orientation -= 360;
            }
            while(orientation < 0) {
                orientation +=  360;
            }
        }
        
        if(orientation > 225 && orientation < 315) { // 横屏
            sensor_flag = false;
        } else if ((orientation > 315 && orientation < 360) 
                   || (orientation > 0 && orientation < 45)) { // 竖屏
            sensor_flag = true;
        }
        
        if(mLastAndgle != orientation && mAngleChangeListener != null) {
            mAndleChangleListener.onChange(orientation);
            mLastAngle = orientation;
        }
    }
}
```



###  **设备旋转时保存 Activity 的交互状态**



![Activity生命周期](https://upload-images.jianshu.io/upload_images/2050203-8435a89f42cd9508?imageMogr2/auto-orient/strip|imageView2/2/w/513/format/webp)

如果我们不配置 Activity 的方向，或者 Activity 的 `android:configchange` 属性时，每次旋转屏幕，Activity 都会重新创建，那我们要保存我们的当前状态

> 我们可以考虑在 `onPause()` 和 `onStop()`  里面保存我们相应的数据，再从 `onCreate()` 方法里判断 `savedInstanceState` 是否有缓存过我们的数据就可以。至于选择在 `onPause()` 还是 `onStop()` 保存数据，具体的下需求分析。 `onPause()` 在界面失去焦点的时候会调用， `onStop()` 在界面完全看不见的时候调用

```java
private static final String KEY_INDEX = "index";
private int mCurrentIndex = 0;

@Override
protected void onCreate(Bundle savedInstanceState) {
    if(savedInstanceState != null) {
        mCurrentIndex = savedInstanceState.getInt(KEY_INDEX, 0);
    }
}

@Override
protected void onPause(Bundle outState) {
    super.saveInstanceState(outState);
    outState.putInt(KEY_INDEX, mCurrentIndex);
}
```

**生命周期变化**

> onPause-> onStop -> onDestory -> onCreate -> onStart -> onResume


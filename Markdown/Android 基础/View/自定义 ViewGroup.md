---
title: 自定义 ViewGroup
tag: View
category: Android
---



## View Group 的测量布局流程

**View Group绘制和布局流程中的重点**

1. View 在 `onMeasure` 方法中进行自我测量和保存。

2. ViewGroup 循环遍历调用所有子 view 的 onMeasure 方法，利用 onMeasure 方法计算出来的大小，来确定这些 子 View 最终可以占用的大小和所处布局的位置

3. 关注 onMeasure 和 onLayout

4. 父 View 调用子 View 的layout 方法的时候，会把之前 measure 阶段确定的位置和大小都传递给子 View

5. 自定义 View/ViewGroup，只需要关注下面三种需求：

   1. 对于已有的 Android 自带 View，我们只需要重写他的 `onMeasure` 方法即可,**修改一下这个尺寸就完成需求**
   2. 对于 Android 系统没有的，属于我们自定义的 View，需要完全重写 `onMeasure`
   3. 需要重写 `onMeasure` 和 `onLayout` 2个方法，来完成一个复杂的 `ViewGroup` 的测量和布局。

6. onMeasure 的说明

   widthMeasureSpec, heightMeasureSpec  两个参数主要是 父 view 对子view 的尺寸限制

7. 理解父 view 对子 view 的限制

   实际上，父 View 对子 View 的限制据大多数就来自于我们开发者所设置的 layout 开头的这些属性。**这些以 layout 开头的属性，都是设置给父 view 看的**

   > 父 View 要知道这些属性以后，才知道要对子view 的测量加以什么限制


<!-- more -->

## 自定义 BannerView

```java
public class BannerImageView extends ImageView{
    // 宽高比
    float ratio;
    public BannerImageView(Context context) {
        super(context);
    }
    
    public BannerImageView(Context context, AttributeSet attrs) {
        super(context, attrs);
        TypedArray array = context.obtainStyledAttributes(attrs, R.styleable.BannerImageView);
        ratio = array.getFloat(R.styleable.BannerImageView_ratio, 1.0f);
        array.recycle();
    }
    
    @Override
    public void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        // 自己的测量走一遍，因为这个方法内部会调用 setMeasureDimension() 来保存测量结果
        // 只有保存了以后，才能取得这个测量结果，否则获取不到
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        
        // 获取测量结果
        int tempWidth = getMeasureWidth();
        int tempHeight = (int) (tempWidth * ratio);
        // 保存以后，父 view 可以拿到这个测量的宽高了。不保存是拿不到的
        setMeasureDimension(tempWidth, tempHeight);
    }
}
```

## 自定义 View ，完全自己写 onMeasure 方法

对于完全自定义  View ，完全自己写的 onMeasure 方法，保存的宽高必须符合父 View 的限制，否则会发生 bug，保存父 View 对子 View 的限制的方法就是直接调用 `resolveSize` 方法即可。

```java
public static int resolveSizeAndState(int size, int measureSpec, int childMeasureState) {
    final int specMode = MeasureSpec.getMode(measureSpec);
    final int specSize = MeasureSpec.getSize(measureSpec);
    final int result;
    switch(specMode) {
        case MeasureSpce.AT_MOST:
            if(specSize < size) {
                result = specSize | MEASURED_STATE_TOO_SMALL;
            } else {
                result = size;
            }
            break;
        case MeasureSpec.EXACTLY:
            result = specSize;
            break;
        case MeasureSpec.UNSPECIFIED:
        default:
            result = size;
    }
    return result | (childMeasureState * MEASURED_STATE_MASK);
}
```

完全自定义 view onMeasure 方法：

1. 先算自己想要的宽高
2. 直接拿 `resolveSize` 方法处理一下
3. 最后 `setMeasuredDimension` 保存

```java
public class LoadingView extends View {
    // 圆的半径
    int radius;
    // 外部矩形的起点
    int left = 10, top = 30;
    
    Paint mPaint = new Paint();
    public LoadingView(Context context) {
        super(context);
    }
    
    public LoadingView(Context context, AttributeSet attrs) {
        super(context, attrs);
        TypedArray typedArray = context.obtainStyledAttributes(attrs, R.styleable.LoadingView);
        radius = typedArray.getInt(R.styleable.LoadingView_radius, 0);
    }
    
    @Override
    public void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        
        int width = left + radius * 2;
        int height = top + radius * 2;
        
        // 一定要用 resolveSize 方法来格式化 View 的宽高，否则遇到某些 layout 的时候一定会出现器官的 bug
        // 不用这个，就完全没有父 View 的感受
        width = resolveSize(width, widthMeasureSpec);
        height = resolveSize(height, heightMeasureSpec);
        setMeasuredDimension(width, height);
    }
    
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        
        // 画矩形
        RectF oval = new Rectf(left, top ,left + radius * 2, top + radius * 2);
        mPaint.setColor(Color.BLUE);
        canvas.drawRect(oval, mPaint);
        // 画圆弧
        mPaint.setColor(Color.RED);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeWidth(2);
        canvas.drawArc(oval, -90, 360, false, mPaint);
    }
}
```

## 自定义 ViewGroup

注意以下几点：

1. 一定要先重写 onMeasure 确定子 View 的宽高和自己的宽高以后，才可以继续写 onLayout 对这些子 View 进行布局
2. ViewGroup 的 onMeasure 其实就是遍历自己的 view ，对自己的每一个子 View 进行 measure，据大多数的时候对子 View 的measure 都可以直接调用  measureChild() 这个方法
3. 计算出 View Group 自己的尺寸并保存，`onMeasuredDinmension`
4. 逼不得已需要重写`measureChild` 的时候，无非就是对父 view 的测量和子 View 的测量，做一个取舍关系而已，可参照 `measureChild` 方法。

```java
/**
 * 从左到右布局，如果不够放，就直接另起一行layout
 */
public class SimpleFlowLayout extends ViewGroup {
    public SimpleFlowLayout(Context context) {
        super(context);
    }
    
    public SimpleFlowLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
    
    /**
     *	layout 算法，就是不够放，就另外放一行
     * 
	 *  无非就是前面 onMeasure 结束以后，你可以拿到所有子 View 和自己的测量宽高，
     */
    @Override
    public void onLayout(boolean changed, int l, int t, int r, int b) {
        int childTop = 0;
        int childLeft = 0;
        int childRight = 0;
        int childBottom = 0;
        
        // 已使用的 width
        int usedWidth = 0;
        // customlayout 自己可使用的宽度
        int layoutWidth = getMeasuredWidth();
        
        for(int i = 0; i < getChildCount(); i++) {
            View childView = getChildAt(i);
            // 取得这个子 View 要求的宽度和高度
            int childWidth = childView.getMeasuredWidth();
            int childHeight = childView.getMeasuredHeight();
            
            // 如果宽度不够，就另外启动一行
            if(layoutWidth - usedWidth < childWidth) {
                childLeft = 0;
                usedWidth = 0;
                childTop += childHeight;
                childBottom = childTop + childHeight;
                childView.layout(0, childTop, childRight, childBottom);
                usedWidth = usedWidth + childWidth;
                childLeft = childWidth;
                continue;
            }
            childRight = childLeft + childWidth;
            childBottom = childTop + childHeight;
            childView.layout(childLeft, childTop, childRight, childBottom);
            childLeft += childWidth;
            usedWidth += childWidth;
        }
    }
    
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        // 先取出 SimpleFlowLayout 的父 View 对他的测量限制
        // 只有知道了自己的宽高，才能限制子 View 的宽高
        int widthMode = MeasureSpec.getMode(widthMeasureSpec);
        int heightMode = MeasureSpec.getMode(heightMeasureSpec);
        
        int widthSize = MeasureSpec.getSize(widthMeasureSpec);
        int heightSize = MeasureSpec.getSize(heightMeasureSpec);
        
        int usedWidth = 0; // 已使用宽度
        int remaining = 0;	// 剩余可用宽度
        int totalHeight = 0; // 总高度
        int lineHeight = 0; // 当前行高
        
        for(int i = 0; i< getChildCount(); i++) {
            View childView = getChildAt(i);
            LayoutParams lp = childView.getLayoutParams();
            
            // 先测量子View
            measureChild(childView, widthMeasureSpec, heightMeasureSpec);
            // 然后计算以下宽度里面，还有多少是可用的，也就是剩余可用宽度
            remaining = widthSize - usedWidth;
            
            // 如果一行不够放，也就是说这个子 View 测量的宽度，大于这一行剩下的宽度时，我们要另外启动一行
            if(childView.getMeasuredWidth > remaining) {
                // 另外启动一行
                usedWidth = 0;
                totalHeight += lineHeight;
            }
            
            // 已使用 width 进行累加
            usedWidth += childView.getMeasuredWidth();
            // 当前 view 的高度
		   lineHeight = childView.getMeasuredHeight();
            
    	}
        // 如果 SimpleFlowLayout 的高度为 wrap_content  的时候，采用我们叠加的高度，否则我们当然用父对其的限制高度
        if(heightMode == MeasureSpec.AT_MOST) {
            heightSize = totalHeight;
        }
        
        setMeasuredDimension(widthSize, heightSize);
    }
}
```


---
title: RandomLayout 随机摆放布局
tag: View
category: Android
---



随机摆放布局，先上效果

![image-20210208162638517](https://raw.githubusercontent.com/xiaomanwong/static_file/master/images/image-20210208162638517.png?token=GHSAT0AAAAAABTDT2CCOJSFYSEAEUFZPJREYSNPRJQ)

在有效空间内，随机摆放子 View ，并保障子 View 不会重叠。类似的需求，在开发过程中也会经常遇到。从图中看，随机摆放，那就不能使用常规的 `LinearLayout` `RelateLayout` 或者是 `RecyclerView` 这些。因为他们都不满足随机性。
<!--more -->

### 分析

首先，我们需要一个容器，`ViewGroup` `LinearLayout` 都可以给我们选择

然后，重写布局函数，确认宽高、测量子 View 等

其次，我们要保证随机性，那么就需要一个 `Random` 函数，并存储各个子 View 的坐标，确认重复性

最后，布局子 View

### 实现

1. 创建一个 `RandomLayout` 继承 `LinearLayout`
2. 重写 `onMeasure` 计算父布局及子布局的宽高和模式，并存储
3. 重写 `onLayout` ，计算子 View 位置以及判定是否重合
   1. 创建一个 `ArrayList<Point>` 用来存储子 View 的左顶点坐标，摆放时，遍历集合，找到重合立即重新生成，没有则继续
   2. 重合判定条件； `abs(rPoint.x - oPoint.x) <= childWidth && abs(rPoint.y - oPoint.y) <= childHeight`, 意思是说：两个点的横纵距离均小于当前 View 的 宽和高 
4. 布局子 View



```kotlin
class RandomLayout(context: Context, attributes: AttributeSet) : LinearLayout(context, attributes) {
    private var mWidth: Int = 0
    private var mHeight: Int = 0
    private var childWidth: Int = 0
    private var childHeight: Int = 0
    private val childPointList = ArrayList<Point>(20)

    /**
     * onMeasure 获得上下容器的宽和高及计算模式
     */
    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
        mWidth = MeasureSpec.getSize(widthMeasureSpec)
        mHeight = mWidth/* * 3 / 2*/
        // 测量所有的 childView 宽和高
        setMeasuredDimension(mWidth, mHeight)
        measureChildren(widthMeasureSpec, heightMeasureSpec)
    }

    /**
     * 布局，循环子 view ，并为其布局
     */
    override fun onLayout(changed: Boolean, left: Int, top: Int, right: Int, bottom: Int) {
        super.onLayout(changed, left, top, right, bottom)
        // 获取所有子 View 的总数
        // 循环设置每一个子View的位置
        for (index in 0 until childCount) {
            val child = getChildAt(index)
            childWidth = child.measuredWidth
            childHeight = child.measuredHeight
            // 获取 xy 坐标
            layoutChild(child, index)
        }
    }

    /**
     * 子 View 布局
     */
    private fun layoutChild(child: View, index: Int) {
        // 先随机生成一个坐标点，然后判断是否有重叠，重叠则重新生成新的点
        var rPoint = randomPointFactory()
        if (index > 0) {// 第一个点不需要处理
            while (isOverLapping(rPoint)) {
                // 判断有没有重叠的部分，如果有就返回 true， 重新创建并比较
                rPoint = randomPointFactory()
            }
        }
        
        if (childPointList.size != childCount) {
            // 把没有重合的店放到集合中去
            childPointList.add(rPoint)
        }
        child.layout(rPoint.x, rPoint.y, rPoint.x + childWidth, rPoint.y + childHeight)
    }

    private fun randomPointFactory(): Point {
        // 随机获取俩个数，作为每个子View的左上角坐标，最大为父布局的 XY 最小为 0
        val random = Random
        val x: Int = random.nextInt(mWidth - childWidth) % ((mWidth - childWidth) - 1 + 1) + 1
        val y: Int = random.nextInt(mHeight - childHeight) % ((mHeight - childHeight) - 1 + 1) + 1
        return Point(x, y)
    }
	// 重叠判定
    private fun isOverLapping(rPoint: Point): Boolean {
        childPointList.indices.forEach { index ->
            val oPoint = childPointList[index]
            if (abs(rPoint.x - oPoint.x) <= childWidth && abs(rPoint.y - oPoint.y) <= childHeight) {
                return true
            }
        }
        return false
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        childPointList.clear()
    }

    fun addChildView(item: View) {
        addView(item)
        invalidate()
    }


}
```


---
title: RecyclerView 总结
tag: View
category: Android
---



## List View 的局限性

1. 只有纵向列表一种布局
2. 没有支持动画的  API
3. 接口设计和系统不一致
   1. setOnItemClickListener()
   2. setOnItemLongClickListener()
   3. setSelection()
4. 没有强制实现 ViewHolder
5. 性能不如 RecyclerView

<!-- more -->

## RecyclerView 优势

1. 默认支持 Linear、Grid、Staggered Grid 三种布局
2. 友好的 ItemAnimator 动画 API
3. 强制实现 ViewHolder
4. 解耦的架构设计
5. 相对 ListView 性能更好

 



![image-20200709164241306](https://github.com/xiaomanwong/static_file/blob/master/images/image-20200709164241306.png?raw=true)



Recycler View： 负责将 Datas 展示在自己身上，其本身是一个 ViewGroup，只认识 View，因此需要一个 Adapter 来将 Datas 的内容转换为 View

Adapter： 负责翻译，将 Datas 内容，转换为 View，方便 RecyclerView 展示

ViewHolder： RecyclerView 只会与 ViewHolder 进行交互，因此 ViewHolder 充当中间件，来将 Datas 的内容传递给  RecyclerView

LayoutManager：负责布局，RecyclerView 将其子 View 的布局管理，交给它来完成

Recycler：负责管理 View 的生命周期，LayoutManager 只管负责 View 的布局任务，对其回收交给了 Recycler 来处理，避免造成不必要的错误

ItemAnimator： 负责动画，当 RecyclerView 中的数据发生变化（增、删等）都会通过它来完成平滑的过渡



## RecyclerView 的绘制

RecyclerView 无疑也是一个 View ，View 的绘制同样逃离不了三大步骤 `onMeasure()` `onLayout()` `onDraw()` 



### onMeasure

LayoutManager 负责 RecyclerView 的绘制，其有一个 `mAutoMeasure` 属性，用来控制是否开启自动测量，开启情况下，布局交由 `RecyclerView` 使用一套默认的测量机制；否则，自定义的 LayoutManager 需要重写 `onMeasure` 来处理自身的测量工作。

#### **自动测量原理：**

当 RecyclerView 的宽高都为 `EXACTLY` 时， 可以直接设置对应的宽高，然后返回，结束测量

如果宽高都不时 `EXACTLY` 则会在 `onMeasure` 中开始布局的处理。

RecyclerView.State 这个类封装了当前 RecyclerView 的信息。State 中的一个变量 `mLayoutStep` 记录了 RecyclerView  当前的布局状态

* STEP_START
* STEP_LAYOUT
* STEP_ANIMATIONS

对应的， RecyclerView 的布局过程也分为三步，STEP_START 表示开始布局，对应需要调用 `dispatchLayoutStep1()` 来执行第一步布局，结束后， `mLayoutStep` 变为 STEP_LAYOUT ，表示接下来需要调用 `dispatchLayoutStep2()` 进行布局，结束后 `mLayoutStep` 变为 STEP_ANIMATIONS, 继续执行第三步 `dispatchLayoutStep3()`



* dispatchLayoutStep1:  负责记录状态

* dispatchLayoutStep2：负责布局
* dispatchLayoutStep3：与 step1 比较，根据变化来触发动画



### onLayout

```java
protected void onLayout(boolean changed, int l int t, int r, int b) {
    TraceCompat.beginSection(TRACE_ON_LAYOUT_TAG);
    dispatchLayout();
    TraceCompat.endSection();
    mFirstLayoutComplete = true;
}

void dispatchLayout() {
    mState.mIsMeasuring = false;
    if(mState.mLayoutStep == State.STEP_START) {
        dispatchLayoutStep1();
        mLayout.setExactMeasureSpecsFrom(this);
        dispatchLayoutStep2();
    } else if(mAdapterHelper.hasUpdates() 
              || mLayout.getWidth() != getWidth() 
              || mLayout.getHeight() != getHeight()) {
        // first 2 steps are done in onMeasure but looks like we have to run again due to changed size
        mLayout.setExactMeasureSpecsFrom(this);
        dispatchLayoutStep2();
    } else {
        // always make sure we sync them (to ensure mode is exact)
        mLayout.setExactMeasureSpecsFrom(this);
    }
    
    dispatchLayoutStep3();
}
```

通过 `dispatchLayout` 可以验证RecyclerView 的 layout三步走原则，如果在 `onMeasure` 中已经完成了 step1 和 step2 ，则只会执行 step3，否则，会在 `onLayout` 中依次触发三步走。

#### dispatchLayoutStep1

```java
private void dispatchLayoutStep1(){
	if(mState.mRunSimpleAnimations) {
        int count = mChildHelper.getChildCount();
        for(int i = 0; i < count; i++) {
            final ViewHolder holder = getChildViewHolderInt(mChildHelper.getChildAt(i));
            final ItemHolderInfo animationInfo = mItemAnimator.recordPreLayoutInformation(mState, holder, ItemAnimator.buildAdapterChangeFlagsForAnimations(holder), holder.getUnmodifiedPayloads());
            mViewInfoStore.addToPreLayout(holder, animationInfo);
        }
    }
    mState.mLayoutStep = State.STEP_LAYOUT
}
```

step 的第一步目的就是记录 View 的状态，先遍历当前所有 View，一次进行处理，mItemAnimator 会根据每个 View 的信息，封装一个 ItemHolderInfo, 这个 ItemHolderInfo 中主要包含的就是 View 的位置状态等。然后将 ItemHodlerInfo 存入 mViewInfoStore 中。在进入第二步后， View 的信息就将被改变

#### dispatchLayoutStep2

```java
private void dispatchLayoutStep2(){
    mLayout.onLayoutChildren(mRecycler, mState);
    
    mState.mLayoutStep = State.STATE_ANIMATIONS;
}
```

layout 的第二步就是真正的布局 View。RecyclerView 的真正布局是由 LayoutManger 来负责的，其主要工作也在 LayoutManager 中。

```java
public  void onLayoutChildren(RecyclerView.Recycler recycler, RecyclerView.State state) {
    
    if(!mAnchorInfo.mValid 
      || mPendingScrollPosition != NO_POSITION 
      || mPendingSavedState != null) {
        updateAnchorInfoForLayout(recycler, state, mAnchorInfo);
    }
    
    if(mAnchorInfo.mLayoutFromEnd) {
        firstLayoutDirection = mShouldReverseLayout 
            ? LayoutState.ITEM_DIRECTIONTAIL
            : LayoutState.ITEM_DIRECTION_HEAD;
    } else {
        firstLayoutDirection = mShouldReverseLayout 
            ? LayoutState.ITEM_DIRECTION_HEAD
            : LayoutState.ITEM_DIRECTION_TAIL;
    }
    
    onAnchorReady(recycler, state, mAnchorInfo, firstLayoutDirection);
    
    if(mAnchorInfo.mLayoutFromEnd) {
        
    } else {
        // fill towards end
        updateLayouStateToFillEnd(mAnchorInfo);
        fill(recycler, mLayoutState, state, false);
        
        // fill towards start
        updateLayoutStateToFillStart(mAnchorInfo);
        fill(recycler, mLayoutState, state, false);
    }
}
```

流程很负责，大致流程如下

* 找到 anchor点
* 根据 anchor 一直向前布局，直到填充满 anchor 点前面的所有区域
* 根据 anchor 一直向后布局，直到填充满 anchor 点后面的所有区域

anchor 点的寻找是由 `updateAnchorInfoForLayout` 函数负责。向下追踪会看到 `updateAnchorFromChildren`  方法，其内容为，先寻找被 focus 的 child， 找到以此 child 作为 anchor ，否则根据布局方向寻找最合适的 child 来作为 anchor，如果找到则将 child 的信息复制给 anchorInfo 。 `anchorInfo` 主要记录的信息就是 View 的物理位置与 Adapter 中的位置。找到后返回 true，否则返回 false，交给上一步函数做处理。

继续当找到 anchor 后，会根据 anchor 来布局，通过 fill 方法来完成

```java
int fill(RecyclerView.Recycler recycler, LayoutState layoutState, RecyclerView.state state, boolean stopOnFocusable) {
    final int start = layoutState.mAvailable;
    if(layoutState.mScrollingOffset != LayoutState.SCROLLING_OFFSET_NaN) {
        recycleByLayoutState(recycler, layoutState);
    }
    
    int remainingSpace = layoutState.mAvailable + layoutState.mExtra;
    LayoutChunkResult layoutChunkResult = mLayoutChunkResult;
    while((layoutState.mInfinite || remainingSpace > 0)
         && layoutState.hasMore(state)) {
        layoutChunk(recycler, state, layoutState, layoutChunkResult);
    }
    return start-layoutState.mAvailable;
}
```

**recycleByLayoutState** 这个函数，会根据当前信息对不需要的 View 进行回收:

```java
private void recycleByLayoutState(RecyclerView.Recycler recycler, LayoutState layoutState) {
    if(layoutState.mLayoutDirection == LayoutState.LAYOUT_START) {
        
    } else {
        recycleViewsFromStart(recycler, layoutState.mScrollingOffset);
    }
}
```

继续看 `recycleViewsFromStart`

```java
private void recycleViewsFromStart(RecyclerView.Recycler recycler, int dt){
    final int limit = dt;
    final int childCount = getChildCount();
    if(mShouldReverseLayout) {
        
    } else {
        for(int i = 0; i < childCount; i++){
            View child = getChildAt(i);
            if(mOrientationHelper.getDecoratedEnd(child) > limit
              || mOrientationHelper.getTransformedEndWithDecoration(child) > limit) {
        recycleChildren(recycler, 0, i);
                return;
            }
        }
    }
}
```

该函数的作用时遍历所有的子 View ,找出逃离边界的 View 进行回收，回收函数在 `recycleChildren` 里，而这函数又调用了 `removeAndRecycleViewAt` 

```java
public void removeAndRecycleViewAt(int index, Recycler recycler) {
    final View view = getChildAt(index);
    removeViewAt(index);
    recycler.recycleView(view);
}
```

该函数先调用 `removeViewAt` ，将 View 从 RecyclerView 中移除，紧接着是 recycler 执行了 View 的回收逻辑。在 fill 函数的一开始会去回收逃离出屏幕的 view。

```java
while((layoutState.mInfinite || remainningSpace > 0) 
     && layoutState.hasMore(state)) {
    layoutChunk(recycler, state, layoutState, layoutChunkResult);
}
```

只要又剩余空间，就会执行 layoutChunk 方法

```java
void layoutChunk(RecyclerView.Recycler recycler, RecyclerView.State stat, LayoutState layoutState, LayoutCHunkResult result){
    View view = layoutState.next(recycler);
    
    LayoutParams params = (LayoutParams) view.getLayoutParams();
    if(layoutState.mScrapList == null) {
        if(mShouldReverseLayout == (layoutState.mLayoutDirection == LayoutState.LAYOUT_START)) {
            addView(view);
        } else {
            addView(view, 0);
        }
    } else {
        
    }
    
    layoutDecoratedWithMargins(view, left, top, right, bottom);
}
```

在 layoutState 的 next 方法返回了一个 view， 凭空变出一个 View， 很神奇

```java
View next(RecyclerView.Recycler recycler ) {
    final View view = recycler.getViewForPosition(mCurrentPosition);
    return view;
}
```

可见 view 的获取逻辑也是由 recycler 来负责， 所以我们只需要清楚 recycler 可以根据位置返回一个 View 即可。

我们在看 layoutChunk 对刚刚生成的 View 的处理

```java
if(mShouldReverseLayout == (layoutState.mLayoutDirectoin == LayoutState.LAYOUT_STATE)) {
    addView(view);
} else {
    addView(view, 0);
}
```

明显的调用了 addView 方法，虽然这个方法是 LayoutManager 的，但是这个方法最终会多次辗转调用到 Recycler View 的 addView 方法，将 view 添加到 RecyclerView 中。

dispatchLayoutStep2 整个布局过程，完成了对 子 View 的测量与布局

#### dispatchLayoutStep3

最后一步

```java
private void dispatchLayoutStep3(){
    mState.mLayoutStep = State.STEP_START;
    if(mState.mRunSimpleAnimations) {
        for(int i = mChildHelper.getChildCount() - 1; i >= 0; i--) {
            final ItemHolderInfo animationInfo = mItemAnimator.recordPostLayoutInformation(mState, holder);
            mViewInfoStore.addToPostLayout(holder, animationInfo);
        }
        
        mViewInfoStore.process(mViewInfoProcessCallback);
    }
}
```

这里是与第一步呼应的，此时子 View 都已布局完成，所以子 View 的信息都发生了变化。第一步出现的 mViewInfoStore 和 mItemAnimator 再次登场，这次 mItemAnimator 调用的是 recordPostLayoutInformation 方法，而 mViewInfoStore 调用的是 addToPostLayout 方法，

```java
void addToPostLayout(ViewHolder holder, ItemHolderInfo info) {
    InfoRecord record = mLayoutHolderMap.get(holder);
    if(record == null ) {
        record = InfoRecord.obtain();
        mLayoutHolderMap.put(holder, record);
    }
    record.postInfo = info;record.flags |= FLAT_POST;
}
```

最后 mViewInfoStore 调用了 process 方法，根据 mViewInfoStore 中的 View 信息，来执行动画逻辑。



### 缓存逻辑



缓存共分为四层

1. Scrap  内存缓存
2. Cache 内存缓存: 不发生 bindView
3. ViewCacheExtension 用户自定义缓存
4. Recycled View Pool 缓存池

![img](https://pic2.zhimg.com/80/v2-a8d1b3f8f1d3b96db61ef34b3934c7b9_720w.jpg)

RecyclerView 的缓存时分为多级的，但其实真个逻辑很好理解，

```java
View getViewForPosition(int position, boolean dryRun) {
    boolean fromScrap = false;
    ViewHolder holder = null;
    if(mState.isPreLayout()) {
        holder = getChangedScrapViewForPosition(position);
		fromScrap = holder != null
    }
    
    if(hoder == null) {
        hodler = getScrapViewForPosition(position, INVALID_TYPE, dryRun);
    }
    
    if(holder == null ){
        final int offsetPosition = mAdapterHelper.findPositionOffset(position);
        final int type = mAdapter.getItemViewType(offsetPosition);
        if(mAdapter.hasStableIds()){
            holder = getScrapViewForId(mAdapter.getItemId(offsetPosition), type, dryRun);
        }
        
        if(holder == null && mViewCacheExtension != null) {
            final View view = mViewCacheExtension.getViewForPositionAndType(this, position, type);
        }
        
        if(holder == null) {
            // fallback to recycler
            holder = getRecyclerViewPool().getRecyclerView(type);
            if(holder != null){
                holder.resetInternal();
                if(FORCE_INVALIDATE_DISPLAY_LIST){
                    invalidateDisplayListInt(holder);
                }
            }
        } 
        
        if(holder == null ){
            holder = mAdapter.createViewHolder(RecyclerView.this, type);
        }
    }
    
    
    // 生成 LayoutParams 的代码
    return holder.itemView;
}
```

获取 View 的逻辑可以整理为

* 搜索 mChangedScrap， 如果找到则返回相应的 holder
* 搜索 mAttachedScrap与 mCachedViews， 如果找到且 holder 有效则返回相应的 holder
* 如果设置了 mViewCacheExtension, 对其调用 getViewForPositionAndType 方法进行获取，若返回结果则生成对应的 holder
* 搜索 mRecyclerPool, 如果找到则返回 Holder
* 如果上述过程都没有找到对饮的 holder, 则执行 Adapter.createViewHolder(); 创建新的 ViewHolder 实例

**对于 View 的回收**

```java
void recycleViewHolderInternal(ViewHolder holder ) {
    
    if(holder.isRecyclable()) {
        if(!holder.hasAnyOfTheFlags(VieHolder.FLAG_INVALID | ViewHolder.FLAG_REMOVED) | ViewHolder.FLAG_UPDATE) {
            int cachedViewSize = mCachedViews.size();
            if(cachedViewSize >= mViewCacheMax && cachedViewSize > 0) {
                recycleCachedViewAt(0);
                cachedViewSize--;
            }
            
            if(cachedViewSize < mViewCacheMax) {
                mCachedViews.add(holder);
                cached = true;
            }
        }
        
        if(!cached) {
            addViewHolderToRecycledViewPool(holder);
            recycled = true;
        }
    }
}
```

回收没有创建复杂，只涉及到两次缓存， mCachedViews 和 mRecyclerPool , mCachedViews 相当于一个先进先出的数据结构（队列），当有新的 View 需要缓存时，都会将新的 View 存入到 mCachedViews， 而 mCachedView  则会移除头部元素，并将头部元素存储在 mRecyclerPool 中， 即 mCachedViews 相当于一级缓存， mRecyclerPool 相当于二级缓存，并且 mRecyclerPool  时可以多个 RecyclerView 共享的。



## 与 AdapterView 比较

| index |      AdapterView      |                RecyclerView                |
| :---: | :-------------------: | :----------------------------------------: |
|   1   | Simple click listener |            OnItemTouchListener             |
|   2   |    Simple Divider     |               ItemDecoration               |
|   3   | ListView and GridView | LinearLayoutManager<br />GridLayoutManager |
|   4   |      RecyclerBin      |                  Recycler                  |
|   5   |   Header and Footer   |              Partial refresh               |

##### 点击事件

ListView 原生提供了Item 点击、长安的事件，而 RecyclerView  则需要使用 onTouchListener 相对比较复杂

##### 分割线

ListView  可以很轻松设施 Divider 属性来显示 item 之间的分割线，

RecyclerView 需要自己实现 ItemDecoration ，两者比较，前者使用更简单，后者定制性更强

##### 布局类型

AdapterView 提提供了 三种布局管理方式，LinearLayoutManager, GirdLayoutManager, StaggeredGirdLayoutManager

ListView 只提供了一种 LinearLayoutManager 方式

##### 性能优化

* RecyclerView 提供了DiffUtil 工具类，用于整个页面需要刷新，对比列表中的数据，如果未发生变化，则不会触发重绘制操作
* ListView 不支持单个 Item  的刷新，只能整个列表进行 `notifyDataSetChanged` ， RecyclerView 提供了 `itemChange`, `ItemInsert`, `ItemRemoved` 等方法，减少了 性能的开销




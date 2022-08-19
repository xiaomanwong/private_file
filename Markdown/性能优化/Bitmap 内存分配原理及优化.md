# Bitmap 内存分配原理及优化

一张图片在内存占用的空间究竟有多少，不取决于它本身的大小，而是决定于图片库锁采用的展示方式所申请的内存。

如一张 350 * 350 的图片，在磁盘占用上只有 36KB 的空间
![Img](https://segmentfault.com/img/remote/1460000040296316)

创建一个 Demo 显示这张图片
![Img](https://segmentfault.com/img/remote/1460000040296317)

通过 as 的 profile 分析，可以看到当前堆栈的使用情况
![Img](https://segmentfault.com/img/remote/1460000040296318)

可以看出 runtime 时，这张照片实际内存占用  2560000 bytes， 约 2.4 MB 内存。与实际大小相差了整整 70 倍。

https://segmentfault.com/a/1190000040296314
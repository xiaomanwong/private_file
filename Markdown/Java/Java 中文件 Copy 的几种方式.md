# Java 中文件 Copy 的几种方式

## Java.io

利用 `java.io` 类库。直接为源文件创建一个 `FileInputStream` 负责读取，然后再为目标文件创建一个 `FileOutputStream` 负责写入:

<!-- more -->

```java
public static void copyFileByStream(File source, File target) throws IOException {
    InputStream is = null;
    OutputStream os = null;
    try {
        is = new FileInputStream(source);
        os = new FileOutputStream(target);
        byte[] buffer = new byte[1024];
        int length;
        while((length = is.read(buffer)) > 0) {
            os.write(buffer, 0, length);
        }
    } 
}
```

## Java.nio

利用 `java.nio` 类库提供的 transferTo 或 transferFrom  方法实现

```java
public static void copyFileByChannel(File source, File target) throw IOException {
    try(FileChannel sc = new FileInputStream(source).getChannel();
       FileChannel tc = new FileOutputStream(target).getChannel();) {
        long count = sc.size();
        while(count > 0) {
            long transferred = sc.transferTo(sc.position(), count, tc);
            count -= transferred;
        }
    }
}
```

## Java.nio.file.File.copy 

关于 Copy 效率的问题，其实与操作系统和配置有关，总体来说 nio  transferTo/transferFrom 的方式可能更快，因为它更能利用现代操作系统底层机制，避免不必要拷贝和上下文切换。
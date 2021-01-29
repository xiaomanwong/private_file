---
title: Android Q 文件权限适配
date: 2020-03-11 20:11:41
tags:
---

随着 Android Q 的发布，随之而来的适配工作也在暗潮涌动，这里说一下 Android Q 文件存储；
Android Q 在外部存储设备中为每个应用提供了一个“沙盒”，任何其他应用都无法直接访问您的沙盒文件。由于文件是您应用的私有文件，因此您不在需要任何权限即可在外部存储设备中访问和保存自己的设备。这次更新有效的保证了用户文件的隐私性，也赚少了对应应用所需要的权限数量。

“沙盒”就是应用的专属文件，并且访问这个文件夹无需任何权限。Google 推荐应用的沙盒内存储文件地址为
`Context.getExternalFilesDir()` 下的文件夹。需要传入以下参数

```java
Environment.DIRECTORY_MUSIC
Environment.DIRECTORY_PODCASTS
Environment.DIRECTORY_RINGTONES
Environment.DIRECTORY_ALARMS
Environment.DIRECTORY_NOTIFICATIONS
Environment.DIRECTORY_PICUTRES
Environment.DIRECTORY_MOVIES
```
<!-- more -->

可根据具体需要，传入不通的参数。

```java

    /**
     * 获取一个文件通过文件夹类型
     *
     * @param fileName
     * @param boxType
     * @param defaultPath
     * @return
     * @throws FileNotFoundException
     */
    default File getFile(String fileName, String boxType, String defaultPath) throws FileNotFoundException {
        File file;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            file = getCurrentContext().getExternalFilesDir(boxType + File.separator + fileName);
        } else {
            file = new File(defaultPath + fileName);
        }
        if (file == null || !file.exists()) {
            throw new FileNotFoundException();
        }

        return file;
    }
```

**以上代码未经测试，忘见谅**

接下来说一下如何使用系统公共文件，比如相册，相机，下载目录等，这里以访问相册为例：

访问沙盒外(其他应用)的文件系统时，依然需要申请文件权限，`Manifest.permission.READ_EXTERNAL_STORAGE` 和 `Manifest.permission.WRITE_EXTERNAL_STORAGE` 

我们来看一下获取相册资源的代码：
```java
final Uri contentUri = MediaStore.Files.getContentUri("external");
            final String sortOrder = MediaStore.Files.FileColumns.DATE_MODIFIED + " DESC";
            final String selection =
                    "(" + MediaStore.Files.FileColumns.MEDIA_TYPE + "=?"
                            + " OR "
                            + MediaStore.Files.FileColumns.MEDIA_TYPE + "=?)"
                            + " AND "
                            + MediaStore.MediaColumns.SIZE + ">0";

            final String[] selectionAllArgs = {String.valueOf(MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE)};

            ContentResolver contentResolver = mContext.getContentResolver();
            String[] projections;
            projections = new String[]{MediaStore.Files.FileColumns._ID, MediaStore.MediaColumns.DATA,
                    MediaStore.MediaColumns.DISPLAY_NAME, MediaStore.MediaColumns.DATE_MODIFIED,
                    MediaStore.MediaColumns.MIME_TYPE, MediaStore.MediaColumns.WIDTH, MediaStore
                    .MediaColumns.HEIGHT, MediaStore.MediaColumns.SIZE};

            Cursor cursor = contentResolver.query(contentUri, projections, selection, selectionAllArgs, sortOrder);
            
            if (cursor != null && cursor.moveToFirst()) {
                        int pathIndex = cursor.getColumnIndex(MediaStore.MediaColumns.DATA);
                        int mimeTypeIndex = cursor.getColumnIndex(MediaStore.MediaColumns.MIME_TYPE);
                        int sizeIndex = cursor.getColumnIndex(MediaStore.MediaColumns.SIZE);
                        int widthIndex = cursor.getColumnIndex(MediaStore.MediaColumns.WIDTH);
                        int heightIndex = cursor.getColumnIndex(MediaStore.MediaColumns.HEIGHT);

                        do {
                            long size = cursor.getLong(sizeIndex);
                            if (size < 1) {
                                continue;
                            }

                            String type = cursor.getString(mimeTypeIndex);
                            String path = cursor.getString(pathIndex);
                            if (TextUtils.isEmpty(path) || TextUtils.isEmpty(type)) {
                                continue;
                            }

                            int width = cursor.getInt(widthIndex);
                            int height = cursor.getInt(heightIndex);
                            if (width < 1 || height < 1) {
                                continue;
                            }

                            File file = new File(path);
                            if (!file.exists() || !file.isFile()) {
                                continue;
                            }

                            File parentFile = file.getParentFile();
                            if (parentFile != null) {
                                images.add(path);
                            }

                        } while (cursor.moveToNext());

                        cursor.close();
                    }


```

通过上述代码，我们就可以用图片加载工具将图片显示出来，但需要注意的是，我们需要在`AndroidManifest.xml` 中的 `<application>` 标签中加入 `android:requestLegacyExternalStorage="true"` 


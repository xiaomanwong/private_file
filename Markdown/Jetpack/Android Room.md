---
title: Android Room
tag: Android
---

[翻译自官网文档](https://developer.android.com/reference/android/arch/persistence/room/package-summary?hl=zh-cn)



Room 是一个关系映射对象库，可以使我们很方便的访问 App 数据库

* **Database:** 注解用来标记问数据库，该类须继承 RoomDatabase,运行时，可以通过 Room.databaseBuilder 或者获取他的实例 Room.inMemoryDatabasebuilder
* **Entity:** 将 Model 或 pojo 类，标记为数据库行，每个 Entity 都会创建一个数据库表来保存项目。实体类必须在 Database#entities  数组中引用。除非另有说明，否则 Entity 的每个字段（及其父类）都将 Entity 保留在数据库中
* **Dao:** 将类或接口标记为数据访问对象。数据访问对象负责定义访问数据库的方法。带有注释的类 Database 必须具有一个带有 0 个参数的抽象方法，并返回带有 Dao 注释的类。

<!-- more -->

``` java
// File: User.java
@Entity
public class User {
    @PrimaryKey
    private int uid;
    private String name;
    @ColumnInfo(name = "last_name")
    private String lastName;
    // Room 请求 set 和 get 方法去访问数据
}

// File: UserDao.java
@Dao
public interface UserDao {
    @Query("select * from user") 
    List<User> loadAll();
    
    @Query("select * from user where uid in (:userIds)")
    List<User> loadAllByUserId(int... userIds);
    
    @Query("select * from user where name like :first and last_name like :last limit 1")
    User loadOneByNameAndLastName(String first, String last);
    
    @Insert
    void insertAll(User... users);
    
    @Delete
    void delete(User user);
}

// File: AppDatabse.java
@Database(entities = {User.java})
public abstract class AppDatabase extends RoomDatabase {
    public abstract UserDao userDao();
}

// 创建 AppDatabase 实例
AppDatabse db = Room.databaseBuilder(getApplicationContext(), AppDatabase.class, "database_name").build();
```

一旦 Room 在编译期，就开始检测注解，扫描所有可以访问的表/

可以通过使用 `InvalidtaionTracker` 类来观察一个数据表的变化。

Room 允许通过 `Query`  方法返回一个 `LiveData` 类型的数据。它会自动观察相关数据表，一旦发生数据改变，就会触发 `LiveData` 的观察者



```java
// LiveData 会自动分发数据表的改变
@Query("Select * from user order by name limit 5") 
public LiveData<List<User>> loadFirstFiveUsers();
```


![Img](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a049ecd434564b94896711ab0e9e2662~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp)



## 项目地址

https://github.com/AndroidAdvanceWithGeektime/Chapter01

编译时遇到的问题

1. ndk 路径配置

   ```
   ndk.dir=/Users/admin/Library/Android/sdk/ndk/20.1.5948944
   ```

2. 解析时报错

   命令： ./tools/mac/minidump_stackwalk db0d378e-ee42-4a7e-ca6994b6-4481535e.dmp

   报错： dyld[96564]: Symbol not found: __ZTTNSt7__cxx1118basic_stringstreamIcSt11char_traitsIcESaIcEEE
     Referenced from: /Users/admin/github/Chapter01/tools/mac/minidump_stackwalk
     Expected in: /usr/lib/libstdc++.6.dylib
   [1]    96564 abort      ./tools/mac/minidump_stackwalk db0d378e-ee42-4a7e-ca6994b6-4481535e.dmp

   解决方案：

   重新编译 minidump_stackwalk

   ```
   git clone https://github.com/google/breakpad 
   cd breakpad
   ./configure && make
   ```


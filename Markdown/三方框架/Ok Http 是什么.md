



## 为什么选用 OKHTTP

1. OKHTTP 提供了最新的 HTTP 协议版本 HTTP 2.0 和 SPDY 的支持，使得对同一个主机发出的所有请求都可以共享相同的链接
2. 如果 HTTP 2.0 和 SPDY 不可用， OKHTTP 会使用连接池来复用链接提高效率
3. OKHTTP 提供了对 GZIP 的默认支持来降低传输内容的大小
4. OKHTTP 也提供了对 HTTP 响应的缓存机制，可以避免不必要的网络请求
5. 当网络出现问题时， OKHTTP 会自动重试一个主机的多个 IP 地址

## 各拦截器的作用

* interceptor 用户自定义拦截器
* retryAndFollowUpInterceptor: 负责失败重试和重定向
* BridgeInterceptor: 请求时，对必要的 Header 进行一些添加，接收响应时，移除必要的 Header
* CacheInterceptor： 负责读取缓存直接返回（根据请求的信息和缓存响应的信息判断是否存在可用缓存）、更新缓存
* ConnectInterceptor： 负责和服务器建立链接
* CallServerInterceptor：负责向服务器发送请求数据、从服务器读取响应数据

## ConnectionPool

1. 判断 链接是否可用，不可用则从 ConnectionPool 获取链接，ConnectionPool 中无连接，则创建、握手、再存入 ConnectionPool 中
2. 内部有一个 Deque， add 添加 Connection，是的线程池负责定时清理缓存
3. 使用链接复用省去了进行 TCP 和 TLS 握手的一个过程

## 与其他网络框架对比

* Volloy：支持 HTTPS，缓存、异步请求，不支持同步请求。
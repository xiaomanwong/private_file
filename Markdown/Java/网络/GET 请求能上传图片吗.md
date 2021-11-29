# 一道面试题，GET 请求能传图片吗？

java那些事 *前天*

点击上方 **java那些事** ，选择 **星标** 公众号

#### `重磅资讯，干货，第一时间送达---`

**前言**



忘了在哪里看到的这个题目，觉得挺有意思，来说下我的答案及思考过程。



首先，我们要知道的是，图片一般有两种传输方式：base64 和 file 对象。



**base64 图片**



图片的base64编码想必大家都见过：



![图片](https://mmbiz.qpic.cn/mmbiz/7hic3VeMO6icIHiavMlkEMbXdsxqvv9Lmu1RlEiawJibASFD7bUva61bdichNX9MCM04SlV1g3811hjnzMP3epPmbnDg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



base64 的本质是字符串，而 GET 请求的参数在 url 里面，所以直接把图的 base64 数据放到 url 里面，就可以实现 GET 请求传图片。



input 输入框拿到的图是 file 对象，图片 file 对象转 base64 ：



```javascript
// img参数：file文件或者blob
const getBase64 = img => {
  return new Promise((resolve,reject) => {
    const reader = new FileReader();
    reader.onload = e => {
      resolve(e.target.result);
    };
    reader.onerror = e => reject(e);
    reader.readAsDataURL(img);
  })
}
```



问题来了，GET 请求的 url 长度是有限制的，不同的浏览器长度限制不一样，最长的大概是 10k 左右，根据 base64 的编码原理，base64 图片大小比原文件大小大 1/3，所以说 base64 只能传一些非常小的小图，大图的 base64 太长会被截断。



但其实这个长度限制是浏览器给的，而不是 GET 请求本身，也就说，在服务端，GET 请求长度理论上无限长，也就是可以传任意大小的图片。



**file 对象**



我们来看看这个场景：



```html
<form action="http://localhost:8080/" method="get">
    <input type="file" name="logo">
    <input type="submit">
</form>
```



选择图片，然后提交表单，能提交成功，但是接口收不到文件。请求的 url 会变成 http://localhost:8080/?logo=xxx.png ，但是不会携带图片数据。



正常情况，file 对象数据是放在 POST 请求的 body 里面，并且是 form-data 编码。



那么 GET 请求能否有 body 体呢？答案是可以有。



GET 和 POST 并没有本质上的区别，他们只是 HTTP 协议中两种请求方式，仅仅是报文格式不同（或者说规范不同）。



做过底层开发的同事可能比较熟悉，之前我们C语言的同事和我讲，我们的 HTTP 请求，他们收到是这样子的：



![图片](https://mmbiz.qpic.cn/mmbiz/7hic3VeMO6icIHiavMlkEMbXdsxqvv9Lmu1vAtaNIjnyibawYBicJY2eNsNRnicvSdrxNYuC0FZP9RDRnIutARZgOXGw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



举个栗子, 一个普通的 GET 请求，他们收到是这样的：



```http
GET /test/?sex=man&name=zhangsan HTTP/1.1
Host: http://localhost:8080
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: Keep-Alive
```



POST 请求长这样：



```http
POST /add HTTP/1.1
Host: http://localhost:8080
Content-Type: application/x-www-form-urlencoded
Content-Length: 40
Connection: Keep-Alive

sex=man&name=Professional 
```



同样，DELETE、PUT、PATCH 请求，也都是这样的报文。底层解析这个报文的时候，并不关心是什么请求，所以说 GET 请求也可以有 body 体，也可以传 form-data 数据。



有兴趣的可以拿 postman 试一下，看看 GET 请求传图片，接口能不能收到图片文件：



![图片](https://mmbiz.qpic.cn/mmbiz/7hic3VeMO6icIHiavMlkEMbXdsxqvv9Lmu1MrfSOFLc9RzNicz9ZxzXH0V0SNFibMUTjmcPr6qp58fQgOrOs8qibnTXQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

###  

**结尾**



综上所述，GET 请求是可以传图片的，但是 GET 和 POST 的规范还是要遵守的，如果有后台让你这么做，锤他就行了！
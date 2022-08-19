# web3钱包
[toc]{type: "ul", level: [2,3]}

## 钱包包含的功能

- [ ] 支持通过生成助记词、Keystore 文件、私钥创建钱包账号
- [ ] 支持导出钱包账号助记词、Keystore 文件、私钥
- [ ] 支持多个钱包账号管理
- [ ] 账户余额查询及转账功能
- [ ] 历史交易
- [ ] 法币兑换
- [ ] 代币查询

## 什么是 web3
![Img](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/43500485b40e4b3fac2d63584a0a5bd9~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp?)

**web1.0 读**
特点是网页是静态的，或只读。参与者只能消费内容但不能与其交互。
平台创造、平台所有、平台控制、平台收益
![Img](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1c9997be0fc34295b7994831b1760866~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp?)
**web2.0 读、写**
特点是科技公司在互联网的免费层上构建自己的平台，同时提供丰富的用户体验，防止用户离开。用户赋予了这些平台非常大的权利，并使数据泄漏更加危险和频繁。    
用户创造、平台所有、平台控制、平台分配
![Img](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/11c60a9968c24340b9c290ff04c14880~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp?)

**web3.0 读、写、Owner**
web3 是一个去中心化的网络，通过将权利和数据集中在用户手中，而不是大型科技公司。意味着数据分布在网络上，不属于任何实体。
用户无需注册平台一边又一边的提供个人数据，只需要授权平台使用数据。

用户创造、用户所有、用户控制、协议分配

![Img](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/276ca2b49e4c4464b23912b36f5b0b2e~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp?)

## 什么是区块链
1. 区块链是一个分布式网络;
2. 区块链可以帮助多个节点达成共识去记录和 Token 相关的事情; 
3. 区块链可以帮助所有人无门槛地构建属于自己的小经济系统。


### 区块链的应用
#### 数字资产方向
虚拟资产包括金融资产、游戏代币、数字版权、域名、用户流量等。由于虚拟资产不需要与实体资产进行挂钩，所以在对应的区块上更方便。

**虚拟货币**

* 第一类比如游戏代币，通常不与实体经济发生联系。比如游戏点券或钻石。这种货币的特征是封闭性，只能在指定场景中使用。
* 第二类积分类，它可以与实体经济发生联系，比如旅客积分、超市礼品卡等。这种货币的特点是单向性，即只能流入，不能流出。
* 第三类数字货币（加密货币）

**数字货币**
数字货币一般是指公有区块链平台底下的基础代币，该代币被记录在由密码学保证的一套公开账本中，与传统货币不同的是，由于去中心化及可编程等特性，此种货币具有可自定义行我的属性（合约）

## 知识储备

**数字钱包**
钱包指保存 *地址、公钥、私钥* 的文件或其他机构，每个钱包文件至少包含一个账户.

钱包的核心功能是私钥的创建、存储和使用。

数字货币钱包作为数字货币的载体，从技术角度来看，数字货币钱包分为三种类型。
1. 全节点钱包。全节点钱包是指官方发行的一种数字货币钱包版本，这个版本包含了完整的功能 需求，挖矿、发送交易、查询交易记录、管理私钥。
2. SPV 轻钱包(Simplifed Payment Verifcation )。轻钱包为了用户体验，牺牲了全节点的部分 功能，属于全节点钱包的简化版，如挖矿功能、查询交易功能就没有。
3. 中心化资产托管钱包。这种钱包其实是第三方服务商帮助你打理你的数字货币，找一个中介托 管你的数字货币，比较典型的有 blockchain.info。

以上的第 1 种和第 2 种会在各个数字货币的官网出现，属于真正意义上的数字货币钱包，1 相比 2 而言，安全性要更高;所以我在这里推荐你先从全节点钱包开始尝试，毕竟全节点钱包基本囊括了 该币种的所有功能实现。
而第 3 种钱包，与银行移动 App 或支付宝相比，在业务逻辑上区别不大。比如你会把钱托管到支 付宝上一样，你也可以将你的数字货币放进第三类钱包中。
这种钱包往往都是多币种的，深受投资用户的喜欢，而且从方便性和用户体验来说，基本完爆 1 和 2，例如以太坊系钱包 imToken ，多币种钱包 Jaxx，以及各个数字货币交易平台。
无论是什么类型的钱包，建议你在获取钱包程序的时候，一律要从官网下载，即使是移动端 App 也 强烈推荐从官网的入口进入。

```json
{
  "address": "e2c2777b535ed5d178215ea7fa386b6994122131",
  "id": "4d72b8cf-c113-4a32-ab27-2c3269ef8b17",
  "version": 3,
  "crypto": {
    "cipher": "aes-128-ctr",
    "cipherparams": {
      "iv": "9dd52adc1743b664d724e8d567be608d"
    },
    "ciphertext": "e80e1f98c7c99dd4daadd0f50439b956cfbcc850fed6c41592bae994070bccba",
    "kdf": "scrypt",
    "kdfparams": {
      "dklen": 32,
      "n": 4096,
      "p": 6,
      "r": 8,
      "salt": "796cc47bcdc7f7c1250be1b8faf8617a657d39880592350d68b057679b0fb3f3"
    },
    "mac": "421c7e14030625c481cb521fdbcedc3a615564c5c22e4555da8e0cbd06d25b72"
  }
}
```
* cipher: 加密算法， AES 算法，用于加密以太坊私钥
* cipherparams: cipher 算法需要的参数，参数 iv 是 aes-128-ctr 加密算法需要的初始化向量
* ciphertext: 加密后的秘文，aes-128-ctr函数的加密输入密文；
* kdf：秘钥生成函数，用于使用密码加密keystore文件
* kdfparams：kdf算法所需要的参数
* mac：验证密码的编码

**账户**

以太坊的核心，由一对密钥组成--公钥和私钥。账户可以分为两种--外部账户和合约账户。
为凸显劳动者的价值，在虚拟资产世界中引入钱包功能（虚拟货币钱包），为劳动者在虚拟世界中提供劳动报酬以及消费。

::: tip 举例
代驾小哥在家可以利用VR眼镜+配套设备+5G传输身临其境帮喝了酒的车主做代驾，利用区块链转账功能，完成后钱会自动转账到钱包。

我们在虚拟的世界中，工作，获取收益。钱会自动转账到钱包
:::


**密码**
密码不是私钥，是在创建账号时候的密码（可以被修改， 等价于我们平时生活中的账户密码）。密码可以在以下场景中使用
1. 作为转账的支付密码
1. 用 Keystore 导入钱包的时候需要输入密码，用来解锁 Keystore

**私钥**
私钥由 64 位长度的十六进制的字符组成，比如：`0xA4356E49C88C8B7AB370AF7D5C0C54F0261AAA006F6BDE09CD4745CF54E0115A`,**一个账户只有一个私钥且不能修改**。通常一个钱包中的私钥和公钥是成对出现的，有了私钥，我们就可以通过一定的算法生成公钥，再通过公钥经过算法生成地址，这个过程是不可逆的。
私钥要妥善保管，若泄漏别人可以通过私钥解锁账号转出账号内的数字货币。

**keystore**
常见于以太坊钱包，它是将私钥以加密的方式保存为一份 JSON 文件，*这个 JSON 文件就是 keystore*，所以它就是加密后的私钥，keystore 必须配合钱包密码才能使用账号。

**助记词**
::: tip 一串 12 ~ 24 个容易记忆的单词，方便保存和记录
:::
1. 助记词是私钥了另外一种表现形式
1. 助记词可以获取相关联的多个私钥，反过来私钥无法获取助记词
**BIP:**`bitcoin improvement proposals` 的缩写,意思是 Bitcoin 的改进建议，用于提出 Bitcoin 的新功能或改进措施，主要有 BIP32, BIP39, BIP44.

**密码、私钥、助记词于 keystore 之间的关系**
![密码、私钥、助记词于 keystore 之间的关系](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/755abed2a68a4cc396bde85fb55bcfba~tplv-k3u1fbpfcp-zoom-in-crop-mark:3024:0:0:0.awebp)

::: tip 私钥和助记词的重要性
私钥和助记词是是操作资产的唯一途径，如果丢失，那么资产就丢失，不存在忘记助记词还能找回资产的事儿。
:::

**钱包地址**
可以直接理解为银行卡号。

**智能合约**
智能合约是存储在区块链上的不可变的程序。它们根据预定条件的满足，自动执行交易，它们被广泛用于以去中心化的方式执行协议，没有中间人。
智能合约有特定的结果，由不可变的代码管理，所以合约的参与者可以对合约的执行有信心。没有第三方参与，没有时间损失--当条件得到满足时，协议立即执行。


**GasFee**
Gas费，矿工的出场费

Gas Limit：是用户愿意为执行某个操作或确认交易支付的最大 Gas 量（最少 21000）
Gas Price：用户愿意话费于每个 Gas 单位的价钱

交易成本 = GasLimit * GasPrice ，最少佣金为 0.00000002*21000=0.00042ETH.

如果用户设置的值太低，那么 TA 的交易被认为无效的，并且会以因为 Gas 不足错误而被取消，并且其中用于计算的 Gas 不会退到账户。无论交易是否通过，发送者都需要向矿工支付费用。

**NFT**
不可替代代币，是加密货币中的一员


#### web3j 和 bitcoinj

我们需要使用两个库[web3j](https://github.com/web3j/web3j/) 和[bitcoinj](https://github.com/bitcoinj/bitcoinj)

web3 是一套和以太坊通信的封装库，web3j 是 Java 版本的实现，例如发起交易和智能合约进行交互。
我们主要使用了 web3j 中椭圆曲线加密及 Keystore 文件的生成与解密
bitcoinj 的功能和 web3j 类似，它是比特币协议的 Java 实现。
![Img](https://p1-jj.byteimg.com/tos-cn-i-t2oaga2asx/gold-user-assets/2019/3/16/169871fe83e201f0~tplv-t2oaga2asx-zoom-in-crop-mark:3024:0:0:0.awebp)

Android 使用 Gradle 来构建
```groovy
implementation 'org.web3j:core:4.1.0-android'
implementation 'org.bitconinj:bitcoin-core:0.14.7'
```

### 创建钱包账号

::: tip 
以太坊及比特币的地址是由随机生成的私钥经过椭圆曲线算法单向推到。
BIP32 及 BIP44 是为了方便管理私钥提出的分层推导方案
BIP39 定义助记词让分层种子的备份更方便
:::
**通过助记词创建钱包账号**
这是目前钱包客端最常见的一种账号创建方式，包含一下几个步骤：
1. 生成一个随机数种子；
2. 通过随机数种子得到助记词
3. 通过种子 + 路径派生生成私钥
4. 使用 Keystore 保存私钥
5. 私钥推导出账号地址


``` java
// 创建钱包对象入口函数
    public static Bip39Wallet generateBip39Wallet(String password, File destinationDirectory)
            throws CipherException, IOException {
        // 生成一个随机中子数
        byte[] initialEntropy = new byte[16];
        secureRandom.nextBytes(initialEntropy);
        // 生成助记词
        String mnemonic = MnemonicUtils.generateMnemonic(initialEntropy);
        // 生成 seed
        byte[] seed = MnemonicUtils.generateSeed(mnemonic, password);
        // 生成私钥
        ECKeyPair privateKey = ECKeyPair.create(sha256(seed));
        // 创建出钱包
        String walletFile = generateWalletFile(password, privateKey, destinationDirectory, false);
        return new Bip39Wallet(walletFile, mnemonic);
    }
```

### 加载钱包文件
需要提供钱包文件和密码,可获取到地址，公钥，私钥
```java
public static Credentials loadCredentials(String password, File source) throws IOException, CipherException {
    WalletFile walletFile = objectMapper.readValue(source, WalletFile.class);
    return Credentials.create(Wallet.decrypt(password, walletFile));
}

public static void main(String[] args) {
    Credentials credentials = loadCredentials("pwd", "path");
    String address = credentials.address;
    String privateKey = credentials.privateKey;
    String publicKey = credentials.publicKey;
}
```

:::tip钱包的创建和加载都发生在本地，并未同步到以太坊区块链。
:::





## 与钱包业务相关

### 法币充值 -> 啫喱币
> 法币与啫喱 NFT 兑换比例为 1:1

第三方支付渠道暂时未定
### 钱包创建流程
* 钱包密码
用于访问钱包，访问 keystore，获取密钥使用。
消费、充值
* 助记词
助记词创建钱包, BIP39 助记词，从 1024 个单词表中，随机生成 12 个便于记忆的单词。
* 地址
用于线上交易使用的一串
* DID
本地钱包创建好之后，由服务端生成的一串与地址 1 对 1 绑定的地址。

### 钱包恢复（换机流程）
通过助记词/keystore 恢复钱包




## 参考资料

[[1] 我认为 web3 是什么（大白话 web3）](https://juejin.cn/post/7091606409208397854)
[ [2]Web3.0：互联网的未来](https://juejin.cn/post/7105952483540729893)
[ [3]使用web3j构建以太坊钱包](https://juejin.cn/post/6844903683608707086)
[ [4]web3j demo](https://github.com/initsysctrl/we3jdemo)
[ [5]Doc web3j](https://docs.web3j.io/4.8.7/web3j_eth2_client/)
[ [6]以太坊教程](https://www.qikegu.com/docs/4820)
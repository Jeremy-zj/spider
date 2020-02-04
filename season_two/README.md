
app的数据获取主要依赖于各种服务端的接口。由于我们没有浏览器这种可以比较直观的看到后台请求的工具。所以主要用一些抓包技术来抓取数据
简单的接口可以使用Charles和mitmproxy分析出来规律。
如果遇到更复杂的接口。需要利用mitmdump对接python来对抓取到的请求和响应进行实时处理和保存。
若需要做规模化的爬虫还要有处理自动化操作的工具。这里我们使用Appinum实现。可以像Selenium一样对App进行自动化控制。例如自动模拟App的点击
。下拉等操作

## App爬虫相关工具和库的安装

- Charles:网络抓包工具。比Fiddler的功能更为强大。跨平台支持的更好。这里用来做移动端的抓包
- mitmproxy：一个支持HTTP和HTTPS的抓包程序。类似Fiddler和Charles。但是主要通过控制台操作。
- mitmdump: mitmproxy的关联组件。可以对接python脚本实现监听后的处理。
- mitmweb: mitmproxy的关联组件。可以清楚的观察到mitmproxy捕获的请求
- Appium：是移动端的自动化测试工具。类似pc端的Selenium可以驱动Android。Ios等设备进行自动化测试。比如模拟点击等。


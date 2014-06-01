网页正文内容抽取
===================
此代码是对论文《基于行块分布函数的通用网页正文抽取》的Python实现方式。论文的出发点是针对搜索引擎正文提取的解决方案，移除了所有的标签元素，因此我在此保留了标签元素，改进用户阅读体验。

####特点：

* 保留正文标签
* 资源（图片、超链接等）路径为绝对路径（即使原文是相对路径）避免找不到资源

####调用：

    from html_body_extractor import BodyExtractor
    url = 'http://ballpo.com/detail/182560.html'
    be = BodyExtractor(url)
    be.execute()
    print be.body

####输出：
>经纪人承认，尽管拉齐奥前锋凯塔(Keita Balde Diao)刚刚与蓝白军团续约，但来自英超联赛的俱乐部仍旧对他保持着浓厚的兴趣。 <font color='#FFFFFF'></font> </p><p><a target="_blank" href="http://ballpo.com//uploads5/userup/1405/11202I033U.jpg"><img width="600" height="360" border="0" alt="" src="http://ballpo.com//uploads5/userup/1405/11202I033U.jpg" /></a>  <font color='#FFFFFF'></font> </p><p>“今天，对凯塔感兴趣的俱乐部都知道，要想拉齐奥放走他，你必须拿出一大笔的资金，”经纪人萨维尼(Ulisse Savini)告诉TuttoMercatoWeb.com。“没有人打电话给我，但我们都很清楚：对凯塔感兴趣的俱乐部很多，这一点也不意外。除了利物浦经常在关注他之外，还有曼联。” <span class='Obn244'></span> </p><p>最后，经纪人解释道，这名19岁的前巴塞罗那球员需要拿到西班牙的护照才能转投英国踢球，尽管这问题不大。

####TODO：

* 自定义样式
* 进一步改进提取正确率
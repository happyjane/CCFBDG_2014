#危害公共安全事件的关联关系挖掘及预测  
***
####第二届大数据技术创新与创业大赛代码作品说明文档
<pre><code>
团队名称：OmniEye团队 
团队成员:陈夏明，强思维，王海洋，孙莹，石开元  
指导老师：上海交通大学网络信息中心 金耀辉 教授  
联系方式：chenxm35@gmail.com ，13122706618
</code></pre>
## 概述  
>本危害公共安全事件的关联关系挖掘及预测案例提供了基于多维（时间、空间、语义）数据分析的公共安全事件管理方法，包括同类、异类事件的相关性分析，以及预测未来一段时间内同地区发生类似事件的可能性。该系统提供了完整的媒体数据处理和模型生成方法，主要分为空间关联性分析和未来事件预测两部分，我们提供了两种解决方案：一种是结合python、R在本地进行处理；一种是用Hadoop集群利用spark进行数据处理。包含以下核心模块可供单独调用：  
>*  数据源事件识别、提取  
>*  众包标注与校验    
>*  时空、语义特征提取  
>*  媒体传播规律、事件发生时空关联性分析    
>*  基于Gradient-Boosting算法的事件预测、交叉验证  
**  

## 环境要求    
>*  Mac OS X, Linux or Windows,SAE，微信公众平台  
>*  PHP，Python 2.7+,R or SPark   
>*  Hadoop 1.0.3+,Spark 
**  

##  代码集介绍：  
>*  `Event_classify`:数据预处理及事件分类
>*  `Feature_spatio-temporal`：事件时空特征提取
>*  `Correlation_analysis`：事件关联性分析
>*  `Critical_forecast`：暴恐事件预测
**  

##编译及配置      
###源码下载  
>该工程源码使用github仓库进行管理，克隆仓库到本地使用命令：`git clone https://github.com/OMNI-Lab/CCFBDC2014.git or git clone git@github.com:OMNI-Lab/CCFBDC2014.git` 或直接`Download ZIP`打包下载源码  
###编译源码  
* `Event_classify`:
+ 本地python运行： 
>新闻分类，在`classify_news`文件夹中运行`python classify_news.py`   
>微博分类，在`classify_weibo`文件夹中运行`classify_weibo.py`   
+ spark环境运行：  
>新闻分类，spark环境下运行 `pyspark news_classify.py`
>微博分类，spark环境下运行 `pyspark weibo_classify.py`

>独立事件特征抽取，spark环境下运行 `pyspark event_feature.py`  
* `Correlation_analysis`:
>提取事件媒体的特征,包括事件报告的数量、媒体报道、评论的数量。R环境下运行：`extract_features.R (Use:  $ R -f extract_features.R)`
>其次,我们从时间和空间两个维度分析事件相关性。空间维度上,中国主要地区使用Pearson Coefficient定义相似系数并,并通过区域矩阵给出。在时间维度上,我们通过分析类似事件的时间顺序,检测显著事件重复出现的时间间隔。R环境下运行`features_analysis.R(Use:  $ R -f features_analysis.R)`
* `Critical_forecast`：
>spark环境下运行`prediction.py`

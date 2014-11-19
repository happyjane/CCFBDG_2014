<?php
header("Content-type:text/html;charset=gbk");
//define your token
define("TOKEN", "omnilab");
date_default_timezone_set(PRC);

$wechatObj = new wechatCallbackapiTest();
//$wechatObj->responseMsg();
$wechatObj->valid();


class wechatCallbackapiTest
{  
     //确认部分，略去
    public function valid()
    {
        $echoStr = $_GET["echostr"];

        //valid signature , option
        if($this->checkSignature()){
            echo $echoStr;
            exit;
        }
    }
    private function checkSignature()
    {   
        if (!defined("TOKEN")) {
            throw new Exception('TOKEN is not defined!');
        }
        
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];    
                
        $token = TOKEN;
        $tmpArr = array($token, $timestamp, $nonce);
        sort($tmpArr);
        $tmpStr = implode( $tmpArr );
        $tmpStr = sha1( $tmpStr );
        
        if( $tmpStr == $signature ){
            return true;
        }else{
            return false;
        }
    }
    
    //响应函数
    // public function responseMsg()
    // {
    //     //get post data, May be due to the different environments
    //     $postStr = $GLOBALS["HTTP_RAW_POST_DATA"];//接收微信公众平台发送过来的用户消息，该消息数据结构为XML，不是php默认的识别数据类型
    //     $postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
    //     //使用simplexml_load_string() 函数将接收到的XML消息数据载入对象$postObj中。这个严谨的写法后面还得加个判断是否载入成功的条件语句，不过不写也没事
    //     $fromUsername = $postObj->FromUserName;//发送消息用户的OPENID赋值给$fromUsername变量
    //     $toUsername = $postObj->ToUserName;//$postObj中的公众账号的ID赋值给$toUsername变量
    //     $time = date('Y-m-d H:i:s');
    //     $msgType = $postObj->MsgType;
    //     $mysql = new SaeMysql();
    //     $count == 0;
    //     //$key1= "d86cbf57-3df6-425c-9520-1bf65342ec1d";
    //     // $key2= "ca77af73-f179-445d-964c-bbf118ae1b7c";

    //     $main = "*请输入样本集（1--新闻，2--微博）：";
       
    //     $textTpl = "<xml>
    //                      <ToUserName><![CDATA[%s]]></ToUserName>
    //                      <FromUserName><![CDATA[%s]]></FromUserName>
    //                      <CreateTime>%s</CreateTime>
    //                      <MsgType><![CDATA[%s]]></MsgType>
    //                      <Content><![CDATA[%s]]></Content>
    //                      <FuncFlag>0</FuncFlag>////位0x0001被标志时，星标刚收到的消息。
    //                      </xml>"; 
    //     $webTplHead = "<xml>
    //                              <ToUserName><![CDATA[%s]]></ToUserName>
    //                              <FromUserName><![CDATA[%s]]></FromUserName>
    //                              <CreateTime>%s</CreateTime>
    //                              <MsgType><![CDATA[%s]]></MsgType>
    //                              <ArticleCount>%d</ArticleCount>
    //                              <Articles>";
    //     $webTplBody = "<item>
    //                              <Title><![CDATA[%s]]></Title> 
    //                              <Description><![CDATA[%s]]></Description>
    //                              <PicUrl><![CDATA[%s]]></PicUrl>
    //                              <Url><![CDATA[%s]]></Url>
    //                              </item>";
    //     $webTplFoot = "</Articles>
    //                             <FuncFlag>0</FuncFlag>
    //                             </xml>";

    //     switch ($msgType){
    //             case 'text':
    //                 $keyword = trim($postObj->Content);//trim() 函数从字符串的两端删除空白字符和其他预定义字符，这里就可以得到用户输入的关键词
    //                 $sql = "select record_id,state from user where OpenID = '$fromUsername'";
    //                 $result = $mysql->getData($sql);
    //                 $record = $result[0]['record_id'];
    //                 $state = $result[0]['state'];

    //                 if($state == 0 ){
    //                     switch ($keyword) {
    //                         case 1:
    //                             $sql = "update user set state = '0' where OpenID = '$fromUsername'";
    //                             $mysql->runSql($sql);
    //                             $key= "d86cbf57-3df6-425c-9520-1bf65342ec1d";
    //                             $dataset_dict = {"resource_id": $key, "filters":{"checked":"0"}};
    //                             //$post_string = '%7B%22records%22%3A%20%5B%7B%22OpenID%22%3A%20%22'.$fromUsername.'%22%2C%20%22发布时间%22%3A%20%22'.date('Y-m-d H:i',time()).'%22%2C%20%22评论内容%22%3A%20%22'.$keyword.'%22%7D%5D%2C%20%22force%22%3A%20true%2C%20%22method%22%3A%20%22insert%22%2C%20%22resource_id%22%3A%20%2key%22%7D';
    //                             $remote_server = 'http://202.121.178.242/api/action/datastore_search';
    //                             $context = array(
    //                                 'http'=>array(
    //                                     'method'=>'POST',
    //                                     'header'=>'Authorization: e17ca6fe-c588-4938-b910-0079ff791f66',
    //                                     'content'=>$dataset_dict)
    //                                 );
    //                             $stream_context = stream_context_create($context);
    //                             $data = file_get_contents($remote_server,FALSE,$stream_context);
    //                             $data_dict = $data->read(true,'r');
    //                             $response_dict = json_decode($data.read());
    //                             foreach ($response_dict['result']['records'] as $key => $value){
    //                                 $num = $value['num'];
    //                                 $cid = $value['cid'];
    //                                 if( !(empty($value['title']))
    //                                     {$title =$value['title'];}
    //                                 $content = $value['content'];
    //                                 $contentS = "\n请输入类别(0。无关信息 1。公交爆炸 2。暴恐 3。校园砍杀 q。退出):";
    //                                 $contentStr="num:   ".$num."cid:   ".$cid."\ntitle:  ".$title."\ncontent:   ".$content.$contentS;
    //                                 $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
    //                                 echo $resultStr;
    //                                 //使用sprintf() 函数将格式化的数据写入到变量中去;$fromUsername, $toUsername, $time, $msgType, $contentStr 分别顺序替换模板里“%s”位置
    //                                 while(true == true){
    //                                     if ($keyword == 'q'){
    //                                         echo "本次已标注：".$count."条！";

    //                                         $sql = "insert into user values('$fromUsername','','0')";
    //                                         $mysql->runSql($sql);
    //                                         exit;
    //                                     }elseif(in_array($keyword,$mark)){
    //                                         $value['checked'] = 1;
    //                                         $value['hit_tag'] = $keyword;
    //                                         $data = list($value);
    //                                         $key= "d86cbf57-3df6-425c-9520-1bf65342ec1d";
    //                                         $dataset_dict = {"resource_id": key, "force": True, "records": data, "method":"update"};
    //                                         $remote_server = 'http://202.121.178.242/api/action/datastore_upsert';
    //                                         $context = array(
    //                                             'http'=>array(
    //                                                 'method'=>'POST',
    //                                                 'header'=>'Authorization: e17ca6fe-c588-4938-b910-0079ff791f66',
    //                                                 'content'=>$dataset_dict)
    //                                                             );
    //                                         $stream_context = stream_context_create($context);
    //                                         $data = file_get_contents($remote_server,FALSE,$stream_context);
    //                                         $count =$count +1;
    //                                 }else{$contentStr = '请输入类别(q 退出)：';
    //                                         echo $context;
    //                                     }
    //                                 } 
    //                             }                                  
    //                             break;
    //                         case 2:
    //                             $sql = "update user set state = '0' where OpenID = '$fromUsername'";
    //                             $mysql->runSql($sql);
    //                             $key= "d86cbf57-3df6-425c-9520-1bf65342ec1d";
    //                             $dataset_dict = {"resource_id": $key, "filters":{"checked":"0"}};
    //                             //$post_string = '%7B%22records%22%3A%20%5B%7B%22OpenID%22%3A%20%22'.$fromUsername.'%22%2C%20%22发布时间%22%3A%20%22'.date('Y-m-d H:i',time()).'%22%2C%20%22评论内容%22%3A%20%22'.$keyword.'%22%7D%5D%2C%20%22force%22%3A%20true%2C%20%22method%22%3A%20%22insert%22%2C%20%22resource_id%22%3A%20%2key%22%7D';
    //                             $remote_server = 'http://202.121.178.242/api/action/datastore_search';
    //                             $context = array(
    //                                 'http'=>array(
    //                                     'method'=>'POST',
    //                                     'header'=>'Authorization: e17ca6fe-c588-4938-b910-0079ff791f66',
    //                                     'content'=>$dataset_dict)
    //                                 );
    //                             $stream_context = stream_context_create($context);
    //                             $data = file_get_contents($remote_server,FALSE,$stream_context);
    //                             $data_dict = $data->read(true,'r');
    //                             $response_dict = json_decode($data.read());
    //                             foreach ($response_dict['result']['records'] as $key => $value){
    //                                 $num = $value['num'];
    //                                 $cid = $value['cid'];
    //                                 if( !(empty($value['title']))
    //                                     {$title =$value['title'];}
    //                                 $content = $value['content'];
    //                                 $contentS = "\n请输入类别(0。无关信息 1。公交爆炸 2。暴恐 3。校园砍杀 q。退出):";
    //                                 $contentStr="num:   ".$num."cid:   ".$cid."\ntitle:  ".$title."\ncontent:   ".$content.$contentS;
    //                                 $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
    //                                 echo $resultStr;
    //                                 //使用sprintf() 函数将格式化的数据写入到变量中去;$fromUsername, $toUsername, $time, $msgType, $contentStr 分别顺序替换模板里“%s”位置
    //                                 while(true == true){
    //                                     if ($keyword == 'q'){
    //                                         echo "本次已标注：".$count."条！";
    //                                         exit;
    //                                     }elseif(in_array($keyword,$mark)){
    //                                         $value['checked'] = 1;
    //                                         $value['hit_tag'] = $keyword;
    //                                         $data = list($value);
    //                                         $key= "d86cbf57-3df6-425c-9520-1bf65342ec1d";
    //                                         $dataset_dict = {"resource_id": key, "force": True, "records": $data, "method":"update"};
    //                                         $remote_server = 'http://202.121.178.242/api/action/datastore_upsert';
    //                                         $context = array(
    //                                             'http'=>array(
    //                                                 'method'=>'POST',
    //                                                 'header'=>'Authorization: e17ca6fe-c588-4938-b910-0079ff791f66',
    //                                                 'content'=>$dataset_dict)
    //                                                             );
    //                                         $stream_context = stream_context_create($context);
    //                                         $data_string = file_get_contents($remote_server,FALSE,$stream_context);
    //                                         $count =$count +1;
    //                                     }else{$contentStr = '请输入类别(q 退出)：';
    //                                         echo $contentStr;
    //                                     }
    //                                 } 
    //                             }                                  
    //                             break;
    //                     }

    //             case 'event':
    //                 $keyword = trim($postObj->Event);
                    
    //                 switch ($keyword) {
    //                         case 'subscribe':
    //                                 //mysql_set_charset("gbk");
    //                                 $sql = "insert into user values('$fromUsername','','0')";
    //                                 $mysql->runSql($sql);
    //                                 $contentStr = "*请输入样本集（1--新闻，2--微博）：";
    //                                 $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, "text", $contentStr);
    //                                 echo $resultStr;
    //                                 break;

    //                         case 'unsubscribe':
    //                                 $sql = "delete from user where fromUsername='$fromUsername'";
    //                                 $mysql->runSql($sql);
    //                                 break;

    //                         default:
    //                             # code...
    //                                 break;
    //                 }

    //                 break;
    //         }        
    // }
}
?>



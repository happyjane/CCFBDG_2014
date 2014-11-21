var firstpage = 1;
var lastpage = 11;
var the_timeout = setTimeout("navorbm.location.reload();", 3000 ); 
var currentPage = firstpage;
var currentbm = 1;
var currentZoom = 100;
var isload = 1;
var offsetX = 0;
var offsetY = 0;
var pageload = 0;
function init()
{
var pageListOptions ="";
toolbarWin.document.pageListForm.pageList.selectedIndex = 0;
toolbarWin.document.zoomList.zoomSelected.selectedIndex = 5;
for(i = firstpage; i <= lastpage; i++)
{
var pageindex = i - firstpage + 1;
var pageListItem;
var countPages = lastpage - firstpage + 1;
if(i == currentPage) 
pageListItem = "<option value='" + i + "' selected>page" + pageindex;
else
pageListItem = "<option value='" + i +" '>page " + pageindex;
pageListItem = pageListItem + " of " + countPages + "</option> ";
pageListOptions += pageListItem + "\n";
}
if ("Microsoft Internet Explorer"!= window.navigator.appName)
{
toolbarWin.document.pageListForm.pageList.innerHTML = pageListOptions;
}
else
{
pageListOptions = "<select name=\"pageList\"onChange=\"parent.pageChange(this)\">"+ pageListOptions + "</select>";
toolbarWin.document.pageListForm.innerHTML = pageListOptions;
}
pageload ++;
}
function ShowOrHideNavOrBm()
{
if(document.getElementById("mainframe").cols!="0,*")
{
this.isload = 0;document.getElementById("mainframe").cols ="0,*";
toolbarWin.document.NavOrBmBtn.src = "gif/close.gif";
}
else
{
this.isload = 1;
document.getElementById("mainframe").cols ="134,*";
toolbarWin.document.NavOrBmBtn.src = "gif/open.gif";
OpenIndexPage();
}
}
function OpenIndexPage()
{
if(document.getElementById("mainframe").cols != "134,*")
return;
document.getElementById("mainframe").cols = "134,*";
toolbarWin.document.NavOrBmBtn.src = "gif/open.gif";
navorbm.location = "navigation.html";
navorbmimg.location = "navimg.html";
this.isload = 1;
}
function OpenBookMarksPage()
{
if(document.getElementById("mainframe").cols != "134,*")
return;
document.getElementById("mainframe").cols = "134,*";
toolbarWin.document.NavOrBmBtn.src = "gif/open.gif";
navorbm.location = "bookmark.html";
navorbmimg.location = "bmimg.html";
this.isload = 2;
}
function GotoThePage(pageno)
{
if(pageno >= firstpage && pageno <= lastpage)
{
var strnewpage = new String("P");
var szPageNum = new String(pageno);
var szPageNumLen = 5 - szPageNum.length;
strnewpage = strnewpage + szPageNum + ".html";
content.location = strnewpage;
toolbarWin.document.pageListForm.pageList.selectedIndex = pageno-firstpage;
toolbarWin.document.FirstPageBtn.src = "gif/firstpage.gif";
toolbarWin.document.PrePageBtn.src = "gif/prepage.gif";
toolbarWin.document.NextPageBtn.src = "gif/nextpage.gif";
toolbarWin.document.LastPageBtn.src = "gif/lastpage.gif";
if(pageno == firstpage)
{
toolbarWin.document.FirstPageBtn.src = "gif/firstpage1.gif";
toolbarWin.document.PrePageBtn.src = "gif/prepage1.gif";
}
if(pageno == lastpage)
{
toolbarWin.document.NextPageBtn.src = "gif/nextpage1.gif";
toolbarWin.document.LastPageBtn.src = "gif/lastpage1.gif";
}
if( isload == 1 )
{
for(i = firstpage; i <= lastpage; i++)
{
if(i == pageno)
navorbm.document.getElementById("img"+i).src = "gif/curpagelbl.gif";
else
navorbm.document.getElementById("img"+i).src = "gif/otherpagelbl.gif";
}
}
currentPage = parseInt(pageno);
}
}
function GotoTheBookMark(pageno,bmno)
{
if(pageno >= firstpage && pageno <= lastpage)
{
GotoThePage(pageno);
var imgs = navorbm.document.images;
for(i = 1; i <= imgs.length; i++)
{
if(i == bmno)
navorbm.document.images[i-1].src = "gif/curbmlbl.gif";
else
navorbm.document.images[i-1].src = "gif/bmlbl.gif";
}
currentbm = parseInt(bmno);
if ("Microsoft Internet Explorer" != window.navigator.appName)
setNewZoom(100);
}
}
function setNewZoom(newZoom)
{
if(newZoom >= 50 && newZoom <= 200)
{
if(currentZoom != newZoom )
{
var obj = content.document.getElementsByTagName("table");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
el.height *= newZoom/currentZoom;
el.width *= newZoom/currentZoom;
}
var obj = content.document.getElementsByTagName("img");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
el.height *= newZoom/currentZoom;
el.width *= newZoom/currentZoom;
}
var obj = content.document.getElementsByTagName("span");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
if ( !isNaN(parseInt(el.style.fontSize)) )
{
var fontSize = parseInt(el.style.fontSize);
el.style.fontSize = parseInt(fontSize*newZoom/currentZoom) + 'px';
}
}
var obj = content.document.getElementsByTagName("div");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
var t = parseInt(el.style.top);
var l = parseInt(el.style.left);
if(t && l)
{
el.style.top = parseInt(t*newZoom/currentZoom) + 'px';
el.style.left = parseInt(l*newZoom/currentZoom) + 'px';
}
var h = parseInt(el.style.height);
var w = parseInt(el.style.width);
if(h && w)
{
el.style.height = parseInt(h*newZoom/currentZoom) + 'px';
el.style.width = parseInt(w*newZoom/currentZoom) + 'px';
}
}
toolbarWin.document.zoomList.zoomSelected.selectedIndex = (newZoom-50)/10;
}
if(newZoom == 50){
toolbarWin.document.ZoomoutBtn.src = "gif/zoomout1.gif";
}
else
{
toolbarWin.document.ZoomoutBtn.src = "gif/zoomout.gif";
}
if(newZoom == 200)
{
toolbarWin.document.ZoominBtn.src = "gif/zoomin1.gif";
}
else
{
toolbarWin.document.ZoominBtn.src = "gif/zoomin.gif";
}
currentZoom = newZoom;
}
}
function zoomIn()
{
setNewZoom(currentZoom+10);
}
function zoomOut()
{
setNewZoom(currentZoom-10);
}
function zoomChange(selObj)
{
var newZoom = selObj.options[selObj.selectedIndex].value;
setNewZoom(parseInt(newZoom));
}
function pageChange(selObj)
{
var newPage = selObj.options[selObj.selectedIndex].value;
GotoThePage(parseInt(newPage));
if ("Microsoft Internet Explorer" != window.navigator.appName)
setNewZoom(100);
}
function GotoNewPage(pageno)
{
GotoThePage(parseInt(pageno));
if ("Microsoft Internet Explorer" != window.navigator.appName)setNewZoom(100);
}
function myprint()
{
content.focus();
content.print();
}
function left()
{
if (0==this.offsetX) return;
this.offsetX = 0;
this.offsetY = 0;
toolbarWin.document.LeftBtn.src = "gif/curleft.gif";
toolbarWin.document.CenterBtn.src = "gif/center.gif";
toolbarWin.document.RightBtn.src = "gif/right.gif";
GotoThePage(currentPage);
if ("Microsoft Internet Explorer" != window.navigator.appName)
setNewZoom(100);
}
function center()
{
var cw = content.document.body.clientWidth;
var ch = content.document.body.clientHeight;
var iw = 0;
var ih = 0;
var obj = content.document.getElementsByTagName("table");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
var iw = el.width;
var ih = el.height;
}
if (cw>iw && (cw-iw)/2 != this.offsetX)
{
this.offsetX = (cw-iw)/2;
this.offsetY = 0;
toolbarWin.document.LeftBtn.src = "gif/left.gif";
toolbarWin.document.CenterBtn.src = "gif/curcenter.gif";
toolbarWin.document.RightBtn.src = "gif/right.gif";
GotoThePage(currentPage);
if ("Microsoft Internet Explorer" != window.navigator.appName)
setNewZoom(100);
}
}
function right()
{
var cw = content.document.body.clientWidth;
var ch = content.document.body.clientHeight;
var iw = 0;
var ih = 0;
var obj = content.document.getElementsByTagName("table");
for (var i=0;i < obj.length;i++)
{
var el = obj[i];
var iw = el.width;
var ih = el.height;
}
if(cw>iw && cw-iw!=this.offsetX)
{
this.offsetX = cw-iw;
this.offsetY = 0;
toolbarWin.document.LeftBtn.src = "gif/left.gif";
toolbarWin.document.CenterBtn.src = "gif/center.gif";
toolbarWin.document.RightBtn.src = "gif/curright.gif";
GotoThePage(currentPage);
if ("Microsoft Internet Explorer" != window.navigator.appName)
setNewZoom(100);
}
}

;$(document).ready(function(){var text=$('.card_comment-textarea');var texto=$('.card_commento');var helper=$('.card_comment-helper');function closeHelper(id){$('#card_comment-helper'+id).hide();$('.card_comment'+id).attr('status','stop')}
text.on('keyup',function(e){var id=$(this).attr('id')
var text=$(this).text()
console.log(e.key)
if(e.key=='Enter'||e.key===' '||(e.key==='Backspace'&&text[text.length-1]=='!')){closeHelper(id)}
else{is_search=false;crnt='';for(var i=window.getSelection().anchorOffset-1;i>=0;i--){if(text[i]==='!'){is_search=true;break;}
else if(text[i]===' '){crnt=''
break;}
crnt=crnt+text[i]}
if(is_search&&text[text.length-1]!='!'){var d=document.getElementById('card_comment-helper'+id);d.style.left=getSelectionCoords().x-250+'px';d.style.top=getSelectionCoords().y-300+'px';$('#card_comment-helper'+id).show();var url=$(this).attr('url')
$.ajax({url:url,data:{'text':crnt,},dataType:'json',success:function(data){if(data.res!='empty'){for(var i=0;i<data.res.length;i++){$('.card'+id+'helper'+(i+1)).show()
$('.card'+id+'helper'+(i+1)).text('!'+data.res[i])}
for(var i=data.res.length;i<5;i++){$('.card'+id+'helper'+(i+1)).hide()}}}})}}});$('.takecard').on('click',function(e){this_=$(this)
url=this_.attr('url')
id=this_.attr('id')
$.ajax({url:url,data:{'id':id,},dataType:'json',success:function(data){if(data.ok){this_.removeClass('small green full-w')
this_.text('Отказаться от карточки')
$('.nouser'+id).show()
$('.nouser'+id).text('#'+data.manager)
$('.nouser'+id).attr('href',data.manager_url)}
else{this_.addClass('small green full-w')
this_.text('Взять себе')
$('.nouser'+id).hide()}}})})
$('.card_form-days').on('click',function(e){this_=$(this)
url=this_.attr('url')
id=this_.attr('id')
card=this_.attr('card')
$.ajax({url:url,data:{'id':id,'card':card},dataType:'json',success:function(data){num=id+1
if(data.status=='yes'){this_.addClass('green')
$('#card'+card).addClass('day'+num)}
else{this_.removeClass('green')
$('#card'+card).removeClass('day'+num)}}})})
$('.card_comment-item').on('click',function(e){var str=$(e.target).text();textarea=$('.card_comment'+$(this).attr('id'))
text=textarea.text()
position=window.getSelection().anchorOffset
indexstart=position
for(var i=position-1;i>=0;i--){console.log(text[i])
if(text[i]==='!'){indexstart=i;break;}
else if(text[i]===' '){break;}}
newtext=text.slice(0,indexstart)+str+text.slice(position)
textarea.text(newtext);$('.card_comment-helper').hide()});text.on('input',function(){closeHelper();})
$('.card_form-select-contact').on('change',function(){url='/schools/api/card_called/'
id=$(this).attr('id')
this_=$(this)
selector=document.getElementsByClassName('card_form-select-contact'+id)[0];action=selector.options[selector.selectedIndex].value;console.log(action)
$.ajax({url:url,data:{'id':id,'action':action,},dataType:'json',success:function(data){this_.hide();$('.card_form-select-contact-btn'+this_.attr('id')).text('Связался по '+action)
$('.card_form-select-contact-btn'+this_.attr('id')).show();}})});function getSelectionCoords(win){win=win||window;var doc=win.document;var sel=doc.selection,range,rects,rect;var x=0,y=0;if(sel){if(sel.type!="Control"){range=sel.createRange();range.collapse(true);x=range.boundingLeft;y=range.boundingTop;}}else if(win.getSelection){sel=win.getSelection();if(sel.rangeCount){range=sel.getRangeAt(0).cloneRange();if(range.getClientRects){range.collapse(true);rects=range.getClientRects();if(rects.length>0){rect=rects[0];}
x=rect.left;y=rect.top;}
if(x==0&&y==0){var span=doc.createElement("span");if(span.getClientRects){span.appendChild(doc.createTextNode("\u200b"));range.insertNode(span);rect=span.getClientRects()[0];x=rect.left;y=rect.top;var spanParent=span.parentNode;spanParent.removeChild(span);spanParent.normalize();}}}}
return{x:x,y:y};}});
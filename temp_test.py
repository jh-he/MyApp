import requests

url = 'www.baidu.com'
raw_para = '''include: data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics
limit: 5
offset: 0
sort_by: default'''
para = {}#参数要求传入字典
for each in raw_para.split('\n'):
    key,value = each.split(':',1)
    para[key] = value.replace(" ","")#去除多余空格


r = requests.get(url,params=para)#headers和cookies在我的上一篇文章说到过怎么设置
print(r.url)#查看添加了参数后的url
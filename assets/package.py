# -*- coding:utf-8 -*-
import os,json,re,sys
sdk_dict={}
ABS_PATH=os.path.abspath('')
package_name=''
pre_package_name=''
sdk_file=''
def replace_package_name(path,file_name):
	if os.path.exists(os.path.join(ABS_PATH,path)):
		os.chdir(os.path.join(ABS_PATH,path))
	else:
		print("文件路径不存在")
		return
	#文件备份
	os.system('mkdir backup')
	os.system('copy '+file_name+' backup/'+file_name)
	mod_file_name=file_name.split('.')[0]+'1'+file_name.split('.')[1]
	file_obj=open(file_name,'r',encoding='utf-8')
	mod_file=open(mod_file_name,'w+',encoding='utf-8')
	content=file_obj.read()
	mod_file.write(content.replace(PRE_PACKAGE_NAME,NOW_PACKAGE_NAME))
	file_obj.close()
	mod_file.close()
	os.system('del '+file_name)
	os.rename(mod_file_name,file_name)
	#切回主目录
	os.chdir(ABS_PATH)
def replace_package_name_all1():
	replace_package_name('','AndroidManifest.xml')
	replace_package_name('','build.gradle')
	replace_package_name('src/org/cocos2dx/sdk','WechatsDK.java')
	replace_package_name('src/org/cocos2dx/sdk','XianliaoSDK.java')
	replace_package_name('src/'+PRE_PACKAGE_NAME.replace('.','/')+'/wxapi','Util.java')
	replace_package_name('src/'+PRE_PACKAGE_NAME.replace('.','/')+'/wxapi','WXEntryActivity.java')
	replace_package_name('src/'+PRE_PACKAGE_NAME.replace('.','/')+'/sgapi','SGEntryActivity.java')
def replace_package_name_all():
	global sdk_dict,package_name,pre_package_name
	package_name = sdk_dict['package']['package_name']

	reg_str=r'package=\"(\S*?)\"'
	reg_str1=r'android:taskAffinity=\"\.(\S*?)\.task\"'
	reg_str2=r'applicationId \"(\S*?)\"'
	reg_replace('','AndroidManifest.xml',reg_str,package_name)
	pre_package_name=reg_replace('','build.gradle',reg_str2,package_name)

	reg_str3=r'import (\S*?)\.R;'
	reg_str4=r'import (\S*?)\.wxapi\.Util'
	reg_str5=r'import (\S*?)\.wxapi\.WXEntryActivity'
	reg_replace('src/org/cocos2dx/sdk','WechatsDK.java',reg_str3,package_name)
	reg_replace('src/org/cocos2dx/sdk','XianliaoSDK.java',reg_str3,package_name)

	reg_str6=r'package\s*?(\S*?)\.wxapi'
	reg_replace('src/'+pre_package_name.replace('.','/')+'/wxapi','Util.java',reg_str6,package_name)
	reg_replace('src/'+pre_package_name.replace('.','/')+'/wxapi','WXEntryActivity.java',reg_str6,package_name)

	reg_str7=r'package\s*?(\S*?)\.sgapi'
	reg_replace('src/'+pre_package_name.replace('.','/')+'/sgapi','SGEntryActivity.java',reg_str7,package_name)
	# 替换包名对应路径
	replace_package_path()
	print("================================================\n\
		Tips：包名替换成功\n================================================")
def replace_icon_file():
	org_path="icon\\"+package_name.split('.')[1]
	if not os.path.isdir(org_path) or not os.path.exists(org_path):
		print("\nFailed：确保icon文件夹与包名对应一致!!!!!!!\n")
		sys.exit(0)
	# os.remove('res\\drawable\\share.jpg')
	print('copy '+org_path+'\\Icon-96.png'+' res\\drawable\\share.jpg')
	os.system('copy '+org_path+'\\Icon-96.png'+' res\\drawable\\share.jpg')
	# os.remove('res\\mipmap-hdpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-72.png'+' res\\mipmap-hdpi\\icon.png')
	# os.remove('res\\mipmap-ldpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-36.png'+' res\\mipmap-ldpi\\icon.png')
	# os.remove('res\\mipmap-mdpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-48.png'+' res\\mipmap-mdpi\\icon.png')
	# os.remove('res\\mipmap-xhdpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-96.png'+' res\\mipmap-xhdpi\\icon.png')
	# os.remove('res\\mipmap-xxhdpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-144.png'+' res\\mipmap-xxhdpi\\icon.png')
	# os.remove('res\\mipmap-xxxhdpi\\icon.png')
	os.system('copy '+org_path+'\\Icon-180.png'+' res\\mipmap-xxxhdpi\\icon.png')
	print("================================================\n\
		Tips：Icon资源替换成功\n================================================")
def replace_package_path():
	pre_path_list=['src']
	now_path_list=['src']
	pre_path_list.extend(pre_package_name.split('.'))
	now_path_list.extend(package_name.split('.'))
	try:
		os.rename('/'.join(pre_path_list),'/'.join(pre_path_list[:-1])+'/'+now_path_list[-1])
		os.rename('/'.join(pre_path_list[:-1]),'/'.join(pre_path_list[:-2])+'/'+now_path_list[-2])
		os.rename('/'.join(pre_path_list[:-2]),'/'.join(now_path_list[:-2]))
	except FileNotFoundError as e:
		print("请检查包名与当前文件路径是否一致")
	except PermissionError as e2:
		print("当前文件夹拒绝访问，确保无其他程序访问")
	finally:
		pass
def replace_app_name():
	reg_str=r'\"app_name\">(\S*?)<'
	print(os.getcwd())
	reg_replace('res\\values','strings.xml',reg_str,sdk_dict['package']['app_name'])
	print("================================================\n\
		Tips：APP名称替换成功\n================================================")
def sdk_helper():
	global sdk_dict
	# 百度sdk
	AndroidManifest_file=open('AndroidManifest.xml','r+',encoding='utf-8')
	content_text=AndroidManifest_file.read()
	match_list=re.findall(r'<meta-data[\S\s]*?/>',content_text)
	match_str=get_obj_str(match_list,'baidu')
	replace_str=re.sub(r'android:value=\"(.+)\"','android:value=\"'+sdk_dict['baidu']['app_id']+'\"',match_str)
	mod_file=open('AndroidManifest1.xml','w+',encoding='utf-8')
	content_text=content_text.replace(match_str,replace_str)
	# 闲聊sdk(androidmanifest.xml)
	match_list1=re.findall(r'<data[\S\s]*?/>',content_text)
	match_str1=get_obj_str(match_list1,'xianliao')
	replace_str1=re.sub(r'android:host=\"(.+)\"','android:host=\"xianliao'+sdk_dict['xianliao']['app_id']+'\"',match_str1)
	content_text=content_text.replace(match_str1,replace_str1)
	# 擦肩sdk(androidmanifest.xml)
	match_str2=get_obj_str(match_list1,'\"cj')
	replace_str2=re.sub(r'android:host=\"(.+)\"','android:host=\"'+sdk_dict['cajian']['app_id']+'\"',match_str2)
	mod_file.write(content_text.replace(match_str2,replace_str2))
	AndroidManifest_file.close()
	mod_file.close()
	os.remove('AndroidManifest.xml')
	os.rename('AndroidManifest1.xml','AndroidManifest.xml')
	# 微信SDK
	reg_weixin_str=r'APP_ID = \"(.*?)\"'
	reg_replace('src/org/cocos2dx/sdk','WechatSDK.java',reg_weixin_str,sdk_dict['wechat']['app_id'])
	# 擦肩SDK
	reg_cajian_str=r'CJ_APPID = \"(.*?)\"'
	reg_replace('src/org/cocos2dx/sdk','CajianSDK.java',reg_cajian_str,sdk_dict['cajian']['app_id'])
	# 闲聊SDK
	reg_xianliao_str=r'SG_APPID = \"(.*?)\"'
	reg_replace('src/org/cocos2dx/sdk','XianliaoSDK.java',reg_xianliao_str,sdk_dict['xianliao']['app_id'])
	# bugly配置(两处)
	reg_bugly_str=r'bugly {[\s]*?appId = \'(.*?)\'[\S\s]*?}'
	reg_bugly_str1=r'bugly \{[\S\s]*?appKey = \'(.*?)\'[\S\s]*?}'
	reg_bugly_str2=r'CrashReport.initCrashReport[\s\S]*?\"(.*?)\"'
	reg_replace('','build.gradle',reg_bugly_str,sdk_dict['bugly']['app_id'])
	reg_replace('','build.gradle',reg_bugly_str1,sdk_dict['bugly']['secret'])
	reg_replace('src/org/cocos2dx/cpp','AppActivity.java',reg_bugly_str2,sdk_dict['bugly']['app_id'])
	print("================================================\n\
		Tips：SDK配置成功\n================================================")
def reg_replace(path,file,reg_str,replace_str):
	os.chdir(os.path.join(ABS_PATH,path))
	# if not (os.path.exists("backup") and os.path.isdir("backup")):
	# 	os.system('mkdir backup')
	# if not os.path.exists("backup\\"+file):
	# 	os.system('copy '+file+' backup\\'+file)
	pre_file=open(file,'r',encoding='utf-8')
	now_file_name=file.split('.')[0]+'1'+file.split('.')[1]
	now_file=open(now_file_name,'w+',encoding='utf-8')
	content=pre_file.read()
	replace_content=content
	# 需确保匹配结果唯一
	print(re.findall(reg_str,content))
	for item in re.findall(reg_str,content):
		match_str=item
		# print(replace_str+"<<<"+match_str)
		replace_content=re.sub(match_str,replace_str,replace_content)
	now_file.write(replace_content)
	pre_file.close()
	now_file.close()
	os.remove(file)
	os.rename(now_file_name,file)
	os.chdir(ABS_PATH)
	return ''.join(re.findall(reg_str,content))
def sign_config():
	reg_keyalias=r'keyAlias \'\S*?\''
	reg_passwd=r'keyPassword \'\S*?\''
	reg_path=r'storeFile file\(\'(\S*?)\'\)'
	reg_store_passwd=r'storePassword \'\S*?\''
	reg_gradle=r'RELEASE_STORE_FILE=(\S*?)\s'
	reg_gradle1=r'RELEASE_STORE_PASSWORD=\S*?\s'
	reg_gradle2=r'RELEASE_KEY_PASSWORD=\S*?\s'
	reg_gradle3=r'RELEASE_KEY_ALIAS=\S*?\s'
	updir_path=os.path.abspath(os.path.join(os.getcwd(),"..")).replace('\\','/')
	reg_replace('','build.gradle',reg_keyalias,'keyAlias \''+sdk_dict['signconfig']['keyAlias']+'\'')
	reg_replace('','build.gradle',reg_passwd,'keyPassword \''+sdk_dict['signconfig']['keyPassword']+'\'')
	reg_replace('','build.gradle',reg_store_passwd,'storePassword \''+sdk_dict['signconfig']['storePassword']+'\'')
	print('storeFile file(\''+updir_path+'/'+sdk_dict['signconfig']['signname']+'\')')
	reg_replace('','build.gradle',reg_path,updir_path+'/'+sdk_dict['signconfig']['signname'])
	reg_replace('','gradle.properties',reg_gradle,updir_path+'/'+sdk_dict['signconfig']['signname'])
	reg_replace('','gradle.properties',reg_gradle1,'RELEASE_STORE_PASSWORD='+sdk_dict['signconfig']['storePassword']+'\n')
	reg_replace('','gradle.properties',reg_gradle2,'RELEASE_KEY_PASSWORD='+sdk_dict['signconfig']['keyPassword']+'\n')
	reg_replace('','gradle.properties',reg_gradle3,'RELEASE_KEY_ALIAS='+sdk_dict['signconfig']['keyAlias']+'\n')
	print("================================================\n\
		Tips：签名文件配置成功\n================================================")
def get_obj_str(list,key):
	for item in list:
		if item.find(key)!=-1:
			return item
def getstart():
	global sdk_file
	sdk_file_list=[]
	i=0
	for file in os.listdir(ABS_PATH):
		if len(re.findall(r'sdk_(\S*?)\.json',file))!=0:
			sdk_file_list.append(file)
	if len(sdk_file_list)==0:
		print("确保json文件放于该路径！!!")
		sys.exit(0)
	else:
		print("================================================")
		for item in sdk_file_list:
			print(str(i)+':'+item)
			i=i+1
		k=input("================================================\n选择要使用的配置文件：")
		try:
			sdk_file=sdk_file_list[int(k)]
			print(sdk_file)
		except IndexError:
			print("Failed:确认输入的序号合法!!!")
if __name__ == '__main__':
	getstart()
	content=json.loads(open(sdk_file,encoding='utf-8').read())
	for item in content:
		sdk_dict[item['name']]=item
	replace_package_name_all()
	replace_app_name()
	replace_icon_file()
	sdk_helper()
	sign_config()
	print("Success：配置成功！")
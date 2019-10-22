# -*- coding:utf-8 -*-
import os,shutil,re,sys
ABS_PATH=os.path.abspath('')
packagePath=""
version=""
clientPath=""
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
		if replace_str!="":
			replace_content=re.sub(match_str,replace_str,replace_content)
	now_file.write(replace_content)
	pre_file.close()
	now_file.close()
	os.remove(file)
	os.rename(now_file_name,file)
	os.chdir(ABS_PATH)
	return ''.join(re.findall(reg_str,content))
def init_client_path():
	global clientPath
	proj_name=ABS_PATH.split('\\')[-1]
	up_dir=os.path.abspath(os.path.join(os.getcwd(),'..'))
	clientPath_mod=os.path.join(up_dir,"GameClientRelease")
	if not os.path.exists(os.path.join(up_dir,"GameClientRelease")):
		print(os.path.join(up_dir,"GameClientRelease\\"+proj_name))
		clientPath_mod=input("输入你的ClientRelease路径：")
	if not os.path.exists(os.path.join(up_dir,"GameClientRelease\\"+proj_name)):
		clientPath=clientPath_mod+"\\"+input("工程名不一致，输入ClientRelease下的工程名：")
		shutil.copytree(clientPath,clientPath_mod+"\\"+proj_name)
		shutil.rmtree(clientPath)
	clientPath=clientPath_mod+"\\"+proj_name
	# return clientPath
def encrypt_game():
	if os.path.exists('encrypt'):
		shutil.rmtree('encrypt')
	os.system('mkdir encrypt')
	if os.path.exists("encrypt_game.py"):
		os.system('python encrypt_game.py')
	else:
		os.system('encrypt_game.bat')
def get_version():
	bigVersion=[]
	smallVersion={}
	for file in os.listdir(clientPath):
		if len(re.findall(r'^[vV](\d)\.(\d*?)$',file))!=0:
			result=re.findall(r'^[vV](\d)\.(\d*?)$',file)
			# print(result)
			bigVersion.append(int(result[0][0]))
			if result[0][0] not in smallVersion:
				smallVersion[result[0][0]]=[]
			smallVersion[result[0][0]].append(int(result[0][1]))
	bigVersion.sort()
	smallVersion[str(bigVersion[-1])].sort()
	return "v"+str(bigVersion[-1])+"."+str(smallVersion[str(bigVersion[-1])][-1]+1)
def move_encrypt_dir():
	global version
	version=get_version()
	# if not os.path.exists(clientPath+'\\'+version):
	# 	os.system('mkdir '+clientPath+'\\'+version)
	shutil.copytree("encrypt",clientPath+'\\'+version)
def modify_maifest(reverse):
	# 打包失败回退
	increase=reverse and -1 or 1
	# manifestFile=open("manifest_creator.ini","r+",encoding="utf-8")
	reg_game_dir=r'gameDir = ([vV][\.\d]*)\s'
	reg_curr_version=r'currVersion = ([\.\d]*)\s'
	reg_replace(clientPath,'manifest_creator.ini',reg_game_dir,version)
	curr_version=reg_replace(clientPath,'manifest_creator.ini',reg_curr_version,"")
	curr_version=".".join(curr_version.split('.')[:-1])+'.'+str(int(curr_version.split(".")[-1])+increase)
	reg_replace(clientPath,'manifest_creator.ini',reg_curr_version,curr_version)
def modify_package_file():
	global packagePath
	packagePath=os.path.abspath(os.path.join(clientPath,".."))+"\\dabao"
	reg_package=r"gameList = \[\'(.+?)\'\]"
	print(packagePath)
	reg_replace(packagePath,"package.py",reg_package,clientPath.split('\\')[-1])
if __name__ == '__main__':
	encrypt_game()
	init_client_path()
	move_encrypt_dir()
	modify_maifest(False)
	modify_package_file()
	os.chdir(packagePath)
	# os.system("python package.py")
	if os.system("python package.py")==0:
		print("打包成功！")
	else:
		shutil.rmtree(clientPath+'\\'+version)
		modify_maifest(True)
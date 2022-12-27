import shutil
import sys
import os
import subprocess
import time



try:
    wx_id=sys.argv[1]
except:
    print("\033[34m[+]Author:Jmc_G0mini[+]\033[0m")
    print("\033[31m[+]Function:聚合小程序一键化反编译[+]\033[0m")
    print("\033[31m[+]Version:V1.1[+]\033[0m")
    print("\033[31m[+]支持分包功能[+]\033[0m")
    print("\033[32m[+]用法介绍：""\r\n" + "python main.py wxid" + "\r\n" + "path.txt放入小程序路径\033[0m")

wx_path=open('path.txt','r',encoding='utf-8')
wx_path=wx_path.read().splitlines()
wx_path=str(wx_path[0])+"\\"+str(wx_id)

def describe():
    print("\033[34m[+]Author:Jmc_G0mini[+]\033[0m")
    print("\033[31m[+]Function:聚合小程序一键化反编译[+]\033[0m")
    print("\033[31m[+]Version:V1.1[+]\033[0m")
    print("\033[31m[+]支持分包功能[+]\033[0m")
    print("\033[32m[+]用法介绍：""\r\n" + "python main.py wxid" + "\r\n" + "path.txt放入小程序路径\033[0m")



#获取需要解密的文件夹
def path(wx_path):
    file_paths = []
    for root , dirs , files in os.walk(wx_path):
        for file in files:
            # 构造文件的完整路径
            file_path = os.path.join(root, file)
            # 将文件的路径添加到列表中
            file_paths.append(file_path)
    file_paths=sorted(file_paths)
    return file_paths
    # for file_path in file_paths:
    #     print (file_path)

def dec():
    ## 解密
    num=0
    for dec_path in path(wx_path):
        num+=1
        file_name='dec'
        dec_path='"'+dec_path+'"'
        sys1 = os.system(f'decrypt.exe -wxid {wx_id} -in {dec_path}')
        shutil.move('dec.wxapkg','new_dec')
        folder_path='new_dec'
        file_list = os.listdir('new_dec')
        for i, file in enumerate(file_list):
            # 如果文件名是 "dec.wxapkg"，则进行重命名
            if file == "dec.wxapkg":
                # 设置新的文件名
                new_file_name = f"dec_{chr(ord('a') + num-1)}.wxapkg"
                # 重命名文件
                os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_file_name))

## 获取解包路径
def dec_path():
    file_paths = []
    for root, dirs, files in os.walk('new_dec'):
        for file in files:
            # 构造文件的完整路径
            file_path = os.path.join(root, file)
            # 将文件的路径添加到列表中
            file_paths.append(file_path)
    file_paths = sorted(file_paths)
    return file_paths

## 解包
def dec_pack():
    len_=str(len(dec_path()))
    if int(len_) >= 2 :
        commands=[]
        for dec_ in dec_path()[1:]:
            command=[f'node.exe wxappUnpacker\wuWxapkg.js {dec_} -s=new_dec\\dec_a']
            commands.append(command)
        sys2=subprocess.Popen(f'node.exe wxappUnpacker\wuWxapkg.js {dec_path()[0]}',shell=True)
        sys2.wait()
        for x in commands:
            sys3=subprocess.Popen(x[0],shell=True)
            sys3.wait()
    else:
        sys2 = subprocess.Popen(f'node.exe wxappUnpacker\wuWxapkg.js {dec_path()[0]}', shell=True)
        sys2.wait()
# 定义异常报错处理程序



if __name__ == '__main__':
    describe()
    path(wx_path)
    dec()
    dec_path()
    dec_pack()
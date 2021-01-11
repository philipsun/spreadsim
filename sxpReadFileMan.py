# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose: This is to connect pygame to sxpNCPState
# Create Time: 2020/12/18 10:15
# Author: Xiaoping Sun  xiaopingsun@gmail.com//971994252@qq.com
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
#this file contains some classes that are to read text files

import codecs
import os,sys

import re
import pickle
import xlrd
import xlsxwriter
import joblib
import shutil
import json

dirstack = []
dirfile_list = []
total_len = 0
total_word = 0
import time
#this is to just make the current_one a back and then,save the latest one as current one
def coverbakcopythensave(fname,project_dict):
    bkfname = fname + '.bak'
    if os.path.exists(fname):
        if os.path.exists(bkfname): #first check and remove last bak
            os.remove(bkfname)
        os.rename(fname,bkfname) #then copy current to bak
    SaveObject(project_dict,fname) #finally, save new
def saveastimeversion(fname,dataobject):
    tfname = makebaktimefilename(fname)
    SaveObject(tfname,dataobject)
def replacewithnew(fname,fname_new,timebackdir):
    dirname,lfname = os.path.split(fname)
    tname = makebaktimefilename(lfname)
    bakfullname = os.path.join(timebackdir,tname)
    shutil.copy(fname,bakfullname)
    os.remove(fname)
    shutil.copy(fname_new,fname)
def makebaktimefilename(fname):
    timestr ="--{0}".format( time.time())
    tfname = fname + timestr
    while(os.path.exists(tfname)):
        timestr ="--{0}".format( time.time())
        tfname = fname + timestr
    return tfname

def makebaktimefilenamesuff(fname,suffix = '.zip'):
    timestr ="{0}".format(time.time())
    tfname = fname + timestr
    while(os.path.exists(tfname)):
        timestr ="{0}".format( time.time())
        tfname = fname + timestr
    return tfname + suffix

def traversedir(input_path,result,file_pat='\.py$'):
    files = os.listdir(input_path)
    for filename in files:
        if os.path.isdir(input_path+'/'+filename):
            traversedir(input_path+'/'+filename,result,file_pat)
        else:
            if matchpat(filename,file_pat):
                result.append(input_path+'/'+filename)    
def matchpat(filename,file_pat):
    g = re.match(file_pat,filename)
    if g:
        return True
    return False

def copydir(srcdir,trgdir):
    try:
        shutil.copytree(srcdir,trgdir)
        return 'ok'
    except Exception as e:
        msg = 'copytree dir failed'+srcdir+str(e)
        return msg
def deletedir(srcdir):
    try:
        shutil.rmtree(srcdir)
        return 'ok'
    except Exception as e:
        msg = 'delete dir failed'+srcdir+str(e)
        print(msg)
        return msg


def SaveObject(ob,fname):
    joblib.dump(ob,fname,compress=9)
def LoadObject(fname):
    if os.path.exists(fname)==False:
        print('not exists',fname)
        return None
    return joblib.load(fname)
def extractname(fullname):
    name_dict={}

    curr = os.getcwd()
    drivename,remname=os.path.splitdrive(fullname)
    dirname,filename=os.path.split(fullname)
    name_dict['isdir']=os.path.isdir(fullname)
    name_dict['drivename']= drivename
    name_dict['remname']= remname
    name_dict['currdir']=curr
    name_dict['dirname']= dirname
    name_dict['fname']= filename
    return name_dict
def IsExsit(fname):
    return os.path.exists(fname)

def CheckDir(dirstr):
    if os.path.exists(dirstr) == False:
        os.path.os.mkdir(dirstr)
        print('ok, we make dir',dirstr)
    print('ok',dirstr)
    return dirstr
def CheckDelMkDir(dirstr):
    if os.path.exists(dirstr) == False:
        os.path.os.mkdir(dirstr)
        print('ok, we make dir',dirstr)
    else:
        #os.removedirs(dirstr)
        try:
            shutil.rmtree(dirstr)
            return dirstr
        except Exception as e:
            msg = 'delete dir failed'+dirstr+str(e)
            print(msg)
            return None

        print('ok, we del origin one dir',dirstr)
        os.path.os.mkdir(dirstr)
        print('ok, we make dir',dirstr)
    print('ok',dirstr)
    return dirstr

def TestJsonDump():
    json_dict = {}

    urlrec = []
    for i in range(10):

        id =0;
        for j in range(10):
            urlitem = {'i':i,'j':j}
            urlrec.append(urlitem)
    json_dict['test']=urlrec
    urlrecfile = 'test.json'
    urlf = open(urlrecfile,'w+')
    json.dump(urlrec,urlf)
    urlf.close()
    fname = 'json_dict.json'
    StoreJsonDict(json_dict,fname)
def StoreJsonDict(json_dict,fname):
    strjson = json.dumps(json_dict)
    f = codecs.open(fname,'w+','utf-8')
    f.write(strjson)
    f.close
    return 1
def ExtractJsonFromStr(jstr):
    t=json.JSONDecoder().decode(jstr)
    return t

def ReadJSonFromJSonFile(fname):
    f=file(fname)
    f = codecs.open(fname,'r','utf-8')
    txt = f.read()
    t=json.JSONDecoder().decode(txt)
    return t

def ExtractJasonStr(jstr):
##        pattern = r"var\sdata=(\{.*?\})";
##        #but this won't work for nested brackets so we use another simple one
##        ct = re.findall(pattern,str,0)# it will return '{hello}' in ct[0] for str='var data={hello};
    ph = r'var\sdata='
    pe = r'};'
    str1 = re.sub(ph,'',jstr)
    str2 = re.sub(pe,'}',str1)
    return str2
def DeepSave(fname,ob):
    joblib.dump(ob,fname,compress=9)
def CheckLoadDict(dirfile):
    d  ={}
    if os.path.exists(dirfile)==True:
        return joblib.load(dirfile)
    return d
def CheckLoadList(dirfile):
    d  =[]
    if os.path.exists(dirfile)==True:
        return joblib.load(dirfile)
    return d

def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def IsType(fname,typename):
    fs = fname.split('.')
    if fs[-1] == typename:
        return True;
    else:
        return False
def GetDirFileList(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         pass
      else:
         filelist.append(f)
    return filelist
def WriteExcel(fname, tableindex,rwstrset):
    if not os.path.exists(fname):
        print('file does not exists',fname)
        return []
    try:
        workbook = xlsxwriter.Workbook(fname)
        nsheet = len(rwstrset)
        for eachtable in rwstrset:
            worksheet = workbook.add_worksheet()
            row = 0
            for eachrw in eachtable:
                col = 0
                for eachcol in eachrw:
                    # ctype 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                    ctype = 1
                    xf = 0
                    value = str(eachcol)
                    worksheet.write(row, col, value)
                    col = col + 1
                row = row + 1
            print('row write ', row)
        workbook.close()
    except Exception as e:
        print('error in writing excel',e)

def LoadExcel(fname,tableindex=0):
    if not os.path.exists(fname):
        print('file does not exists',fname)
        return []
    data = xlrd.open_workbook(fname)
    table = data.sheets()[tableindex]
    nrows = table.nrows
    ncols = table.ncols
    print('load', fname,nrows,ncols)
    return table
def CountFileLineWord(filedir,ftype):
    dirstack = []
    dirfile_list = []
    total_len = 0
    total_word = 0
    total_len, total_word = TraverseCountDir(filedir, ftype)
    print('in ', filedir, ' you have: len, word are:')
    print(total_len,total_word)
def GetDirFile(filedir,ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0,0
    filelist = []
    subdirlist = []
    total_fnum = 0
    total_type = 0
    total_size  = 0
    dirstack = []

    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    subfile_dic ={}
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(df)
         dirstack.append(df.lower())
      else:
         filelist.append(f)
    file_type_set =[]
    for eachf in filelist:
        ff =  os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        total_fnum = total_fnum + 1
        if urttype == ftype:
            total_type = total_type + 1
            file_type_set.append(ff)
    return file_type_set
def CountFileNum(filedir,ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0,0,0
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    total_fnum = 0
    total_type = 0
    total_size  = 0
    dirstack = []

    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    subfile_dic ={}
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(df)
         dirstack.append(df.lower())
      else:
         filelist.append(f)
    for eachf in filelist:

        ff =  os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        total_fnum = total_fnum + 1
        if urttype == ftype:
            total_type = total_type + 1
            total_size = total_size + os.path.getsize(ff)
    while len(subdirlist) > 0:
        next_subdir = subdirlist.pop()
        tl, tw,ts = CountFileNum(next_subdir,ftype)
        total_fnum = total_fnum + tl
        total_type = total_type + tw
        total_size = total_size + ts
    return total_fnum, total_type,total_size
def TraverseCountDir(filedir,ftype):
    if not os.path.exists(filedir):
        print(filedir)
        print('no dir to be read')
        return 0,0
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    total_len = 0
    total_word = 0
    dirstack = []

    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    subfile_dic ={}
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(df)
         dirstack.append(df.lower())
      else:
         filelist.append(f)
    for eachf in filelist:

        ff =  os.path.join(filedir, eachf).lower()
        urttype = GetFileType(eachf)
        if urttype == ftype:
            dirfile_list.append([ff,eachf])
            txtlines = ReadTxtLines(ff)
            lennum = len(txtlines)
            wordnum = 0
            for eachline in txtlines:
                wds = eachline.split(' ')
                wordnum = wordnum + len(wds)
            print(lennum,wordnum,ff)
            total_len = total_len + lennum
            total_word = total_word + wordnum
    while len(subdirlist) > 0:
        next_subdir = subdirlist.pop()
        tl, tw = TraverseCountDir(next_subdir,ftype)
        total_len = total_len + tl
        total_word = total_word + tw

    return total_len, total_word
def GetFileType(fname):
    ft = fname.split('.')
    return ft[-1]
def GetURLFileType(urls):
    patstr ='/{0,2}(\w+)(\.)(\w+)$'
    pattern = re.compile(patstr)
    match = pattern.search(urls)
    pat_name= 'urltype'
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(urls,posd[1])
        return tg[2]
        #pattern_pos.append([tgtxt,posd,tg[2],pat_name,1,0])
    return ''
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
     else:
         return r'.'
rootdir = r'D:\pythonwork\code\axureui'
rootdir = r'./'  #cur_file_dir()
print(('rootdir:', rootdir))
logfilename =rootdir + r'\weblog\log.txt'
indexpage = rootdir + r'\templates\index.html'
startuipage = rootdir + r'\templates\start.htm'
webfileroot = rootdir + r'\webfile'
webfilerootpattern = webfileroot.replace('\\','\\\\').lower()

def GetWebFilePathName(s):
    patstr ='d:\\\\pythonwork\\\\code\\\\axureui\\\\webfile(.+)'
    patstr =webfilerootpattern + '(.+)'
    pattern_pos = []
    pattern = re.compile(patstr)
    match = pattern.search(s)
    pat_name = 'url'
    filesuffixpatstr = r''
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,1,0])
        return tg[0]
    print('')
def TraverseDir(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(df)
         dirstack.append(df.lower())
      else:
         filelist.append(f)
    for eachf in filelist:
        if eachf == 'axQuery.std.js':
            breakpoint = 1
        ff =  os.path.join(filedir, eachf).lower()

        urlpath = GetWebFilePathName(ff)
        if urlpath is None:
            print('none in', ff)
        else:
            urttype = GetURLFileType(eachf)
            webfile_dic[urlpath] = [ff,urttype]
            dirfile_list.append([ff,eachf,urlpath])
    while len(dirstack) > 0:
        next_subdir = dirstack.pop()
        TraverseDir(next_subdir)
    return filelist, subdirlist

def GetDir(filedir):
    if not os.path.exists(filedir):
        print('no dir to be read')
        return []
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(f)
      else:
         filelist.append(f)

    return filelist, subdirlist
def WriteStrFile(filename,txtstr,encodetype='gbk'):
    #    ut = sxpTextEncode.GetUnicode(txtstr)
        ut = txtstr
   #     ut = ut.encode('utf-8')
        f = codecs.open(filename,'w+',encodetype)
        f.write(ut)
        f.close();


def ReadTextUTF(fname):
       try:

           f = codecs.open(fname,'r','utf-8')
           txt = f.read()
           f.close()
           return txt
       except IOError:
            print('wrong in open')
            return []
       return textcontent
def ReadTextContent(fpathname):
        try:
            file = open(fpathname,'r')
            textcontent = file.read()
            file.close()
            return textcontent
        except IOError:
            print('wrong in open')
            return []
        return textcontent

def ReadALL(fpathname):
        print(fpathname)
        try:
            file = open(fpathname,'r')
            lineset = [];
            while 1:
                lines = file.readlines(100000)
                if not lines:
                   break
                for line in lines:
                  print(line);
                lineset = lineset + lines;

            file.close()
            return lineset
        except IOError:
            print('wrong in open')
            file.close();
            return []
        return lines
def ReadTxtLines(fpathname):
        try:
            file = open(fpathname,'r')
            lineset = [];
            while 1:
                line = file.readline()
                if not line:
                   break
                if len(line.strip())==0:
                    continue;
                else:
                    lineset.append(line);
            file.close()
            return lineset
        except IOError:
            print('wrong in open')
            file.close();
            return []
        return lines
def SaveTxtFile(fname,txt,encodetype='utf-8'):
        try:
            fileHandle =codecs.open(fname,'w','utf-8')
            fileHandle.write(txt)
            fileHandle.close()
        except IOError as e:
            print(fname)
            print(('wrong in open',e))

def BackupTxtFile(fname):
    txt = ReadTextUTF(fname)
    fnamename = fname+'.bk'
    i = 0
    while(1):
        if os.path.exists(fnamename):
            fnamename = fnamename + '.bk'
            i = i + 1
            if i >=2:
                fnamename = fname+ '.bk'
                SaveTxtFile(fnamename,txt)
                print('overlap the oldest fil:',fnamename)
                break
        else:
            SaveTxtFile(fnamename,txt)
            print('backup it to file:',fnamename)
            break
def GetNewName(fname):
    fnamename = fname+'(1)'
    i = 0
    while(1):
        if os.path.exists(fnamename):
            fnamename = fnamename + '.bk'
            i = i + 1
            if i >=10:
                fnamename = fname+ '.bk'
                print('overlap the oldest fil:',fnamename)
                break
        else:
            print('backup it to file:',fnamename)
            break
    return fnamename
def TestCount():
    dirstack = []
    dirfile_list = []
    total_len = 0
    total_word = 0
    filedir = r'E:\pythonworknew\code\textparse'
    print(filedir)
    print('--------------------- count source code')
    ftype = 'py'
    CountFileLineWord(filedir,ftype)
    ftype = 'html'
    CountFileLineWord(filedir,ftype)
    print('---------------------count document num')
    ftype = 'pdf'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num,f_size= CountFileNum(filedir,ftype)
    print('There are %.3f' % (f_size/1024/1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype)
    ftype = 'pptx'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num,f_size= CountFileNum(filedir,ftype)
    print('There are %.3f' % (f_size/1024/1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype)
    ftype = 'docx'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num,f_size= CountFileNum(filedir,ftype)
    print('There are %.3f' % (f_size/1024/1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype)
    ftype = 'jpg'
    filedir = r'D:\pythonwork\code\queryparse'
    tf, specific_file_num,f_size= CountFileNum(filedir,ftype)
    print('There are %.3f' % (f_size/1024/1024), 'Mbytes', 'for all', specific_file_num, ' of type: ', ftype)
def testcopy():
    src = r'.\src\test'
    trg = r'.\trg' #if using .\trg, the copydir will creat .\trg and copy all files and subdir
    # of  the 'src\test' to the .\trg, if .trg is already there, error reports, cause it will first
    #create the target dir, so you do not have to create it
    src = r'.\src\test'
    trg = r'.\trg\test' #in this case, trg dir should be exists, and its sub dir
    #test should be not exist so that they can create it in the \trg dir becore copying
    #all files and sub dirs to the target dir.

    copydir(src,trg)
def testre():
    fn = r'E:\pythonworknew\code\emailman\testproject\sxpEmailMan.dpy'
    pt = '(.+)\.py$'
    g = re.match(pt,fn)
    if g:
        print(g.groups()[0])
    else:
        print('not matched')
    CheckDelMkDir('E:\pythonworknew\code\emailman\zip')
def main():
   # TestCount()
   # TestCount()
  # testcopy()
  testre()
if __name__ == '__main__':
    main()



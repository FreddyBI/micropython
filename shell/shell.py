import utime
import uos

E='  Error'

def intinput(s):
  try:
    return int(input(s))  
  except ValueError:
    return -1  

from os import listdir

def selectfile():
  nrfiles=tree()
  fnr = intinput('Open filenumber: ')
  filename=""
  if fnr >-1 and fnr <=nrfiles:
    filename=tree(getfilenr=fnr)
  return "" if type(filename) is int else filename # "" if directory selected    

def ed():
       
    def load_file():
      nonlocal filename
      nonlocal data
      saveifchanged()
      filename=selectfile()
      if filename != "":
        f=open(filename,'r')
        s=f.read()
        data = s.split('\n')
        f.close()
        print_data()
        
    def print_filename():
        print("\nFilename >> "+filename+" <<")
        
    def print_data(s=None):
      if currentfile():
        print_filename()
        print()
        line_number = 1
        for line in data:
            if s is None or s in line:
              print(str(line_number)+':'+line)
            line_number += 1
        print()

    def edit_data():
      nonlocal changed   
      if currentfile():    
        print_data()
        i=intinput('Enter line number: (Press return to skip)')-1
        if i > -1 and i < len(data):
          changed=True  
          print(data[i]) 
          data[i] = input()

    def remove_line():
      nonlocal changed   
      if currentfile(): 
        print_data()
        i=intinput('Remove line: (Press return to skip)')-1
        if i > -1 and i < len(data):
           changed=True 
           data.pop(i)

    def save_file():
      nonlocal changed
      if currentfile():
        print_filename()
        f=open(filename, 'w')
        f.write('\n'.join(data))
        f.close()
        print('saved')
        changed=False

    def new_file():
        nonlocal filename
        saveifchanged()
        filename = input('Filename: ')
        if filename in listdir():
          print('File exist!')  
          filename=""  
        elif currentfile():
          data.clear()
          add_data()

    def add_data():
      nonlocal changed  
      if currentfile(): 
        print_data()
        run = True
        counter = len(data)+1
        print('. to stop add lines')
        while run:
            code_line = input(str(counter)+':')
            counter += 1    
            if code_line is '.':
                run = False
            else:
                changed=True
                data.append(code_line)
                
    def insert_data():
      nonlocal changed   
      if currentfile():
        print_data()
        i = intinput('Insert before line ?(Press return to skip)')
        if i < 1:
          return  
        if i > 0 and i <= len(data):
          run = True
          print('. to stop add lines')
          while run:
            code_line = input(str(i)+':')
            if code_line is '.':
                run = False
            else:
                changed=True
                data.insert(i-1,code_line)                
                i+= 1
    def search():
      if currentfile():
        print_data(input('Search:'))
        
    def saveifchanged():
      nonlocal changed   
      if changed:
        print_filename()
        nr= intinput('0-Save file or Press return to skip save file ')
        if nr is 0:
          save_file()
        changed=False  
      
    def exit():
        nonlocal run
        saveifchanged()
        run=False
        
    def currentfile():
      if filename is "":
        print ('No Filename!')
        return False
      else:
        return True  

    run = True
    commands = '0-Open 1-Print 2-Edit 3-Remove 4-Save 5-Exit 6-New 7-add 8-Insert 9-Search'
    func=[load_file,print_data,edit_data,remove_line,save_file,exit,new_file,add_data,insert_data,search]
    data=[]
    filename=""
    changed=False
    while run:
        print(commands)
        i = intinput('Enter command: ')
        if i >-1 and i < len(func):
            func[i]()
        else:
            print('Wrong command')

def get_mode(f=""):
    try:
        return uos.stat(f)[0]
    except OSError:
        return 0

def get_stat(f=""):
    try:
        return uos.stat(f)
    except OSError:
        return (0,) * 10

def mode_exists(mode):
    return mode & 0xc000 != 0

def mode_isdir(mode):
    return mode & 0x4000 != 0

def mode_isfile(mode):
    return mode & 0x8000 != 0

def tree(path="/",subdir=True,count=-1,getfilenr=-1): # Lists files recursive or get filename
  try:   
    for data in uos.ilistdir(path):
      name=data[0]
      count+=1
      if path != '/':
        fn = path + '/' + name
      else:
        fn = path + name
      stat = uos.stat(fn)
      mtime = utime.localtime(stat[8])
      if data[1] is 0x4000:
        directory="(directory)"
        size=0
      else:
        if getfilenr != -1 and count ==  getfilenr: return fn   
        directory=""
        size = stat[6]
      if getfilenr is -1:  
        print('[{:3d}] {:6d} {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} {} {}'.format(
        count,size,mtime[0],mtime[1],mtime[2],mtime[3],mtime[4],mtime[5],fn,directory))
      if directory is "(directory)" and subdir:
        count=tree(fn,count=count,getfilenr=getfilenr)
        if type(count) != int : return count
    return count  
        
  except:
    print(E)
    
def lsr(path="/"):# Lists files recursive
  r=tree(path)
  return ""

def ls(path="/"):# Lists files
  r=tree(path,subdir=False)
  return ""
    
def cd(path="."):# Change directory
  try:   
    uos.chdir(path)
  except:
    print(E)
  return ""  

def cat(f,find=""):# Display file contents
  try:
    for line in open(f):
      if find in line: print(line, end='')
  except:
    print(E)
  return ""  
   
def mkdir(target=""):# Create a directory
  mode = get_mode(target)
  if target is "":
    print("Missing target directory")  
  elif not mode_exists(mode):
    uos.mkdir(target)
  else:
    print('%s already exists.' % target)
  return ""  

def pwd():# Display full pathname of the current working
  print(uos.getcwd())
  return ""

def rm(f):# Remove a file
  try:
    uos.remove(f)
  except:
    try:
      uos.rmdir(f)
    except:
      print('%s is not a file or directory.' % f)
  return ""    
      
def run(f):# Run micropython code from file
  try:  
    exec(open(f).read())
  except:
    print('%s is not a file or directory.' % f)
  return ""  
    
def getfunctionsrecords(fileobj):
  for s in (line.strip() for line in fileobj):
    if s[:4]=="def " and "):#" in s:
      #yield s[4:].replace('):',')').split("#")[0]
      yield s[4:]  
  fileobj.close()    

def sys_info():# Display machine info
  from uos import uname,statvfs
  from gc import collect
  from machine import freq
  from micropython import mem_info
  collect()
  print(uname())
  print("machine.freq:",freq(),"flash:",statvfs("/"))
  mem_info()
  return ""
    
def shell():
  for key in sorted(ex):
    print(key,ex[key])  
  try:
    s=input("\nAction? ")
    if s is "q":
      return -1
    elif s.strip().isdigit():
      key='{:2d}'.format(int(s))  
      func=ex[key]
      print(func)
      lpars=func.split("(")
      #print('lpars=',lpars)
      pars=lpars[1].split(")")[0].split(',')
      #print('pars=',pars)
      if len(pars) == 1 and pars[0] == '' :
        code=lpars[0]+"()"  
      else:    
        for nr,par in enumerate(pars):
          if par != 'f' : s=input(par+" ? ")
          ls=pars[nr].split("=")
          if len(ls) is 2:
            if not s is '':
              stringchar='"' if ls[1][-1]=='"' else '' 
              pars[nr]=ls[0]+"="+stringchar+s+stringchar
          elif ls[0] == "f":
            pars[nr]="selectfile()"  
          else:    
            pars[nr]=s
        code=lpars[0]+"("+str(pars).replace("['","").replace("']","").replace("', '",",")+")"
        print(code)
      s=input('exec [y]/n?')
      try:
        if s == "" or s == "y":
         exec('print('+code+')')
         s=input("Press enter to continue.")
      except KeyboardInterrupt:
        return -1
      except:
        print(E) 
      return 1
    else:
      c=ex[s]
      if s is "c":
        c=input("\nCommand? ")  
      try:  
        exec(c)
      except:
        print(E)
    if not s is '':    
      s=input("Press enter to continue.")
  except KeyboardInterrupt:
    return -1
  except:
    print("!"*10)
    s=input("Press enter to continue.")
  return 1

ex={"":"",
      "e":"ed()",
      "h":"help()",
      "m":"help('modules')",
      "lm":'print(dir()) # Loaded modules',
      "r":'from machine import reset;reset()',
      "sd":'import uos;print(uos.listdir("/sd"))', 
      "c":'execute micropython command', 
      "q":"quit"
      }

def sh():
  for i, f in enumerate(getfunctionsrecords(open('shell.py'))):
    ex['{:2d}'.format(i)]=f
  while True:
    if shell() is -1: break
    
sh()




import os
import pickle
from datetime import datetime
import time
def create_snapshot():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # files = []
    direc = []
    dic = {}
    snap = {}
    file_stamp = 0

    for root,sdirs,filenames in os.walk(path):
        for f in filenames:
            f_name = os.path.relpath(os.path.join(root,f),path)
            file_stamp = os.path.getmtime(os.path.join(path,f_name))
            dic[f_name] = file_stamp
        
        for d in sdirs:
            direc.append(os.path.relpath(os.path.join(root,d),path))

    

    tsnap = dict(files = dic , subdirs = direc)
    snap[dt_string] = tsnap

    savesnap(snap)
    return snap

 

def savesnap(snap):
    size = 0
    snap_arr = []
    if os.path.isfile(os.path.join(path,"snapfile")):
        with open(os.path.join(path,"snapfile"),'rb') as file_snap:
            snap_arr = pickle.load(file_snap)
    
    snap_arr.append(snap)

    with open(os.path.join(path,"snapfile"), "wb") as file_snap:
        pickle.dump(snap_arr,file_snap)

    print("Snapshot Saved")



def show_snap():
    with open(os.path.join(path,"snapfile"),"rb") as f:
        arr = pickle.load(f)
    print("0.   Current Snap\n")
    for i in range(len(arr)):
        item = list(arr[i].keys())[0]
        print(i+1,".",item)
        print("")
    

    choice = int(input("Enter your choice: "))  
    print("")
    if choice == 0:
        curr_choice = create_snapshot()
    else: 
        curr_choice = arr[choice-1]
        
    print(curr_choice)
    print("\n")
    
    return curr_choice


def compare_snap():
    diff = {}
    print("Choose 1'st snap\n")
    a_snap = show_snap()
    t1 = list(a_snap.keys())[0]
    t1_t = time.mktime(datetime.strptime(t1, "%d/%m/%Y %H:%M:%S").timetuple())
    print("Choose 2nd snap\n")
    b_snap = show_snap()
    t2 = list(b_snap.keys())[0]
    t2_t = time.mktime(datetime.strptime(t2, "%d/%m/%Y %H:%M:%S").timetuple())

    if t1_t > t2_t:
        print("Difference between ", t2,"->",t1)
        print("\n")
        second = list(a_snap.values())[0]
        first = list(b_snap.values())[0]
    else:
        print("Difference between ", t1,"->",t2)
        print("\n")
        first = list(a_snap.values())[0]
        second = list(b_snap.values())[0]

    print(first)
    diff['deleted_files'] = list(set(first['files'].keys()) - set(second['files'].keys()))
    diff['added_files'] = list(set(second['files'].keys()) - set(first['files'].keys()))
    diff['modified_files'] = []
    diff['added_folders'] = list(set(second['subdirs']) - set(first['subdirs']))
    diff['deleted_folders'] = list(set(first['subdirs']) - set(second['subdirs']))

    for t in set(first['files']).intersection(set(second['files'])):
        # f_name = os.path.relpath(os.path.join(root,f),path)
        # first_stamp = os.path.getmtime(os.path.join(path,t))
        if first['files'][t] != second['files'][t]:
            diff['modified'].append(t)


    print(diff)

def helpfn():
    pass

if __name__ == '__main__':
    print("1. Take snapshot")
    print("2. Show snapshots")
    print("3. Compare snaphots")
    print("4. Help")
    print("5. Exit")

    functions = {
        1:create_snapshot,
        2:show_snap,
        3:compare_snap,
        4:helpfn
    }

    path = input("Enter path")

    ch = int(input("Enter choice: "))
    print('\n')
    if ch in functions:
        functions[ch]()
    else:
        print("Invalid Choice")


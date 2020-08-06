import shutil
import os
import os.path
import stat
import time
import sys
import exifread

month_dict = {'Jan':'01',
              'Feb':'02',
              'Mar':'03',
              'Apr':'04',
              'May':'05',
              'Jun':'06',
              'Jul':'07',
              'Aug':'08',
              'Sep':'09',
              'Oct':'10',
              'Nov':'11',
              'Dec':'12' }
monthF_dict = {'01':'Janauary',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}

class TypeError (Exception):
    pass

if __name__ == '__main__':
    if (len(os.sys.argv) < 3):
        print("Usage: python3 sort_file src_dir dst_dir\n\n")
        exit()

    # get the source directory and destination directory
    src_dir = os.sys.argv[1]
    dst_dir = os.sys.argv[2]

    # walk through all the files
    for roots, dirs, files in os.walk(src_dir):

        for f in files:          
        
            fname = os.path.join(roots, f)
            filename = os.path.abspath(fname)
            
            fo = open(filename,'rb')
            tags = exifread.process_file(fo)
            fo.close()

            if tags and len(tags) > 0 and 'Image DateTime' in tags:
                # get the taken time like: ASCII=2018:12:07 03:10:34
                dt =tags['Image DateTime']

                print(" it is normal\n")
                xtime = str(dt).split() # remove time and keep date
                print(xtime[0], xtime[1])

                year = xtime[0].split(':')[0]
                month = xtime[0].split(':')[1]
                day = xtime[0].split(':')[2]
                #print(year, month, day)
            else:
                #print(" it is except \n")
                # Get file modified time information "%Y%m%d_%H%M%S"
                #mtime = time.localtime(os.stat(filename).st_mtime)

                #获取文件的访问时间、改变时间、修改时间
                #atime = time.ctime(os.path.getatime(filename))
                #ctime = time.ctime(os.path.getctime(filename))
                mtime = time.ctime(os.path.getmtime(filename))

                print(mtime)
                year = mtime[20:24]
                month = month_dict[mtime[4:7]]
                day = mtime[8:10]
                c_H = mtime[11:13]
                c_M = mtime[14:16]
                c_S = mtime[17:19]

                #print( " -------- ", sys._getframe().f_lineno)
                #print(" --- ", year, month, day)

                '''
                if mtime[2] < 10:
                    day = '0' + str(mtime[2])
                else:
                    day = str(mtime[2])
                '''
            
            dat = year + '_' + month + '_' + day
            pathnm = os.path.join(dst_dir, dat)

            # create the directory if not exist
            if not os.path.isdir(pathnm):
                print("Create file folder " + pathnm)
                os.mkdir(pathnm)

            newfile = pathnm + '/' + f
            print(newfile)
            if os.path.isfile(newfile):
                print("exist... " + newfile)
                #do = int(input("1. skip, 2.replace, 3.keep both.\n"))
                do = 3
                if do == 1:
                    continue
                elif do == 2:
                    os.remove(newfile)
                    # move the file
                    print("Move file: " + filename + " to " + pathnm)
                    shutil.move(filename, pathnm)
                elif do == 3:
                    # 1. change the dest name, then copy
                    new_split = os.path.splitext(newfile)
                    new_name = new_split[0] + '_2' + new_split[1]
                    if os.path.isfile(new_name):
                        new_name = new_split[0] + '_3' + new_split[1]
                    if os.path.isfile(new_name):
                        new_name = new_split[0] + '_4' + new_split[1]
                    if os.path.isfile(new_name):
                        new_name = new_split[0] + '_5' + new_split[1]
                    os.rename(newfile, new_name)
                    shutil.move(filename, pathnm)
                else:
                    print("Input Error")
            else:
                shutil.move(filename, pathnm)


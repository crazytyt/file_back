import shutil
import os
import os.path
import stat
import time
import sys
import exifread

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
        
            filename = os.path.join(roots, f)
            #print(filename)
            
            fo = open(filename,'rb')
            tags = exifread.process_file(fo)
            fo.close()

            # get the taken time like: ASCII=2018:12:07 03:10:34
            time=tags['Image DateTime']

            xtime = str(time).split() # remove time and keep date
            #print(xtime[0], xtime[1])

            year = xtime[0].split(':')[0]
            month = xtime[0].split(':')[1]
            day = xtime[0].split(':')[2]
            #print(year, month, day)
            
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



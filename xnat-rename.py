#!/usr/bin/env python

# xnat-rename.py

usage = """
xnat-rename dir1 [dir2 dir3 ...]

      where arguments dir1, dir2 etc are the names of the directory which contains the scans .
      Possibly let the arguments be the individual session directory for a subject. (Session is different than a scan, and a scan has multiple image/dicom files)

"""
import os, os.path
import dicom

def pad_rename(dir_name,series,serNo):
    print "In pad_rename"
    #print dir_name

    for filename in os.listdir(dir_name):
        pfx1,pfx2,pfx3,pfx4,pfx5,pfx6,pfx7,pfx8,pfx9=filename.split('.') #Hard Code, didn't use list for no specific reason

        #Zero padding for 8 digits
        pfx5=pfx5.zfill(8)

        new_filename=pfx1+"."+pfx2+"."+pfx3+"."+pfx4+"."+pfx5+"."+pfx6+"."+pfx7+"."+pfx8+"."+pfx9

        os.rename(os.path.join(dir_name,filename),os.path.join(dir_name,new_filename))

    #Renaming the directory
    parent, tail2 = os.path.split(dir_name)
    os.renames(parent,parent.rsplit('/',1)[0]+"/"+serNo+"_"+series)

def traverseme(dirname):
    pathname = ""
    print
    for f in os.listdir(dirname):
        pathname = os.path.join(dirname,f)
        if os.path.isdir(pathname):
            traverseme(pathname)
        elif pathname.lower().endswith('.dcm'):
            head, tail = os.path.split(pathname)
            dd = dicom.ReadFile(pathname)
            series = getattr(dd,"SeriesDescription","Unknown")
            serNo = getattr(dd,"SeriesNumber","1")
            print "Series is::" + series
            pad_rename(head,series,str(serNo))
            break



if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print usage
        sys.exit()
    arg_dir = sys.argv[1:]
    for dir_name in arg_dir:
        print dir_name
        if os.path.isdir(dir_name):
            traverseme(dir_name)
        else:
            print usage
            print "ERROR: input arguments should be of the type >> directory"

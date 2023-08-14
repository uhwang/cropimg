'''
    crop image files with given amounts
    
    8/8/23
'''
import sys
import pathlib
import subprocess as sp

#magick $FILE -crop 0x0+0+76 $FILE-crop.png
#done

def print_usage():
    print("python [path1] [ext] [path2] [left]x[top]x[right]x[bottom]\n"
          "path1 : input folder\n"
          "ext   : the extension of input files(jpg or png)\n"
          "path2 : subfolder name under path1\n"
          "left  : the amount crop from left\n"
          "top   : the amount crop from top\n"
          "right : the amount crop from right\n"
          "bottm : the amount crop from bottom\n"
          "Ex) python crop book1 png crop 0x75x0x0")

def save(options):

    if len(options) < 4: 
        print_usage()
        return
        
    path1 = pathlib.Path(options[0])
    ext   = options[1]
    path2 = pathlib.Path("%s/%s"%(path1,options[2]))
    
    print("=> List all files")
    files = [f for f in path1.glob("*.%s"%ext) if f.is_file()]
    print("=> %d files"%len(files))
    
    print("=> Create output folder")
    if path2.exists() == False:
        try:
            path2.mkdir()
        except Exception as e:
            print("... Error: %s\n... Fail to create %s"%
                 (e,path2))
            return False
            
    print("=> Success")
    
    skip = options[3].split('x')
    
    for i_, f_in in enumerate(files):
        f_out = pathlib.Path.joinpath(path2, "%s-crop%s"%(f_in.stem, f_in.suffix))
        cmd=[ "magick", 
              str(f_in), 
              "-crop",
              "+%s+%s"%(skip[0],skip[1]),
              "-crop",
              "-%s-%s"%(skip[2],skip[3]),
              str(f_out) ]
        
        try:
            # https://docs.python.org/3/library/subprocess.html
            # If you wish to capture and combine both streams into one, 
            # use stdout=PIPE and stderr=STDOUT instead of capture_output.
            # youtube-dl emits error and warning to stderr
            proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
        except Exception as e:
            print("... Error: %s"%e)
        print("=> cropping %d"%i_)
            
if __name__ == "__main__":
    save(sys.argv[1:])

import os

# path = './data/Lucknow_slaries.json'

# outfile = './cleandata/dd.json'
# 只使用与较小的文件，比较大的文件运行时间长

def fenhang(infile,outfile):

    infopen = open(infile,'r')
    outopen = open(outfile,'w')
    try:
        lines = infopen.readlines()
        list_1 = []
        for line in lines:
            print(line)
            if line not in list_1:
                list_1.append(line)
                outopen.write(line)
        infopen.close()
        outopen.close()
    except:
        pass
# fenhang(path,outfile)


def list_file():

   
    filename_list = os.listdir('data/companyinfo/')
    # print(filename_list)
    for filename in filename_list:
        path = './data/companyinfo/%s'%filename
        print(path)
        outfile = './cleandata/%s'%filename
        print(outfile)
        fenhang(path,outfile)

list_file()









import sys

try:
    with open('test111.txt', 'w+') as fb:
        fb.write('something')

        s = fb.readline()
        print(s)
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise


filename = './result22.html'
    # fb = open(filename, 'wb', encoding='utf-8')
fb = open(filename,'w+')
fb.write("ttt")

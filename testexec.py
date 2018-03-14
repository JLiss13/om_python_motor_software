import sys
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv) - 1)
print("The input arguments are: " , str(sys.argv[1:len(sys.argv)]))

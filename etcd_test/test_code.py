

string = 'v3/BNG1/ABC/RSYS8/ELECTRA/6'

#print dir(string)

x = string.rsplit('/')
for i in range(len(x)):
    print '/'.join(x[:i])


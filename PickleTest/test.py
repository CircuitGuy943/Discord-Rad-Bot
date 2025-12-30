import pickle

file = open("data_file1.p", 'rb')
data = pickle.load(file)
print(len(data))
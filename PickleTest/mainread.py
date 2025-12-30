import pickle

done = False
answer = ""

#Change a pickle from inside a file
def change(file_path, name, changer, value):
    global done
    file = open(file_path, 'rb')
    data = pickle.load(file)
    file = open(file_path, 'wb')
    print(data)
    if changer != "name":
        for N in range(len(data)):
            if data[N]["name"] == name:
                data[N][changer] = value
                done = True
                pickle.dump(data, file)
        if done == False: 
            print("Error: Could not find that name in the database")
    else:
        return "Error: Cannot change name itself"

#Return a certian player's stats, using their name
def printone(file_path, name):
    global done
    file = open(file_path, 'rb')
    data = pickle.load(file)
    for N in range(len(data)):
        if data[N]["name"] == name:
            done = True
            return str(data[N]["name"]) + "'s balance is: " + str(data[N]["balance"]) + ". Their multiplier is: " + str(data[N]["multiplier"]) + ". Their index in the database is: " + str(N)
    if done == False:
        return "Error: Could not find that name in the database"

#Return the database inside a pickle file, assuming there is only one pickle
def printall(file_path):
    global answer
    file = open(file_path, 'rb')
    data = pickle.load(file)
    for N in range(len(data)):
        answer = answer + str(data[N]["name"]) + "'s balance is: " + str(data[N]["balance"]) + " Their multiplier is: " + str(data[N]["multiplier"]) + "\n"
    return answer

print(printone("data_file1.p", "@acid2u"))
change("data_file1.p", "acid2u", "balance", "123123123123123123123123")
print(printone("data_file1.p", "@acid2u"))

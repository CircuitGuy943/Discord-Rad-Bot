import pickle

info_1 = [{"name": "@CircuitGuy943", "balance": "1239483", "multiplier": "x250"}, {"name": "@PurpleShark", "balance": "230", "multiplier": "x50"}, {"name": "@acid2u", "balance": "3", "multiplier": "x5"}]

F = open('data_file1.p', 'wb')
pickle.dump(info_1, F)
F.close()
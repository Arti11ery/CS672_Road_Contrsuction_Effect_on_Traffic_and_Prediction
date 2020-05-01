data = np.load('data/FILTER_RESULT.npy', allow_pickle=True).item()
threshold = 5
i = 0
for key, value in data.items():
    if len(value) > 5:
        i += 1
        print(key,":",value)
print('number of constructions:', i)
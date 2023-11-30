import os

for root, dirs, files in os.walk("../../../ethereum-tests/GeneralStateTests/VMTests/"):
    for file in files:
        print('include_str!("{}"),'.format(os.path.join(root, file)))

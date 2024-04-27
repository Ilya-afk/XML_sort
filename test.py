import shutil


for i in range(100000):
    shutil.copy('input_data/input.xml', f'input_data/input{i}.xml')


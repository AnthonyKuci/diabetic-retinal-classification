from os import listdir
import os

from os.path import isfile, join
from nn_final_image.ETools import EImage
import cv2
import pandas as pd

path_base_train = 'final_data/pre1_train'
path_base_train_destination = 'final_data/pre1_preprocessed_train'

train_files = [f for f in listdir(path_base_train) if isfile(join(path_base_train, f))]
print(train_files[0])

df_train_class_label  = pd.read_csv('a. IDRiD_Disease Grading_Training Labels.csv')

size_total = len(train_files)
index_done = 0

if not os.path.exists(path_base_train_destination):
    os.makedirs(path_base_train_destination)

print('total file size: {}'.format(size_total))
count_skip = 0
for train_file_name in train_files:
    if '.jpg' not in train_file_name:
        count_skip +=1
        print('{} skipped'.format(train_file_name))
        continue

    print('-------\n{} processing started...'.format(train_file_name))

    image_name = train_file_name.split('.')[0]
    class_label = df_train_class_label.loc[df_train_class_label['Image name'] == image_name].iloc[0, df_train_class_label.columns.get_loc('Risk of macular edema')]
    print('class label is: {}'.format(class_label))

    image_name_destination = '{cl}_{file_name}'.format(cl=class_label, file_name=train_file_name)

    img = EImage.read_image('{}/{}'.format(path_base_train, train_file_name),if_read_as_grayscale=True)

    EImage.save_image('{}/{}'.format(path_base_train_destination,image_name_destination), img)
    print('{} done. {}% completed'.format(image_name_destination, round(index_done*100/size_total),1))
    index_done+=1

print('total: {}\ndone: {}\nskipped: {}'.format(size_total, index_done, count_skip))

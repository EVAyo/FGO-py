import os
import cv2
import numpy
import tqdm
path='friend/unused'
for i in tqdm.tqdm(os.listdir(path)):
    if not i.endswith('.png'):continue
    cv2.imwrite(
        f'{path}/{i}',
        cv2.resize(cv2.imread(f'{path}/{i}',cv2.IMREAD_UNCHANGED),(0,0),fx=2/3,fy=2/3,interpolation=cv2.INTER_CUBIC),
        [cv2.IMWRITE_PNG_COMPRESSION,9]
    )
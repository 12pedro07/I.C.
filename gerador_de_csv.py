import csv
import cv2
import time
import os
from dodo_detector import KeypointObjectDetector, SSDObjectDetector
from os.path import isfile, join
from tqdm import tqdm

test_images_direct = 'test_images'
bases_sift = [join('bases_sift/2018', base) for base in os.listdir('bases_sift/2018') if base != "originais"]
log_file = 'logfile.csv'
photos = sorted([join(test_images_direct, f) for f in os.listdir(test_images_direct) if isfile(join(test_images_direct, f))])
object_classes = ['medicine',
                  'chocolate_milk',
                  'heineken',
                  'yellow_juice',
                  'red_juice',
                  'purple_juice',
                  'milk_bottle',
                  'milk_box',
                  'cereal',
                  'iron_man',
                  'shampoo',
                  'monster',
                  'tea_box']

tf_frozen_graph = "arquivos_tf/frozen_graph.pb"
tf_label_map = "arquivos_tf/label_map.pbtxt"
num_classes = 13
ssd_detector = SSDObjectDetector.SSDObjectDetector(tf_frozen_graph, tf_label_map, num_classes)


def detect_and_log(photo, detector, detector_name, log_file, pontos=None, base=None):
    # Criando o CSV, se ele não existir
    if not os.path.exists(log_file):
        with open(log_file, 'a') as csvfile:
            objectwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            objectwriter.writerow(['detector', 'pontos', 'base', 'frame_rate', 'image'] + object_classes)

    img = cv2.imread(photo)
    start = time.time()
    f, d = detector.from_image(img)  # SIFT executado de fato aqui
    end = time.time()
    frame_rate = end-start
    with open(log_file, 'a') as csvfile:
        objectwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        list_csv = [detector_name, pontos, base, frame_rate, photo] + [0] * 13

        if len(d) != 0:
            for item in d:
                if item in object_classes:
                    index = object_classes.index(item)
                    list_csv[index + 5] = 1

        objectwriter.writerow(list_csv)


for photo in tqdm(iterable=photos, desc='Test image',):
    detect_and_log(photo, ssd_detector, 'ssd', log_file)

for metodo in ['SIFT', 'RootSIFT']:
    for pontos in range(10, 51, 10):
        for base in tqdm(bases_sift):
            sift_detector = KeypointObjectDetector.KeypointObjectDetector(base, metodo, 'BF', pontos)
            for photo in photos:
                detect_and_log(photo, sift_detector, metodo, log_file, pontos, base)

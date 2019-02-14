# -*- coding: utf-8 -*-

import json
import cv2
import os
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='visual the detectron detection results')
    parser.add_argument(
        '--ann',
        dest='annFile',
        help='/path/to/annotation',
        default=None, type=str
    )
    parser.add_argument(
        '--dir',
        dest='im_dir',
        help='/path/to/image/',
        default=None,
        type=str
    )
    parser.add_argument(
        '--threshold',
        dest= 'threshold',
        help='the threshold to visual results',
        default= 0.5,
        type= float)
    parser.add_argument(
        '--bbox',
        dest='bbox_path',
        help='/path/to/bbox/result.json',
        default=None,
        type=str
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main(args):
    path = args.bbox_path
    img_dir = args.im_dir
    ann_path = args.annFile
    threshold = args.threshold

    id_filename = {}
    coco = json.load(open(ann_path))
    images = coco['images']
    for imginfo in images:
        img_id = imginfo['id']
        filename = imginfo['file_name']
        id_filename[img_id] = filename

    reader = json.load(open(path))
   
    img_id_bboxes_dict = {}
    
    for bbox_info in reader:
        img_id = bbox_info['image_id']
        category_id = bbox_info['category_id']
        bbox = bbox_info['bbox']
        bbox = [int(x) for x in bbox]
        score = bbox_info['score']
        bbox = bbox + [category_id] + [score]
        if img_id in img_id_bboxes_dict:
            img_id_bboxes_dict[img_id].append(bbox)
        else:
            img_id_bboxes_dict[img_id] = [bbox]

    for img_id in img_id_bboxes_dict:
        filename = id_filename[img_id]
        filepath = os.path.join(img_dir,filename)
        im = cv2.imread(filepath)
        bboxes = img_id_bboxes_dict[img_id]
        for box in bboxes:
            bbox = box[:4]
            category_id = box[4]
            score = box[5]
            if score > threshold:
                cv2.rectangle(im,(bbox[0],bbox[1]),(bbox[0] + bbox[2],bbox[1] + bbox[3]),(255,0,0))
        cv2.imshow("im",im)
        key = cv2.waitKey(0)
        if key == ord('q'):
             break

if __name__ == '__main__':
    args = parse_args()
    main(args)

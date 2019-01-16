import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import imghdr
import os

def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()

#lxl add for detect dir imgs
def my_detect_img(yolo):
    for image_file in os.listdir(FLAGS.input):
        print(image_file)
        try:
            image_type = imghdr.what(os.path.join(FLAGS.input, image_file))
            #print('image_type',image_type)
            if not image_type:
                continue
        except IsADirectoryError:
            continue
        image = Image.open(os.path.join(FLAGS.input, image_file))
        print('image.width:{},image.height:{}'.format(image.width, image.height))
        r_image = yolo.detect_image(image)
        r_image.save(os.path.join(FLAGS.output, image_file), quality=90)

    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        #if "input" in FLAGS:
        #   print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        #detect_img(YOLO(**vars(FLAGS)))
        my_detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")

#   python yolo_video.py --input ./image --output ./img_output --image
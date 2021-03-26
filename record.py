import numpy as np
import cv2
import pyautogui
import argparse
from datetime import date
import time
import os


def process_args(args):
    res = (1920,1080)
    codec = "mp4v"
    codec_list = ["divx", "mjpg", "xvid", "mp4v", "x264"]
    this_date = date.today().strftime("%Y%m%d")
    default_ext = "mp4"
    path = os.path.abspath(".")
    dir_content = len([lst for lst in [file.split(this_date)for file in os.listdir(path)] if lst[0]==''])
    fps = 60.0
    
    args = vars(args)
    input_res = args['res']
    input_codec = args['codec']
    input_outfile = args['out']
    input_fps = args['fps']

    if(input_res):
        try:
            h,w = input_res.split(",")
            res = (int(h), int(w))
        except:
            pass

    if(input_codec):
        if(input_codec.lower() in codec_list):
            codec = input_codec.lower()
    
    if(input_outfile):
        name_ext = len(input_outfile.split("."))
        if(name_ext > 1):
            out = input_outfile
        else:
            out = "{}.{}".format(input_outfile, default_ext)
    else:
        if(dir_content==0):
            out = "{}.{}".format(this_date, default_ext)    
        else:
            out = "{} ({}).{}".format(this_date, dir_content+1, default_ext)

    if(input_fps):
        fps = input_fps

    args['res'] = res
    args['codec'] = codec
    args['out'] = out
    args['fps'] = fps
    
    return args


def main(debug=True):
    parser = argparse.ArgumentParser(description="Capture your screen")
    parser.add_argument('-r', '--res',
                        required=False,
                        help="The resolution of the video. e.g.: 1921,1080")
    parser.add_argument('-c', '--codec',
                        required=False,
                        help="The video codec for the video. e.g.: mp4v")
    parser.add_argument('-o', '--out',
                        required=False,
                        help="The output file name. e.g.: test.mp4")
    parser.add_argument('-f', '--fps',
                        required=False,
                        help="The frame rate for the video. e.g.: 60.0",
                        type=float)
                        
    args = parser.parse_args()
    processed_args = process_args(args)
    if(debug):
        print(processed_args)
    codec = cv2.VideoWriter_fourcc(*processed_args['codec'])
    video_writer = cv2.VideoWriter(processed_args['out'],
                                    codec,
                                    processed_args['fps'],
                                    processed_args['res'])
    cv2.namedWindow("Live Screen", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live Screen", 480, 270)
    start_time = time.process_time()
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_writer.write(frame)
        cv2.imshow('Live Screen', frame)
        if cv2.waitKey(1) == ord('q'):
         break
    end_time = time.process_time()
    
    video_writer.release()
    cv2.destroyAllWindows()

    print("Screen recorded time", end_time - start_time)


if __name__=="__main__":
    
    main()
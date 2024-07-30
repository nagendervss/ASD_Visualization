import argparse, os, cv2, subprocess
from tools import *

def parser():

    args_parser = argparse.ArgumentParser(description='Script to visualize ASD results.')

    args_parser.add_argument('--csv_file_path', type=str, required=True, help='Path to the csv file containing the Active Speaker labels')
    args_parser.add_argument('--source_video_path', type=str, required=True, help='Path to the source video file - the video that is to be marked with active speaker detections.')
    args_parser.add_argument('--marked_video_path', type=str, help='Path to the video marked with active speaker detections. Please note that the output video has to have the extension mp4. If this path is not specified, then the video will be saved to the same path as the source video after appending _marked to the source video name.')
    args_parser.add_argument('--vid', type=str, help='ID of the source video in the csv file with labels. If this argument is not provided, then the ID will be inferred from the source file name.')

    args = args_parser.parse_args()

    return args

def read_labels(label_file_path, fps):

    all_lines = read_csv(label_file_path)
    label_info_dict = {}

    for line in all_lines:

        if line[0] == 'video_id':

            assert line[1] == 'frame_timestamp'
            assert line[2] == 'entity_box_x1'
            assert line[3] == 'entity_box_y1'
            assert line[4] == 'entity_box_x2'
            assert line[5] == 'entity_box_y2'
            assert line[8] == 'label_id'
            continue

        vid = line[0]
        frame_time = float(line[1])
        frame_number = int(frame_time * fps)
        tl_x = float(line[2])
        tl_y = float(line[3])
        br_x = float(line[4])
        br_y = float(line[5])
        bbx = [tl_x, tl_y, br_x, br_y]
        label = int(line[8])

        if vid not in label_info_dict.keys():
            label_info_dict[vid] = {}
        
        if frame_number not in label_info_dict[vid].keys():
            label_info_dict[vid][frame_number] = []
        
        label_info_dict[vid][frame_number].append([bbx, label])

    return label_info_dict

if __name__=='__main__':

    args=parser()

    if args.marked_video_path is None:
        source_video_path_parts = os.path.splitext(args.source_video_path)
        args.marked_video_path = source_video_path_parts[0] + '_marked.mp4'

    if args.vid is None:
        args.vid = os.path.splitext(os.path.split(args.source_video_path)[1])[0]

    fps = get_video_fps(args.source_video_path)
    asd_label_info_dict = read_labels(args.csv_file_path, fps)

    

    vid_cap = cv2.VideoCapture(args.source_video_path)

    frame_counter = -1
    frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    print('fourcc: ', fourcc)

    out_video = cv2.VideoWriter(args.marked_video_path, fourcc, fps, (frame_width, frame_height))

    while(vid_cap.isOpened()):

        success,img = vid_cap.read()
        if success:
            frame_counter = frame_counter + 1
            if frame_counter not in asd_label_info_dict[args.vid].keys():
                out_video.write(img)
                continue
            for bbx in asd_label_info_dict[args.vid][frame_counter]:
                
                if bbx[1] == 1:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                
                tl_x = int(frame_width * bbx[0][0])
                tl_y = int(frame_height * bbx[0][1])
                br_x = int(frame_width * bbx[0][2])
                br_y = int(frame_height * bbx[0][3])

                img = cv2.rectangle(img, (tl_x, tl_y), (br_x, br_y), color, thickness=3)
            out_video.write(img)
            
        else:
            break
    
    vid_cap.release()
    out_video.release()

    tmp_audio_path = os.path.splitext(args.source_video_path)[0] + '.wav'
    marked_video_path_parts = os.path.splitext(args.marked_video_path)
    marked_video_with_audio_path = marked_video_path_parts[0] + '_with_audio' + marked_video_path_parts[1]
    generate_audio_from_video(args.source_video_path, tmp_audio_path)
    add_audio_to_video(tmp_audio_path, args.marked_video_path, marked_video_with_audio_path)
    cmd = f'rm {tmp_audio_path}'
    subprocess.call(cmd, shell=True)
import csv, cv2, subprocess

def read_csv(csv_file_path, delimiter=','):

    with open(csv_file_path, 'r') as f:
        csvreader = csv.reader(f, delimiter=delimiter)
        all_lines = list(csvreader)
    
    return all_lines

def get_video_fps(video_path):

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def generate_audio_from_video(source_video_path, target_audio_path):
    cmd = f'ffmpeg -i {source_video_path} {target_audio_path}'
    subprocess.run(cmd, shell=True)

def add_audio_to_video(source_audio_path, source_video_path, target_video_path):

    cmd = f'ffmpeg -i {source_video_path} -i {source_audio_path} -c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 {target_video_path}'
    subprocess.run(cmd, shell=True)
    
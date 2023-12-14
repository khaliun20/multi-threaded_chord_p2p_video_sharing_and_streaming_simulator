import os
import subprocess
import json

def compress_video(input_video, output_folder, bitrates):
    for bitrate in bitrates:
        bitrate_folder = f'{output_folder}/{bitrate}'
        os.makedirs(bitrate_folder, exist_ok=True)
        
        output_file = f'{bitrate_folder}/output_{bitrate}.mp4'
        command = (
            f'ffmpeg -i {input_video} -c:v libx264 -b:v {bitrate}k -c:a aac -b:a 128k '
            f'-profile:v baseline -preset slow -s 640x360 {output_file}'
        )
        subprocess.run(command, shell=True)

def split_video(output_folder, bitrates, segment_duration):
    for bitrate in bitrates:
        bitrate_folder = f'{output_folder}/{bitrate}'
        os.makedirs(bitrate_folder, exist_ok=True)
        
        command = (
            f'ffmpeg -i {bitrate_folder}/output_{bitrate}.mp4 -c copy -map 0 -f segment '
            f'-segment_time {segment_duration} -reset_timestamps 1 {bitrate_folder}/output_%03d.mp4'
        )
        subprocess.run(command, shell=True)

def generate_json(output_folder, bitrates, segment_duration_ms):
    manifest = {
        "segment_duration_ms": segment_duration_ms,
        "bitrates_kbps": bitrates,
        "segment_sizes_bits": []
    }

    dic = {}
    for bitrate in bitrates:
        bitrate_folder = f'{output_folder}/{bitrate}'

        # Assuming files are named output_001.mp4, output_002.mp4, ..., output_010.mp4
        segment_sizes = []

        for i, segment_file in enumerate(sorted(os.listdir(bitrate_folder))):
            if segment_file.startswith('output_0') and segment_file.endswith('.mp4'):
                segment_path = os.path.join(bitrate_folder, segment_file)
                segment_size = os.path.getsize(segment_path) * 8  # Convert to bits
                segment_sizes.append(segment_size)

        # manifest["segment_sizes_bits"].append(segment_sizes)
        dic[bitrate] = segment_sizes

    for i in range(len(dic[bitrates[0]])):
        temp = []
        for bitrate in bitrates:
            temp.append(dic[bitrate][i])
        manifest["segment_sizes_bits"].append(temp)
    
    with open(f'{output_folder}/manifest.json', 'w') as json_file:
        json.dump(manifest, json_file, indent=2)


if __name__ == "__main__":
    make_video = True
    input_video = './videos/input_video.mp4'
    output_folder = 'videos'
    bitrates = [50, 100, 200, 500, 1000]
    segment_duration_ms = 1000  # 1 second per segment
    if make_video:
        print("\n\n\n\n\n\n\nCompressing video...")
        compress_video(input_video, output_folder, bitrates)
        print("\n\n\n\n\n\n\nSplitting video...")
        split_video( output_folder, bitrates, segment_duration_ms / 1000)
    print("\n\n\n\n\n\nGenerating manifest...")
    generate_json(output_folder, bitrates, segment_duration_ms)

import os
import sys
import subprocess
from pytubefix import YouTube
import re
import shutil
from typing import List, Dict

DEFAULT_DOWNLOAD_PATH = r"E:\Video\YouTube"

def sanitize_filename(name: str) -> str:
    safe = re.sub(r'[^A-Za-z0-9]', '_', name)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')

def get_available_resolutions(yt: YouTube) -> List[Dict[str, str]]:
    """Получает все доступные разрешения видео"""
    video_streams = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True)
    resolutions = []
    
    for stream in video_streams:
        resolution = stream.resolution
        if resolution and resolution not in [r['resolution'] for r in resolutions]:
            resolutions.append({
                'resolution': resolution,
                'fps': stream.fps,
                'filesize': stream.filesize,
                'stream': stream
            })
    
    # Сортируем по разрешению (от большего к меньшему)
    resolutions.sort(key=lambda x: int(x['resolution'].split('p')[0]) if x['resolution'] else 0, reverse=True)
    return resolutions

def display_resolutions(resolutions: List[Dict[str, str]]) -> None:
    """Отображает список доступных разрешений"""
    print("\nДоступные разрешения:")
    print("-" * 50)
    for i, res in enumerate(resolutions, 1):
        fps_text = f" @ {res['fps']}fps" if res['fps'] else ""
        size_text = f" ({res['filesize'] // (1024*1024)}MB)" if res['filesize'] else ""
        print(f"{i:2d}. {res['resolution']}{fps_text}{size_text}")
    print("-" * 50)

def select_resolution(resolutions: List[Dict[str, str]]) -> Dict[str, str]:
    """Позволяет пользователю выбрать разрешение"""
    while True:
        try:
            choice = input(f"\nВыберите разрешение (1-{len(resolutions)}): ").strip()
            if not choice:
                print("Пожалуйста, введите номер разрешения.")
                continue
                
            choice_num = int(choice)
            if 1 <= choice_num <= len(resolutions):
                return resolutions[choice_num - 1]
            else:
                print(f"Пожалуйста, введите число от 1 до {len(resolutions)}.")
        except ValueError:
            print("Пожалуйста, введите корректное число.")
        except KeyboardInterrupt:
            print("\nОперация отменена пользователем.")
            sys.exit(0)

def download_youtube_video(url: str, output_path: str = DEFAULT_DOWNLOAD_PATH) -> None:
    os.makedirs(output_path, exist_ok=True)
    tmp_path = os.path.join(output_path, "tmp")
    os.makedirs(tmp_path, exist_ok=True)

    print("Initializing YouTube video...")
    yt = YouTube(url)
    
    print(f"Название видео: {yt.title}")
    print(f"Автор: {yt.author}")
    print(f"Длительность: {yt.length // 60}:{yt.length % 60:02d}")

    # Получаем все доступные разрешения
    resolutions = get_available_resolutions(yt)
    
    if not resolutions:
        print("Не удалось найти доступные разрешения видео.")
        return
    
    # Показываем разрешения и позволяем пользователю выбрать
    display_resolutions(resolutions)
    selected_resolution = select_resolution(resolutions)
    
    print(f"\nВыбрано разрешение: {selected_resolution['resolution']}")
    
    # Используем выбранное разрешение для видео потока
    video_stream = selected_resolution['stream']
    audio_stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first()

    if not video_stream or not audio_stream:
        print("Could not find suitable video/audio streams.")
        return

    base_name = sanitize_filename(yt.title)
    resolution_suffix = selected_resolution['resolution'].replace('p', '')
    base_name_with_resolution = f"{base_name}_{resolution_suffix}"
    
    video_file = os.path.join(tmp_path, f"{base_name_with_resolution}_video.mp4")
    audio_file = os.path.join(tmp_path, f"{base_name_with_resolution}_audio.mp4")
    output_file = os.path.join(output_path, f"{base_name_with_resolution}.mp4")

    if os.path.exists(output_file):
        print(f"File already exists: {output_file}")
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        return

    try:
        print("Downloading video stream...")
        video_stream.download(output_path=tmp_path, filename=f"{base_name_with_resolution}_video.mp4")
        print("Video downloaded.")

        print("Downloading audio stream...")
        audio_stream.download(output_path=tmp_path, filename=f"{base_name_with_resolution}_audio.mp4")
        print("Audio downloaded.")

        if not os.path.exists(video_file) or not os.path.exists(audio_file):
            print("Error: one of the files was not downloaded.")
            return

        print("Merging video and audio with ffmpeg...")
        subprocess.run(f'ffmpeg -y -i "{video_file}" -i "{audio_file}" -c copy "{output_file}"', shell=True)
        print(f"Download complete: {output_file}")

    finally:
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_youtube.py <YouTube_URL> [Output_Folder]")
        sys.exit(1)

    video_url = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_DOWNLOAD_PATH

    download_youtube_video(video_url, save_path)

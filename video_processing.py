import cv2
import numpy as np
import tempfile
import os
from moviepy import VideoFileClip


def enhance_video(video_file, kernel):
    # Сохранение во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
        temp_input.write(video_file.getbuffer())
        input_path = temp_input.name

    # Обработка видео
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Подготовка выходного файла
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output:
        output_path = temp_output.name
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = cv2.filter2D(frame, -1, kernel)
            out.write(processed_frame)

        cap.release()
        out.release()

    # Микширование аудио
    final_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    video_clip = VideoFileClip(output_path)
    audio_clip = VideoFileClip(input_path).audio

    if audio_clip:
        video_clip.audio = audio_clip

    video_clip.write_videofile(
        final_output,
        codec='libx264',
        audio_codec='aac',
        logger=None
    )

    # Очистка временных файлов
    for path in [input_path, output_path]:
        if os.path.exists(path):
            os.remove(path)

    return final_output
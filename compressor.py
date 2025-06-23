# compressor.py
import os
from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
import moviepy.editor as mp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('compressor_imgvid.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['file']
    filename = file.filename.lower()
    buffer = BytesIO()

    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img = Image.open(file.stream)
        img_format = img.format
        if img_format == 'JPEG':
            img.save(buffer, format='JPEG', quality=85, optimize=True)
        elif img_format == 'PNG':
            img.save(buffer, format='PNG', optimize=True)
        else:
            return "The image format are not suported", 400
        buffer.seek(0)
        return send_file(buffer, mimetype=f'image/{img_format.lower()}', as_attachment=True, download_name=f'compressed.{img_format.lower()}')

    elif filename.endswith('.mp4'):
        # Salva temporariamente o vídeo
        temp_input = 'temp_input.mp4'
        temp_output = 'temp_output.mp4'
        file.save(temp_input)
        # Reduz bitrate para comprimir (ajuste conforme necessário)
        clip = mp.VideoFileClip(temp_input)
        clip.write_videofile(temp_output, bitrate="800k", audio_codec='aac', threads=2, logger=None)
        with open(temp_output, 'rb') as f:
            buffer.write(f.read())
        buffer.seek(0)
        os.remove(temp_input)
        os.remove(temp_output)
        return send_file(buffer, mimetype='video/mp4', as_attachment=True, download_name='compressed.mp4')

    else:
        return "Format not suported. Send JPG, PNG or MP4.", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
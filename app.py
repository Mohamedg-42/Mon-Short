import os
import subprocess
from flask import Flask, request, render_template, Response

app = Flask(__name__)

# Chemin vers yt-dlp (adapté pour l'hébergement)
YTDLP_PATH = 'yt-dlp'  # Utilisation de la commande directement car installée via pip

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download_video():
    video_url = request.args.get('url')
    quality = request.args.get('quality', 'best')
    format_type = request.args.get('format', 'mp4')
    
    print(f"URL reçue: {video_url}")
    print(f"Qualité demandée: {quality}")
    print(f"Format demandé: {format_type}")

    if not video_url:
        return "URL manquante", 400

    try:
        # Construire la commande en fonction des options
        cmd = [YTDLP_PATH]
        
        # Configuration de la qualité
        if quality == 'best':
            cmd.extend(['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'])
        elif quality == '720p':
            cmd.extend(['-f', 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'])
        elif quality == '480p':
            cmd.extend(['-f', 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'])
        elif quality == '360p':
            cmd.extend(['-f', 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best'])

        # Configuration du format
        if format_type == 'audio':
            cmd.extend(['-x', '--audio-format', 'mp3'])
            mime_type = 'audio/mpeg'
            file_extension = 'mp3'
        else:
            cmd.extend(['--merge-output-format', 'mp4'])
            mime_type = 'video/mp4'
            file_extension = 'mp4'

        # Options communes optimisées pour la performance
        cmd.extend([
            '--no-playlist',
            '--no-warnings',
            '--quiet',
            '--no-check-certificates',
            '--buffer-size', '16M',
            '--http-chunk-size', '10M',
            '--concurrent-fragments', '4',
            '--no-cache-dir',
            '--no-mtime',
            '--no-simulate',
            '-o', '-',
            video_url
        ])

        print(f"Commande exécutée: {' '.join(cmd)}")

        # Lancer le processus avec un buffer plus grand
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=16*1024*1024
        )

        def generate():
            try:
                while True:
                    chunk = process.stdout.read(16*1024*1024)
                    if not chunk:
                        break
                    yield chunk
            except Exception as e:
                print(f"Erreur lors de la génération du flux: {str(e)}")
                import traceback
                print(f"Traceback complet: {traceback.format_exc()}")
            finally:
                process.terminate()
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()

        return Response(
            generate(),
            mimetype=mime_type,
            headers={
                'Content-Disposition': f'attachment; filename="video.{file_extension}"',
                'Content-Type': mime_type,
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Accept-Ranges': 'bytes',
                'Content-Length': '-1'
            }
        )

    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        import traceback
        print(f"Traceback complet: {traceback.format_exc()}")
        return f"Erreur serveur inattendue: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
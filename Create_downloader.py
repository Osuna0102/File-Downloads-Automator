import os
import shutil
import time

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Main download folder
source_dir = r"D:\\Descargas"

# Add new folder if needed
destination_dir_sfx = os.path.join(source_dir, "SFX")
destination_dir_music = os.path.join(source_dir, "Audios")
destination_dir_video = os.path.join(source_dir, "Videos")
destination_dir_image = os.path.join(source_dir, "Imagenes")

destination_dir_pdf = os.path.join(source_dir, "Documentos\\PDFs")
destination_dir_pdf_words = os.path.join(source_dir, "Documentos")


destination_dir_arch_comp = os.path.join(source_dir, "ZIPs")
destination_dir_book = os.path.join(source_dir, "Books")

destination_dir_torrent = os.path.join(source_dir, "Torrents")
destination_dir_exe = os.path.join(source_dir, "Exe")



# Extensions
image_extensions = (".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt",
                    ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico")
video_extensions = (".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mkv", ".mp4", ".mp4v", ".m4v", ".avi",
                    ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd")
audio_extensions = (".m4a", ".flac", "mp3", ".wav", ".wma", ".aac")
pdf_extensions = (".pdf", ".pdfk")
arch_comp_extensions = (".7z", ".apk", ".ark", ".arc", ".arj", ".a", ".ar", ".cab", ".car", ".cpio", ".dmg", ".ear",
                        ".gca", ".genozip", ".pak", ".partimg", ".paq6", ".paq7", ".paq8", ".rar", ".shk", ".sit",
                        ".sitx", ".sqx", ".gz", ".tgz", ".bz2", ".tbz2", ".tlz", ".txz", ".shar", ".lbr",
                        ".iso", ".mar", ".sbx", ".tar", ".f", ".lz", ".lz4", ".lzma", ".lzo", ".rz", ".sfark", ".sz",
                        ".q", ".xz", ".z", ".zst", ".war", ".wim", ".uca", ".uha", ".xar", ".xp3", ".yz1",
                        ".zip", ".zipx", ".zoo", ".zpaq", ".zz")

book_extensions = (".epub")

word_extensions = (".docx",".xlsx",".pptx")

torrent_extensions = (".torrent", ".srt")

exe_extensions = (".exe")




def make_unique(destination, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(destination, name)):
        name = f"{filename} ({counter}){extension}"
        counter += 1
    return name


def move(destination, entry, name):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)

        if not os.path.exists(os.path.join(destination, name)):
            shutil.move(entry.path, os.path.join(destination, name))

        else:
            unique_name = make_unique(destination, name)
            shutil.move(entry.path, os.path.join(destination, unique_name))
    except Exception as e:
        logging.error(f'move() -> destination {destination}; entry {entry}; name {name}')
        logging.error(f'Exception throwed: {e}')


class Handler(FileSystemEventHandler):

    def on_created(self, event):
        path_split = event.src_path.split('\\')
        path_split = path_split[:-1]
        path_join = '\\'.join(path_split)

        with os.scandir(path_join) as entries:
            for entry in entries:
                name = entry.name

                if name.lower().endswith(tuple(audio_extensions)):
                    print(f'Moving sound {name}')
                    move(destination_dir_sfx, entry, name)

                elif name.lower().endswith(tuple(video_extensions)):
                    print(f'Moving video {name}')
                    move(destination_dir_video, entry, name)

                elif name.lower().endswith(tuple(image_extensions)):
                    print(f'Moving image {name}')
                    move(destination_dir_image, entry, name)

                elif name.lower().endswith(tuple(pdf_extensions)):
                    print(f'Moving pdf {name}')
                    move(destination_dir_pdf, entry, name)

                elif name.lower().endswith(tuple(arch_comp_extensions)):
                    print(f'Moving zip {name}')
                    move(destination_dir_arch_comp, entry, name)

                elif name.lower().endswith(tuple(book_extensions)):
                    print(f'Moving book {name}')
                    move(destination_dir_book, entry, name)

                elif name.lower().endswith(tuple(word_extensions)):
                    print(f'Moving word {name}'+ f' to  {destination_dir_pdf_words}')
                    move(destination_dir_pdf_words, entry, name)
               

                elif name.lower().endswith(tuple(torrent_extensions)):
                    print(f'Moving torrent {name}')
                    move(destination_dir_torrent, entry, name)   


                elif name.lower().endswith(tuple(exe_extensions)):
                    print(f'Moving exe {name}')
                    move(destination_dir_exe, entry, name)

                else:
                    print(f'File {name} not recognized.')


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='C:\\download-folder.log',
                        encoding='utf-8')
    except PermissionError:
        print('Permission denied to file')
    folder_to_track = source_dir
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, folder_to_track, recursive=False)
    observer.start()
    print('Observer started')
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
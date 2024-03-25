import os
import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QProgressBar, QFileDialog
)
from pytube import YouTube

class QualityUpdater(QThread):
    update_finished = pyqtSignal()

    def __init__(self, url, quality_combo):
        super().__init__()
        self.url = url
        self.quality_combo = quality_combo

    def run(self):
        try:
            yt = YouTube(self.url)
            all_streams = yt.streams

            resolutions = set(
                (stream.resolution, stream.mime_type, stream.type, f"{stream.filesize_mb} MB")
                for stream in all_streams if stream.resolution and 'acodec' in str(stream)
            )
            audio_resolutions = set(
                (stream.abr, stream.mime_type, stream.type, f"{stream.filesize_mb} MB")
                for stream in all_streams if stream.resolution is None
            )
            resolutions = sorted(resolutions, key=lambda x: (int(x[0].replace('p', '')), x[1], x[3]))
            audio_resolutions = sorted(audio_resolutions, key=lambda x: (int(x[0].replace('kbps', '')), x[1], x[3]))

            self.quality_combo.clear()
            self.quality_combo.addItems([
                f"{resolution[0]} - {resolution[1]} - {resolution[2]} - {resolution[3]}"
                for resolution in resolutions
            ])
            self.quality_combo.addItems([
                f"{audio_res[0]} - {audio_res[1]} - {audio_res[2]} - {audio_res[3]}"
                for audio_res in audio_resolutions
            ])
            self.quality_combo.setEnabled(True)

        except Exception as e:
            print(f"An error occurred: {e}")

        self.update_finished.emit()


class DownloadWorker(QThread):
    download_progress = pyqtSignal(int, float)
    download_finished = pyqtSignal(str)
    download_error = pyqtSignal(str)

    def __init__(self, video_url, selected_option, output_path, output_entry):
        super().__init__()
        self.video_url = video_url
        self.selected_option = selected_option
        self.output_path = output_path
        self.output_entry = output_entry

    def run(self):
        try:
            yt = YouTube(self.video_url, on_progress_callback=self.on_download_progress)
            yt.register_on_progress_callback(self.on_download_progress)

            selected_quality, selected_mime_type, stream_type, stream_size = self.selected_option.split(' - ')
            stream_size = float(stream_size.replace(' MB', ''))
            if stream_type == 'audio':
                video_streams = yt.streams.filter(abr=selected_quality, mime_type=selected_mime_type)
            else:
                video_streams = yt.streams.filter(res=selected_quality, mime_type=selected_mime_type)

            video_stream = video_streams.first()

            if video_stream is None:
                raise ValueError("No available streams found for download.")

            self.download_progress.emit(0, stream_size)
            self.output_entry.setEnabled(False)
            video_stream.download(self.output_path)
            self.output_entry.setEnabled(True)
            self.download_finished.emit(video_stream.default_filename)

        except Exception as e:
            self.download_error.emit(str(e))

    def on_download_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_percentage = int((bytes_downloaded / total_size) * 100)
        self.download_progress.emit(progress_percentage, stream.filesize_mb)


class YouTubeDownloaderApp(QWidget):
    DEFAULT_THUMBNAIL_WIDTH = 320
    DEFAULT_THUMBNAIL_HEIGHT = 180

    def __init__(self):
        super().__init__()
        self.filename = ''
        self.filepath = ''
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 500, 250)

        self.url_label = QLabel('YouTube Video URL:')
        self.url_entry = QLineEdit()
        self.url_entry.textChanged.connect(self.update_quality_options)

        self.output_label = QLabel('Output Path:')
        self.output_entry = QLineEdit()
        self.output_entry.setText('.')
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.select_download_path)

        self.quality_label = QLabel('Select Quality:')
        self.quality_combo = QComboBox()
        self.quality_combo.setEnabled(False)

        self.title_label = QLabel('Video Title')
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_video)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setFixedSize(self.DEFAULT_THUMBNAIL_WIDTH, self.DEFAULT_THUMBNAIL_HEIGHT)

        self.open_location_button = QPushButton('Open File Location')
        self.open_location_button.clicked.connect(self.open_file_location)
        self.open_location_button.setEnabled(False)

        self.open_file_button = QPushButton('Open Downloaded File')
        self.open_file_button.clicked.connect(self.open_downloaded_file)
        self.open_file_button.setEnabled(False)

        self.status_label = QLabel('')
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.url_label)
        form_layout.addWidget(self.url_entry)
        form_layout.addWidget(self.output_label)
        form_layout.addWidget(self.output_entry)
        form_layout.addWidget(self.browse_button)
        form_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.thumbnail_label, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.quality_label)
        form_layout.addWidget(self.quality_combo)
        form_layout.addWidget(self.download_button)
        form_layout.addWidget(self.status_label)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.open_location_button)
        button_layout.addWidget(self.open_file_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)
        self.show()

    def update_quality_options(self):
        url = self.url_entry.text()

        # Stop previous thread if running
        if hasattr(self, 'quality_thread') and self.quality_thread.isRunning():
            self.quality_thread.quit()
            self.quality_thread.wait()

        self.quality_thread = QualityUpdater(url, self.quality_combo)
        self.quality_thread.update_finished.connect(self.quality_update_finished)
        self.quality_thread.start()

        # Fetch video thumbnail URL and update the thumbnail
        try:
            yt = YouTube(url)
            thumbnail_url = yt.thumbnail_url
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            resized_pixmap = pixmap.scaledToWidth(self.DEFAULT_THUMBNAIL_WIDTH, Qt.SmoothTransformation)
            self.thumbnail_label.setPixmap(resized_pixmap)

            title = yt.title
            self.title_label.setText(title)
        except Exception as e:
            print(f"Error fetching thumbnail: {e}")

    def quality_update_finished(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def download_video(self):
        video_url = self.url_entry.text()
        selected_option = self.quality_combo.currentText()

        self.download_button.setEnabled(False)

        try:
            self.download_thread = DownloadWorker(video_url, selected_option, self.filepath, self.output_entry)
            self.download_thread.download_progress.connect(self.update_download_progress)
            self.download_thread.download_finished.connect(self.download_finished)
            self.download_thread.download_error.connect(self.handle_download_error)
            self.download_thread.start()

        except Exception as e:
            self.status_label.setText(f"An error occurred: {e}")
            self.download_button.setEnabled(True)

    def update_download_progress(self, progress, total_size):
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"Downloading... {progress}% ({total_size} MB)")

    def download_finished(self, filename):
        self.filename = filename
        self.status_label.setText(f"Download complete! 🎉")
        self.progress_bar.setValue(100)
        self.download_button.setEnabled(True)
        self.open_location_button.setEnabled(True)
        self.open_file_button.setEnabled(True)

    def select_download_path(self):
        download_path = QFileDialog.getExistingDirectory(self, 'Select Download Path', '.', QFileDialog.ShowDirsOnly)
        if download_path:
            self.output_entry.setText(download_path)
        self.filepath = download_path

    def handle_download_error(self, error_message):
        self.status_label.setText(f"Download error: {error_message}")
        self.download_button.setEnabled(True)

    def open_file_location(self):
        output_path = self.output_entry.text()
        os.startfile(output_path)

    def open_downloaded_file(self):
        file_path = os.path.join(self.filepath, self.filename)
        os.startfile(file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader_app = YouTubeDownloaderApp()
    sys.exit(app.exec_())

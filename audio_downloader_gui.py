import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import threading
import subprocess
import os

class AudioDownloaderGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Audio Downloader")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # YouTube URL entry
        url_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        url_label = Gtk.Label(label="YouTube URL:", xalign=0)
        self.url_entry = Gtk.Entry()
        url_box.pack_start(url_label, False, False, 0)
        url_box.pack_start(self.url_entry, True, True, 0)
        vbox.pack_start(url_box, False, False, 0)

        # Output folder chooser
        folder_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        folder_label = Gtk.Label(label="Output Folder:", xalign=0)
        self.folder_entry = Gtk.Entry()
        self.folder_button = Gtk.Button(label="Choose...")
        self.folder_button.connect("clicked", self.on_choose_folder)
        folder_box.pack_start(folder_label, False, False, 0)
        folder_box.pack_start(self.folder_entry, True, True, 0)
        folder_box.pack_start(self.folder_button, False, False, 0)
        vbox.pack_start(folder_box, False, False, 0)

        # Download button
        self.download_button = Gtk.Button(label="Download")
        self.download_button.connect("clicked", self.on_download_clicked)
        vbox.pack_start(self.download_button, False, False, 0)

        # Status label (multi-line)
        self.status_label = Gtk.Label(label="", xalign=0)
        self.status_label.set_line_wrap(True)
        vbox.pack_start(self.status_label, False, False, 0)

        # Track download thread
        self.download_thread = None

    def on_choose_folder(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select Output Folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.folder_entry.set_text(dialog.get_filename())
        dialog.destroy()

    def on_download_clicked(self, widget):
        url = self.url_entry.get_text().strip()
        folder = self.folder_entry.get_text().strip()
        if not url:
            self.status_label.set_text("Please enter a YouTube URL.")
            return
        if not folder:
            self.status_label.set_text("Please select an output folder.")
            return
        # Disable button to prevent multiple downloads
        self.download_button.set_sensitive(False)
        self.status_label.set_text("Starting download...")
        # Start download in a background thread
        self.download_thread = threading.Thread(
            target=self.run_download,
            args=(url, folder),
            daemon=True
        )
        self.download_thread.start()

    def run_download(self, url, folder):
        # Build the yt-dlp command (mirroring audio_downloader.py)
        output_folder = os.path.expanduser(folder)
        command = [
            "yt-dlp",
            "--ignore-errors",
            "--format", "bestaudio[ext=m4a]",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "160K",
            "-P", output_folder,
            "--output", "%(title)s.%(ext)s",
            "--yes-playlist",
            "--embed-metadata",
            "--embed-thumbnail",
            "--add-metadata",
            "--postprocessor-args", "-id3v2_version 3",
            "--download-archive", os.path.join(output_folder, "downloaded.txt"),
            url
        ]
        try:
            # Ensure output folder exists
            os.makedirs(output_folder, exist_ok=True)
            # Start subprocess and capture output
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            status_lines = []
            for line in process.stdout:
                # Update status label with the latest output
                status_lines.append(line.rstrip())
                # Show only the last 10 lines for brevity
                GLib.idle_add(
                    self.status_label.set_text,
                    "\n".join(status_lines[-10:])
                )
            process.wait()
            if process.returncode == 0:
                GLib.idle_add(
                    self.status_label.set_text,
                    "Download completed successfully."
                )
            else:
                GLib.idle_add(
                    self.status_label.set_text,
                    f"Download failed with exit code {process.returncode}."
                )
        except Exception as e:
            GLib.idle_add(
                self.status_label.set_text,
                f"Error: {str(e)}"
            )
        finally:
            # Re-enable the download button
            GLib.idle_add(self.download_button.set_sensitive, True)

def main():
    win = AudioDownloaderGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
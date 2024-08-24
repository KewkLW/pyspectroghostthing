import config
import moderngl
import time
import pyaudio

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QShortcut, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QLabel

from utils import logger
from source import File, Microphone  # Import the required classes

class Window(QOpenGLWidget):
    frame_rate = 61

    def __init__(self):
        super().__init__()
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setDefaultFormat(fmt)
        fmt.setSamples(4)
        self.setFormat(fmt)

        self.t = None

        QShortcut(Qt.Key_Escape, self, self.quit)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(int(1000 / self.frame_rate))

        # Initialize devices attribute
        self.devices = []

        # Main UI Layout (Vertical)
        main_layout = QVBoxLayout()

        # Horizontal Layout for Dropdowns and Button
        top_layout = QHBoxLayout()

        # Device dropdown
        self.device_dropdown = QComboBox()
        self.device_dropdown.addItem("None")  # Add "None" option
        self.device_dropdown.setFixedWidth(300)  # Set a fixed width
        top_layout.addWidget(QLabel("Audio Device:"))
        top_layout.addWidget(self.device_dropdown)
        self.device_dropdown.currentIndexChanged.connect(self.on_device_selected)

        # Channel dropdown
        self.channel_dropdown = QComboBox()
        self.channel_dropdown.setFixedWidth(300)  # Set a fixed width
        top_layout.addWidget(self.channel_dropdown)

        # File load button
        self.load_button = QPushButton("Load Audio File")
        self.load_button.setFixedWidth(300)  # Set a fixed width
        top_layout.addWidget(self.load_button)
        self.load_button.clicked.connect(self.load_audio_file)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(top_layout)

        container = QWidget(self)
        container.setLayout(main_layout)
        container.setGeometry(10, 10, config.WINDOW_WIDTH - 20, 70)  # Adjusted container size

        # Populate the dropdown with audio devices
        self.populate_audio_devices()

    def populate_audio_devices(self):
        """Populate the dropdown with available audio devices, removing duplicates."""
        p = pyaudio.PyAudio()
        self.device_dropdown.clear()
        self.device_dropdown.addItem("None")  # Add "None" option
        self.devices = []  # Reset the devices list
        device_names = set()  # Track unique device names

        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            device_name = device_info.get('name', f'Device {i}')

            if device_name not in device_names:
                self.device_dropdown.addItem(device_name)
                self.devices.append(device_info)
                device_names.add(device_name)
            else:
                logger.info(f"Duplicate device ignored: {device_name}")

        p.terminate()
        
        logger.info(f"Devices populated: {self.devices}")  # Log the devices list

    def on_device_selected(self):
        """Handle when a new device is selected."""
        selected_index = self.device_dropdown.currentIndex()
        logger.info(f"Selected index: {selected_index}")  # Log the selected index

        if selected_index == 0:  # "None" selected
            self.source = None
            self.channel_dropdown.clear()
        elif selected_index > 0 and selected_index <= len(self.devices):
            # Check if the index is within the valid range
            device_info = self.devices[selected_index - 1]
            logger.info(f"Selected device info: {device_info}")  # Log the selected device info
            self.populate_channels(device_info)

            # Initialize microphone with the selected device
            device_index = selected_index - 1
            channel_index = self.channel_dropdown.currentIndex()
            self.source = Microphone(device_index=device_index, channel_index=channel_index)
            logger.info(f"Microphone initialized on device index {device_index} and channel index {channel_index}")
        else:
            logger.error(f"Selected device index {selected_index - 1} is out of range.")
            self.channel_dropdown.clear()

    def populate_channels(self, device_info):
        """Populate the channels dropdown based on the selected device."""
        self.channel_dropdown.clear()
        channels = device_info['maxInputChannels']
        for i in range(1, channels + 1):
            self.channel_dropdown.addItem(f"Channel {i} (Mono)")
        for i in range(1, channels, 2):
            self.channel_dropdown.addItem(f"Channels {i}-{i+1} (Stereo)")

    def get_selected_device_info(self):
        """Get the selected device info."""
        selected_index = self.device_dropdown.currentIndex()
        return self.devices[selected_index - 1] if selected_index > 0 else None

    def load_audio_file(self):
        """Load an audio file and set it as the source."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
        if filename:
            self.file_path = filename
            self.source = File(self.file_path)  # Now the 'File' class is recognized and used
            self.device_dropdown.setCurrentIndex(0)  # Reset device to "None"
            self.channel_dropdown.clear()

    def initializeGL(self):
        self.ctx = moderngl.create_context(require=330)
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.multisample = True
        self.init()

    def resizeGL(self, w, h):
        self.size(w, h)

    def paintGL(self):
        now = time.time()
        dt = now - self.t if self.t else 1.0 / self.frame_rate
        self.t = now
        self.draw(dt)

    def quit(self):
        self.exit()
        self.close()

    @classmethod
    def run(cls):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication([])
        main = cls()
        main.show()
        app.exit(app.exec())

    #---------------
    #   Interface
    #---------------
    
    def init(self):
        logger.info('init')

    def size(self, w, h):
        logger.info(f'size {w} {h}')

    def draw(self, dt):
        if not self.source:
            return  # No source available to draw

        available = self.source.available()
        logger.info(f"Available windows: {available}")

        for i in range(2):
            window = self.source.get()
            if window is not None:
                self.wave.add(window)
                self.spec.add(window)
            else:
                logger.info("No window data available from the source.")

        self.wave.update()
        self.spec.update()

        for node in self.nodes:
            node.draw()

    def exit(self):
        logger.info('exit')

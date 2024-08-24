# Audio Spectrogram Visualizer

This is a Python application that visualizes audio input as both a waveform and a spectrogram in real-time. The application supports audio input from both files and live microphones.
![image](https://github.com/user-attachments/assets/d3bb9472-8e5a-425e-936b-c29594245a68)

## Features

- **Real-Time Audio Visualization**: Display live spectrograms and waveforms from microphone input or audio files.
- **Multiple Audio Sources**: Select audio input from any available microphone or load audio files (WAV, MP3).
- **Channel Selection**: Choose specific channels for visualization, including mono and stereo options.

## Requirements

- Python 3.8 or higher
- `PyQt5`
- `moderngl`
- `librosa`
- `matplotlib`
- `numpy`
- `pyaudio`

You can install these dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Configuration

This project expects a `config.py` file containing configuration constants. Below is an example of what your `config.py` might look like:

```python
# config.py

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
WINDOW_SIZE = 1024
HOP_SIZE = 512
```

## Running the Application

1. Clone this repository or download the files.
2. Ensure all dependencies are installed.
3. Run the application using:

```bash
python main.py
```

## Usage

- **Select Audio Device**: Use the dropdown menu to select an audio device for input.
- **Select Channel**: Choose the specific channel(s) you want to visualize (Mono or Stereo).
- **Load Audio File**: Click the "Load Audio File" button to choose an audio file (WAV or MP3) for visualization.

### UI Overview

- The application window will display the following:
  - **Top Menu**: Contains dropdowns for selecting the audio device, channels, and a button to load audio files.
  - **Waveform Display**: The upper part of the main window shows the waveform of the audio input.
  - **Spectrogram Display**: The lower part of the main window shows the spectrogram of the audio input.

## Troubleshooting

- If the spectrogram or waveform is not displaying:
  - Ensure your system supports OpenGL 3.3 or higher.
  - Check the console output for any error messages or debug information.
  - Make sure that the selected audio device is working correctly and receiving input.

## Contribution

Feel free to fork the repository and submit pull requests. Contributions are welcome... maybe.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

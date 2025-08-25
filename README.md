# 🎯 Face Recognition Attendance System

A Python-based web application that automatically marks class attendance by detecting faces in uploaded photos and comparing them with a pre-stored dataset of student images.

## ✨ Features

- **🤖 AI-Powered Face Recognition**: Uses advanced face recognition technology to identify students
- **📸 Photo Upload**: Simple drag-and-drop interface for class photos
- **📊 Automatic Attendance**: Instantly marks present/absent students
- **📈 Detailed Reports**: Comprehensive attendance reports with statistics
- **💾 Data Export**: Download attendance data as CSV files
- **📱 Responsive Design**: Modern, mobile-friendly web interface
- **🔒 Local Storage**: All data stored locally on your system
- **📚 History Tracking**: View attendance records from previous sessions

## 🏗️ System Architecture

```
face_attendance_app/
│
├── app.py                     # Flask application entry point
├── requirements.txt           # Python dependencies
├── dataset/                   # Student images (30 photos)
├── models/
│   └── encodings.pkl          # Pre-computed face encodings
├── templates/
│   ├── index.html             # Upload page
│   └── report.html            # Attendance report
│   └── history.html           # Attendance history
├── static/
│   ├── css/style.css          # Custom styling
│   └── js/script.js           # Interactive functionality
├── attendance/
│   └── attendance.csv         # Attendance records
├── uploads/                   # Temporary uploaded files
└── utils/
    ├── face_utils.py          # Face detection & recognition
    ├── db_utils.py            # Database/CSV management
    └── report_utils.py        # Report generation
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Web browser

### Step 1: Clone or Download

```bash
# If using git
git clone <repository-url>
cd FACE_ATTENDANCE

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The `face_recognition` library requires additional system dependencies:

#### Windows:
```bash
# Install Visual Studio Build Tools first
pip install cmake
pip install dlib
pip install face_recognition
```

#### macOS:
```bash
# Install Xcode Command Line Tools first
xcode-select --install
pip install face_recognition
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-dev cmake build-essential
sudo apt-get install libdlib-dev libblas-dev liblapack-dev
pip install face_recognition
```

### Step 3: Prepare Student Dataset

1. Create a `dataset/` folder in your project directory
2. Add student photos (JPG, PNG, GIF format)
3. Name files as: `Student_Name.jpg` (use underscores for spaces)
4. Ensure each photo has a clear, front-facing view of the student's face

**Example dataset structure:**
```
dataset/
├── Alice_Johnson.jpg
├── Bob_Smith.jpg
├── Carol_Davis.jpg
└── ... (30 student photos)
```

### Step 4: Run the Application

```bash
python app.py
```

The application will:
- Create necessary directories
- Generate face encodings for all students
- Start the web server

Open your browser and navigate to: `http://localhost:5000`

## 📖 Usage Guide

### 1. Initial Setup

When you first run the application:
- It will automatically create a sample dataset if none exists
- Generate face encodings for all student photos
- Create the attendance tracking system

### 2. Taking Attendance

1. **Upload Class Photo**: 
   - Take a photo of your class during the session
   - Upload it through the web interface
   - Drag and drop or click to browse

2. **Process Attendance**:
   - Click "Process Attendance"
   - System detects all faces in the photo
   - Matches faces with stored student photos
   - Generates attendance report

3. **View Results**:
   - See who's present/absent
   - Download CSV report
   - View attendance statistics

### 3. Managing Data

- **View History**: Access previous attendance records
- **Export Data**: Download CSV files for record keeping
- **Track Progress**: Monitor attendance patterns over time

## 🔧 Configuration

### Face Recognition Settings

Edit `utils/face_utils.py` to adjust:

```python
self.tolerance = 0.6  # Face recognition tolerance (0.0-1.0)
# Lower = stricter matching, Higher = more lenient
```

### File Upload Limits

Modify `app.py` to change:

```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
```

### Database Settings

The system uses CSV files by default. To use SQLite:

1. Modify `utils/db_utils.py`
2. Implement SQLite database functions
3. Update connection strings

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main upload page |
| `/upload` | POST | Process class photo |
| `/report` | GET | View attendance report |
| `/download_csv/<date>` | GET | Download CSV report |
| `/history` | GET | View attendance history |

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'face_recognition'"**
   - Install system dependencies first
   - Use conda: `conda install -c conda-forge dlib face_recognition`

2. **"No faces detected"**
   - Check photo quality and lighting
   - Ensure faces are clearly visible
   - Try different photo angles

3. **"Low recognition accuracy"**
   - Improve photo quality in dataset
   - Adjust tolerance setting
   - Use consistent lighting conditions

4. **"Port already in use"**
   - Change port in `app.py`: `app.run(port=5001)`
   - Kill existing process: `netstat -ano | findstr :5000`

### Performance Tips

- Use high-quality photos for student dataset
- Ensure good lighting in class photos
- Keep photos under 5MB for faster processing
- Close other applications during processing

## 🔒 Security & Privacy

- **Local Storage**: All data stays on your system
- **No Cloud Upload**: Photos processed locally
- **Data Encryption**: Consider encrypting sensitive data
- **Access Control**: Implement user authentication if needed

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📈 Future Enhancements

- [ ] Real-time video processing
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-class support
- [ ] Email notifications
- [ ] Integration with LMS systems
- [ ] Biometric authentication
- [ ] Cloud backup options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) library
- [OpenCV](https://opencv.org/) for image processing
- [Flask](https://flask.palletsprojects.com/) web framework
- [Bootstrap](https://getbootstrap.com/) for UI components

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for educators and administrators**

*Simplify your attendance tracking with the power of AI!*

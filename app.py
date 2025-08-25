from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd
from utils.face_utils import FaceRecognitionSystem
from utils.db_utils import AttendanceManager
from utils.report_utils import ReportGenerator
import json

app = Flask(__name__)
app.secret_key = 'face_attendance_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Initialize systems
face_system = FaceRecognitionSystem()
attendance_manager = AttendanceManager()
report_generator = ReportGenerator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page for uploading class photos"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process attendance"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            # Create uploads directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process attendance
            print(f"DEBUG: Starting face recognition processing for {filepath}")
            
            # Check for new photos and reload encodings if needed
            face_system.check_and_reload_encodings()
            
            try:
                attendance_results = face_system.process_class_photo(filepath)
                print(f"DEBUG: Face recognition completed. Results: {attendance_results is not None}")
            except Exception as e:
                print(f"DEBUG: Face recognition error: {str(e)}")
                flash(f'Face recognition error: {str(e)}', 'error')
                return redirect(url_for('index'))
            
            if attendance_results:
                print(f"DEBUG: Processing {len(attendance_results)} attendance results")
                # Get detailed processing information
                summary_info = attendance_results[0].get('summary_info', {})
                attendance_summary = summary_info.get('attendance_summary', {})
                processing_summary = summary_info.get('processing_summary', {})
                
                print(f"DEBUG: Summary info: {summary_info}")
                
                # Generate detailed success message
                present_count = attendance_summary.get('present', 0)
                absent_count = attendance_summary.get('absent', 0)
                unknown_count = attendance_summary.get('unknown', 0)
                error_count = attendance_summary.get('errors', 0)
                total_faces = processing_summary.get('total_faces_detected', 0)
                total_students = attendance_summary.get('total_students', 0)
                
                # Build detailed message
                message_parts = []
                message_parts.append(f"✅ Attendance processed successfully!")
                
                if total_faces > 0:
                    message_parts.append(f"📸 {total_faces} face(s) detected in the image")
                
                if present_count > 0:
                    message_parts.append(f"👥 {present_count} student(s) marked as Present")
                
                if absent_count > 0:
                    message_parts.append(f"❌ {absent_count} student(s) marked as Absent")
                
                if unknown_count > 0:
                    message_parts.append(f"❓ {unknown_count} unknown person(s) detected")
                
                if error_count > 0:
                    message_parts.append(f"⚠️ {error_count} processing error(s) occurred")
                
                # Add processing details
                if processing_summary.get('warnings'):
                    for warning in processing_summary['warnings']:
                        message_parts.append(f"⚠️ {warning}")
                
                if processing_summary.get('errors'):
                    for error in processing_summary['errors']:
                        message_parts.append(f"❌ {error}")
                
                detailed_message = " | ".join(message_parts)
                print(f"DEBUG: Success message: {detailed_message}")
                
                # Save attendance to database
                date = datetime.now().strftime("%Y-%m-%d")
                print(f"DEBUG: Saving attendance for date: {date}")
                attendance_manager.save_attendance(date, attendance_results)
                
                flash(detailed_message, 'success')
                return redirect(url_for('report', date=date))
            else:
                print("DEBUG: No attendance results generated")
                # No results - provide helpful error message
                error_message = "❌ No attendance data generated. "
                
                # Check if it's a face detection issue
                if not face_system.known_face_encodings:
                    error_message += "No student database found. Please add student photos to the dataset folder."
                else:
                    error_message += "No faces detected in the image. Please ensure: 1) Good lighting, 2) Clear face views, 3) Image quality is sufficient."
                
                print(f"DEBUG: Error message: {error_message}")
                flash(error_message, 'error')
                return redirect(url_for('index'))
                
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file.', 'error')
        return redirect(url_for('index'))

@app.route('/report')
def report():
    """Display attendance report"""
    date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
    attendance_data = attendance_manager.get_attendance_by_date(date)
    
    if not attendance_data:
        flash('No attendance data found for this date.', 'info')
        return redirect(url_for('index'))
    
    return render_template('report.html', 
                         attendance_data=attendance_data, 
                         date=date,
                         total_students=len(attendance_data),
                         present_count=len([a for a in attendance_data if a['status'] == 'Present']))

@app.route('/download_csv/<date>')
def download_csv(date):
    """Download attendance report as CSV"""
    try:
        attendance_data = attendance_manager.get_attendance_by_date(date)
        if not attendance_data:
            flash('No attendance data found for this date.', 'error')
            return redirect(url_for('index'))
        
        csv_content = report_generator.generate_csv(attendance_data, date)
        
        # Create response with CSV content
        from io import StringIO
        output = StringIO()
        output.write(csv_content)
        output.seek(0)
        
        return send_file(
            StringIO(output.getvalue()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'attendance_{date}.csv'
        )
    except Exception as e:
        flash(f'Error downloading CSV: {str(e)}', 'error')
        return redirect(url_for('report', date=date))

@app.route('/history')
def history():
    """Show attendance history"""
    dates = attendance_manager.get_all_dates()
    return render_template('history.html', dates=dates)

@app.route('/view_date/<date>')
def view_date(date):
    """View attendance for a specific date"""
    return redirect(url_for('report', date=date))

@app.route('/test')
def test_system():
    """Test route to check if face recognition system is working"""
    try:
        # Check system status
        status = face_system.get_system_status()
        students = face_system.get_known_students()
        
        test_info = {
            'system_status': status,
            'known_students': students,
            'total_students': len(students),
            'encodings_loaded': len(face_system.known_face_encodings) > 0
        }
        
        return f"""
        <h2>System Test Results</h2>
        <p><strong>System Status:</strong> {test_info['system_status']}</p>
        <p><strong>Known Students:</strong> {test_info['known_students']}</p>
        <p><strong>Total Students:</strong> {test_info['total_students']}</p>
        <p><strong>Encodings Loaded:</strong> {test_info['encodings_loaded']}</p>
        <p><strong>Face Recognition System Ready:</strong> {'✅ Yes' if test_info['encodings_loaded'] else '❌ No'}</p>
        """
    except Exception as e:
        return f"<h2>System Test Failed</h2><p>Error: {str(e)}</p>"

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('attendance', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Initialize face recognition system
    face_system.initialize_system()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

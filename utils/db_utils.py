import pandas as pd
import os
import csv
from datetime import datetime
import logging

class AttendanceManager:
    def __init__(self):
        self.attendance_dir = 'attendance'
        self.attendance_file = os.path.join(self.attendance_dir, 'attendance.csv')
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Ensure attendance directory exists
        os.makedirs(self.attendance_dir, exist_ok=True)
        
        # Initialize attendance file if it doesn't exist
        self._initialize_attendance_file()
    
    def _initialize_attendance_file(self):
        """Initialize the attendance CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.attendance_file):
            try:
                with open(self.attendance_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Date', 'Student Name', 'Status', 'Confidence', 'Timestamp'])
                self.logger.info("Initialized new attendance file")
            except Exception as e:
                self.logger.error(f"Error initializing attendance file: {str(e)}")
    
    def save_attendance(self, date, attendance_results):
        """Save attendance results to CSV file"""
        try:
            # Prepare data for CSV
            rows_to_add = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for result in attendance_results:
                row = [
                    date,
                    result['name'],
                    result['status'],
                    result.get('confidence', 'N/A'),
                    timestamp
                ]
                rows_to_add.append(row)
            
            # Append to existing CSV file
            with open(self.attendance_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows_to_add)
            
            self.logger.info(f"Saved attendance for {date}: {len(rows_to_add)} records")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving attendance: {str(e)}")
            return False
    
    def get_attendance_by_date(self, date):
        """Get attendance data for a specific date"""
        try:
            if not os.path.exists(self.attendance_file):
                return []
            
            # Read CSV file
            df = pd.read_csv(self.attendance_file)
            
            # Filter by date
            date_data = df[df['Date'] == date]
            
            if date_data.empty:
                return []
            
            # Convert to list of dictionaries
            attendance_list = []
            for _, row in date_data.iterrows():
                attendance_list.append({
                    'name': row['Student Name'],
                    'status': row['Status'],
                    'confidence': row['Confidence'],
                    'timestamp': row['Timestamp']
                })
            
            # Sort by status (Present first, then Absent, then Unknown)
            attendance_list.sort(key=lambda x: ('Present', 'Absent', 'Unknown').index(x['status']))
            
            return attendance_list
            
        except Exception as e:
            self.logger.error(f"Error getting attendance for date {date}: {str(e)}")
            return []
    
    def get_all_dates(self):
        """Get all dates with attendance records"""
        try:
            if not os.path.exists(self.attendance_file):
                return []
            
            df = pd.read_csv(self.attendance_file)
            if df.empty:
                return []
            
            # Get unique dates and sort them
            dates = sorted(df['Date'].unique(), reverse=True)
            return dates
            
        except Exception as e:
            self.logger.error(f"Error getting all dates: {str(e)}")
            return []
    
    def get_student_attendance_history(self, student_name):
        """Get attendance history for a specific student"""
        try:
            if not os.path.exists(self.attendance_file):
                return []
            
            df = pd.read_csv(self.attendance_file)
            
            # Filter by student name
            student_data = df[df['Student Name'] == student_name]
            
            if student_data.empty:
                return []
            
            # Convert to list of dictionaries
            history = []
            for _, row in student_data.iterrows():
                history.append({
                    'date': row['Date'],
                    'status': row['Status'],
                    'confidence': row['Confidence'],
                    'timestamp': row['Timestamp']
                })
            
            # Sort by date (newest first)
            history.sort(key=lambda x: x['date'], reverse=True)
            
            return history
            
        except Exception as e:
            self.logger.error(f"Error getting attendance history for {student_name}: {str(e)}")
            return []
    
    def get_attendance_summary(self, start_date=None, end_date=None):
        """Get attendance summary for a date range"""
        try:
            if not os.path.exists(self.attendance_file):
                return {}
            
            df = pd.read_csv(self.attendance_file)
            
            if df.empty:
                return {}
            
            # Filter by date range if specified
            if start_date and end_date:
                df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
            elif start_date:
                df = df[df['Date'] >= start_date]
            elif end_date:
                df = df[df['Date'] <= end_date]
            
            if df.empty:
                return {}
            
            # Calculate summary statistics
            total_records = len(df)
            present_count = len(df[df['Status'] == 'Present'])
            absent_count = len(df[df['Status'] == 'Absent'])
            unknown_count = len(df[df['Status'] == 'Unknown'])
            
            # Get unique students
            unique_students = df['Student Name'].nunique()
            
            # Get attendance rate
            attendance_rate = (present_count / (present_count + absent_count)) * 100 if (present_count + absent_count) > 0 else 0
            
            summary = {
                'total_records': total_records,
                'unique_students': unique_students,
                'present_count': present_count,
                'absent_count': absent_count,
                'unknown_count': unknown_count,
                'attendance_rate': round(attendance_rate, 2),
                'date_range': {
                    'start': df['Date'].min() if not df.empty else None,
                    'end': df['Date'].max() if not df.empty else None
                }
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting attendance summary: {str(e)}")
            return {}
    
    def delete_attendance_date(self, date):
        """Delete attendance records for a specific date"""
        try:
            if not os.path.exists(self.attendance_file):
                return False
            
            # Read CSV file
            df = pd.read_csv(self.attendance_file)
            
            # Remove rows for the specified date
            df_filtered = df[df['Date'] != date]
            
            # Save back to file
            df_filtered.to_csv(self.attendance_file, index=False)
            
            deleted_count = len(df) - len(df_filtered)
            self.logger.info(f"Deleted {deleted_count} attendance records for {date}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting attendance for date {date}: {str(e)}")
            return False
    
    def export_attendance_data(self, output_file=None):
        """Export all attendance data to a new CSV file"""
        try:
            if not os.path.exists(self.attendance_file):
                return None
            
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(self.attendance_dir, f'attendance_export_{timestamp}.csv')
            
            # Copy attendance file
            import shutil
            shutil.copy2(self.attendance_file, output_file)
            
            self.logger.info(f"Exported attendance data to {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error exporting attendance data: {str(e)}")
            return None
    
    def get_system_stats(self):
        """Get system statistics"""
        try:
            if not os.path.exists(self.attendance_file):
                return {
                    'total_records': 0,
                    'total_dates': 0,
                    'total_students': 0,
                    'file_size': 0
                }
            
            df = pd.read_csv(self.attendance_file)
            
            stats = {
                'total_records': len(df),
                'total_dates': df['Date'].nunique() if not df.empty else 0,
                'total_students': df['Student Name'].nunique() if not df.empty else 0,
                'file_size': os.path.getsize(self.attendance_file)
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting system stats: {str(e)}")
            return {}

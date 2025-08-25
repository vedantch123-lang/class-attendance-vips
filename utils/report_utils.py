import pandas as pd
import csv
from datetime import datetime
import logging
from io import StringIO

class ReportGenerator:
    def __init__(self):
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def generate_csv(self, attendance_data, date):
        """Generate CSV content for attendance data"""
        try:
            # Create CSV content
            output = StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['Date', 'Student Name', 'Status', 'Confidence', 'Generated At'])
            
            # Write data rows
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for record in attendance_data:
                writer.writerow([
                    date,
                    record['name'],
                    record['status'],
                    record.get('confidence', 'N/A'),
                    timestamp
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            self.logger.info(f"Generated CSV report for {date} with {len(attendance_data)} records")
            return csv_content
            
        except Exception as e:
            self.logger.error(f"Error generating CSV: {str(e)}")
            return ""
    
    def generate_summary_report(self, attendance_data, date):
        """Generate a summary report of attendance data"""
        try:
            if not attendance_data:
                return {
                    'date': date,
                    'total_students': 0,
                    'present_count': 0,
                    'absent_count': 0,
                    'unknown_count': 0,
                    'attendance_rate': 0,
                    'summary': "No attendance data available"
                }
            
            # Calculate statistics
            total_students = len(attendance_data)
            present_count = len([r for r in attendance_data if r['status'] == 'Present'])
            absent_count = len([r for r in attendance_data if r['status'] == 'Absent'])
            unknown_count = len([r for r in attendance_data if r['status'] == 'Unknown'])
            
            # Calculate attendance rate
            attendance_rate = (present_count / (present_count + absent_count)) * 100 if (present_count + absent_count) > 0 else 0
            
            # Generate summary text
            summary_parts = []
            if present_count > 0:
                summary_parts.append(f"{present_count} students present")
            if absent_count > 0:
                summary_parts.append(f"{absent_count} students absent")
            if unknown_count > 0:
                summary_parts.append(f"{unknown_count} unknown persons detected")
            
            summary = f"Class attendance for {date}: {', '.join(summary_parts)}. "
            summary += f"Overall attendance rate: {attendance_rate:.1f}%"
            
            report = {
                'date': date,
                'total_students': total_students,
                'present_count': present_count,
                'absent_count': absent_count,
                'unknown_count': unknown_count,
                'attendance_rate': round(attendance_rate, 2),
                'summary': summary
            }
            
            self.logger.info(f"Generated summary report for {date}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")
            return {}
    
    def generate_detailed_report(self, attendance_data, date):
        """Generate a detailed report with individual student information"""
        try:
            if not attendance_data:
                return {
                    'date': date,
                    'summary': {},
                    'students': [],
                    'recommendations': []
                }
            
            # Get summary
            summary = self.generate_summary_report(attendance_data, date)
            
            # Organize students by status
            present_students = [r for r in attendance_data if r['status'] == 'Present']
            absent_students = [r for r in attendance_data if r['status'] == 'Absent']
            unknown_persons = [r for r in attendance_data if r['status'] == 'Unknown']
            
            # Generate recommendations
            recommendations = []
            if summary['attendance_rate'] < 80:
                recommendations.append("Low attendance rate detected. Consider following up with absent students.")
            if unknown_persons:
                recommendations.append(f"{len(unknown_persons)} unknown persons detected. Review class photo for unrecognized faces.")
            if absent_students:
                recommendations.append(f"Follow up with {len(absent_students)} absent students.")
            
            detailed_report = {
                'date': date,
                'summary': summary,
                'students': {
                    'present': present_students,
                    'absent': absent_students,
                    'unknown': unknown_persons
                },
                'recommendations': recommendations
            }
            
            self.logger.info(f"Generated detailed report for {date}")
            return detailed_report
            
        except Exception as e:
            self.logger.error(f"Error generating detailed report: {str(e)}")
            return {}
    
    def generate_attendance_chart_data(self, attendance_data):
        """Generate data for attendance charts"""
        try:
            if not attendance_data:
                return {}
            
            # Count by status
            status_counts = {}
            for record in attendance_data:
                status = record['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Prepare chart data
            chart_data = {
                'labels': list(status_counts.keys()),
                'data': list(status_counts.values()),
                'colors': ['#28a745', '#dc3545', '#ffc107']  # Green, Red, Yellow
            }
            
            return chart_data
            
        except Exception as e:
            self.logger.error(f"Error generating chart data: {str(e)}")
            return {}
    
    def format_attendance_for_display(self, attendance_data):
        """Format attendance data for HTML display"""
        try:
            if not attendance_data:
                return []
            
            formatted_data = []
            for record in attendance_data:
                # Add CSS classes for styling
                status_class = {
                    'Present': 'success',
                    'Absent': 'danger',
                    'Unknown': 'warning'
                }.get(record['status'], 'secondary')
                
                # Format confidence
                confidence = record.get('confidence', 'N/A')
                if confidence == 'High':
                    confidence_class = 'text-success'
                elif confidence == 'Low':
                    confidence_class = 'text-warning'
                else:
                    confidence_class = 'text-muted'
                
                formatted_record = {
                    'name': record['name'],
                    'status': record['status'],
                    'status_class': status_class,
                    'confidence': confidence,
                    'confidence_class': confidence_class,
                    'timestamp': record.get('timestamp', 'N/A')
                }
                
                formatted_data.append(formatted_record)
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"Error formatting attendance data: {str(e)}")
            return []
    
    def generate_export_filename(self, date, report_type='attendance'):
        """Generate filename for exported reports"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_{date}_{timestamp}.csv"
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating export filename: {str(e)}")
            return f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    def validate_attendance_data(self, attendance_data):
        """Validate attendance data structure"""
        try:
            if not isinstance(attendance_data, list):
                return False, "Attendance data must be a list"
            
            required_fields = ['name', 'status']
            for i, record in enumerate(attendance_data):
                if not isinstance(record, dict):
                    return False, f"Record {i} must be a dictionary"
                
                for field in required_fields:
                    if field not in record:
                        return False, f"Record {i} missing required field: {field}"
                
                # Validate status values
                valid_statuses = ['Present', 'Absent', 'Unknown']
                if record['status'] not in valid_statuses:
                    return False, f"Record {i} has invalid status: {record['status']}"
            
            return True, "Data validation successful"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"

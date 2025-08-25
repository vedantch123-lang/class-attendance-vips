import face_recognition
import cv2
import numpy as np
import os
import pickle
from PIL import Image
import logging

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encodings_file = 'models/encodings.pkl'
        self.dataset_path = 'dataset'
        self.tolerance = 0.6  # Face recognition tolerance
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def initialize_system(self):
        """Initialize the face recognition system by loading or creating encodings"""
        try:
            if os.path.exists(self.encodings_file):
                self.load_encodings()
                self.logger.info(f"Loaded {len(self.known_face_names)} known faces from encodings file")
            else:
                self.create_encodings()
                self.logger.info(f"Created encodings for {len(self.known_face_names)} known faces")
        except Exception as e:
            self.logger.error(f"Error initializing face recognition system: {str(e)}")
            # Create sample dataset if none exists
            self.create_sample_dataset()
            self.create_encodings()
    
    def create_sample_dataset(self):
        """Create a sample dataset with placeholder images if none exists"""
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path, exist_ok=True)
            
        # Create sample student data
        sample_students = [
            "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Eva Brown",
            "Frank Miller", "Grace Lee", "Henry Taylor", "Ivy Chen", "Jack Anderson",
            "Kate Martinez", "Liam O'Connor", "Maya Patel", "Noah Garcia", "Olivia Kim",
            "Paul Rodriguez", "Quinn Thompson", "Rachel White", "Sam Johnson", "Tina Davis",
            "Uma Singh", "Victor Lopez", "Wendy Clark", "Xavier Hall", "Yara Adams",
            "Zoe Baker", "Alex Turner", "Blake Foster", "Casey Reed", "Drew Cooper"
        ]
        
        # Create placeholder images (you should replace these with actual student photos)
        for i, name in enumerate(sample_students):
            # Create a simple colored rectangle as placeholder
            img = Image.new('RGB', (200, 200), color=(73, 109, 137))
            filename = f"{name.replace(' ', '_')}.jpg"
            filepath = os.path.join(self.dataset_path, filename)
            img.save(filepath)
            
        self.logger.info(f"Created sample dataset with {len(sample_students)} placeholder images")
    
    def create_encodings(self):
        """Create face encodings for all images in the dataset"""
        try:
            self.known_face_encodings = []
            self.known_face_names = []
            
            if not os.path.exists(self.dataset_path):
                self.logger.error("Dataset directory not found")
                return
            
            # Get all image files from dataset
            image_files = [f for f in os.listdir(self.dataset_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            
            if not image_files:
                self.logger.warning("No image files found in dataset directory")
                return
            
            for image_file in image_files:
                try:
                    # Extract student name from filename
                    student_name = image_file.rsplit('.', 1)[0].replace('_', ' ')
                    
                    # Load and encode the image
                    image_path = os.path.join(self.dataset_path, image_file)
                    image = face_recognition.load_image_file(image_path)
                    
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        # Use the first face found in the image
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_names.append(student_name)
                        self.logger.info(f"Encoded face for {student_name}")
                    else:
                        self.logger.warning(f"No face found in {image_file}")
                        
                except Exception as e:
                    self.logger.error(f"Error processing {image_file}: {str(e)}")
                    continue
            
            # Save encodings to file
            self.save_encodings()
            
        except Exception as e:
            self.logger.error(f"Error creating encodings: {str(e)}")
    
    def save_encodings(self):
        """Save face encodings to pickle file"""
        try:
            os.makedirs(os.path.dirname(self.encodings_file), exist_ok=True)
            
            encodings_data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(encodings_data, f)
                
            self.logger.info(f"Saved {len(self.known_face_names)} face encodings to {self.encodings_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving encodings: {str(e)}")
    
    def load_encodings(self):
        """Load face encodings from pickle file"""
        try:
            with open(self.encodings_file, 'rb') as f:
                encodings_data = pickle.load(f)
                
            self.known_face_encodings = encodings_data['encodings']
            self.known_face_names = encodings_data['names']
            
        except Exception as e:
            self.logger.error(f"Error loading encodings: {str(e)}")
            # If loading fails, create new encodings
            self.create_encodings()
    
    def process_class_photo(self, image_path):
        """Process a class photo and return attendance results with improved detection"""
        try:
            print(f"Loading image: {image_path}")
            # Load the image
            image = face_recognition.load_image_file(image_path)
            print("Image loaded successfully")
            
            # Find all faces in the image
            print("Detecting faces...")
            face_locations = face_recognition.face_locations(image, model="hog")  # Use HOG for better accuracy
            print(f"Found {len(face_locations)} faces")
            
            if not face_locations:
                print("No faces detected")
                return None
            
            # Generate face encodings with better parameters
            face_encodings = face_recognition.face_encodings(image, face_locations, num_jitters=3, model="small")
            print(f"Generated {len(face_encodings)} face encodings")
            
            # Check if we have any known students
            if not self.known_face_encodings:
                print("No known students in database")
                return None
            
            print(f"Comparing {len(face_encodings)} faces with {len(self.known_face_encodings)} known students")
            
            # Initialize attendance results
            attendance_results = []
            recognized_students = []
            processed_faces = []  # Track processed face locations to avoid duplicates
            
            # Process each detected face
            for i, face_encoding in enumerate(face_encodings):
                try:
                    # Check if this face location is too close to already processed faces
                    current_location = face_locations[i]
                    is_duplicate = False
                    
                    for processed_loc in processed_faces:
                        # Calculate distance between face centers
                        center1 = ((current_location[0] + current_location[2]) // 2, 
                                  (current_location[1] + current_location[3]) // 2)
                        center2 = ((processed_loc[0] + processed_loc[2]) // 2, 
                                  (processed_loc[1] + processed_loc[3]) // 2)
                        
                        distance = ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5
                        
                        # If faces are very close (within 50 pixels), consider it duplicate
                        if distance < 50:
                            is_duplicate = True
                            print(f"Face {i+1} appears to be duplicate, skipping...")
                            break
                    
                    if is_duplicate:
                        continue
                    
                    # Compare with known faces using stricter tolerance
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, 
                        face_encoding, 
                        tolerance=0.5  # Stricter tolerance for better accuracy
                    )
                    
                    if True in matches:
                        # Find the best match (lowest distance)
                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = face_distances.argmin()
                        confidence_score = 1 - face_distances[best_match_index]
                        
                        student_name = self.known_face_names[best_match_index]
                        
                        # Only accept if confidence is high enough
                        if confidence_score > 0.6:
                            status = "Present"
                            confidence = f"High ({confidence_score:.2f})"
                            recognized_students.append(student_name)
                            processed_faces.append(current_location)
                            print(f"Recognized: {student_name} with confidence {confidence_score:.2f}")
                        else:
                            status = "Unknown"
                            confidence = f"Low ({confidence_score:.2f})"
                            print(f"Low confidence match: {student_name} ({confidence_score:.2f})")
                    else:
                        # No match found
                        student_name = f"Unknown Person {i+1}"
                        status = "Unknown"
                        confidence = "Low"
                        print(f"Unknown face: {student_name}")
                    
                    attendance_results.append({
                        'name': student_name,
                        'status': status,
                        'confidence': confidence,
                        'face_location': current_location
                    })
                    
                except Exception as e:
                    print(f"Error processing face {i+1}: {str(e)}")
                    attendance_results.append({
                        'name': f"Error {i+1}",
                        'status': "Error",
                        'confidence': "N/A",
                        'face_location': face_locations[i]
                    })
            
            # Mark all known students as absent if not recognized
            for student_name in self.known_face_names:
                if student_name not in recognized_students:
                    attendance_results.append({
                        'name': student_name,
                        'status': 'Absent',
                        'confidence': 'N/A',
                        'face_location': None
                    })
                    print(f"Marked absent: {student_name}")
            
            # Sort results: Present first, then Absent, then Unknown, then Error
            attendance_results.sort(key=lambda x: ('Present', 'Absent', 'Unknown', 'Error').index(x['status']))
            
            print(f"Final results: {len(attendance_results)} records")
            return attendance_results
            
        except Exception as e:
            print(f"Major error in process_class_photo: {str(e)}")
            return None
    
    def get_known_students(self):
        """Get list of known students"""
        return self.known_face_names.copy()
    
    def get_system_status(self):
        """Get system status information"""
        return {
            'total_students': len(self.known_face_names),
            'encodings_loaded': len(self.known_face_encodings) > 0,
            'dataset_path': self.dataset_path,
            'encodings_file': self.encodings_file
        }

    def auto_reload_encodings(self):
        """Automatically reload encodings if new photos are detected"""
        try:
            if not os.path.exists(self.dataset_path):
                return False
            
            # Get current image files
            current_images = set([f for f in os.listdir(self.dataset_path) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])
            
            # Check if we have new images
            if hasattr(self, '_last_known_images'):
                if current_images != self._last_known_images:
                    print("New photos detected, reloading encodings...")
                    self.create_encodings()
                    self._last_known_images = current_images
                    return True
            else:
                self._last_known_images = current_images
            
            return False
        except Exception as e:
            print(f"Error in auto-reload: {str(e)}")
            return False
    
    def check_and_reload_encodings(self):
        """Check for new photos and reload if needed"""
        if self.auto_reload_encodings():
            print(f"Reloaded encodings for {len(self.known_face_names)} students")
            return True
        return False

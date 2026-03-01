import cv2
import numpy as np
import tensorflow as tf
import os
from pathlib import Path

class AnxietyDetector:
    def __init__(self, model_path="streamlit_app\anxiety_model.json", weights_path="streamlit_app\anxiety_model.h5"):
        """
        Initialize the Anxiety Detector with pre-trained model
        
        Paths are resolved in the following order:
        1. exact path as given
        2. relative to the current working directory
        3. relative to this module's directory (so packages can ship models)
        
        Parameters:
        -----------
        model_path : str
            Path to model JSON file
        weights_path : str
            Path to model weights HDF5 file
        """
        self.anxiety_dict = {0: "High_Anx", 1: "Low_Anx", 2: "No_Anx"}
        # resolve potential relative paths
        base_dir = Path(__file__).parent
        self.model = self._load_model(model_path, weights_path, base_dir)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def _load_model(self, model_path, weights_path, base_dir: Path):
        """Load model from JSON and weights from HDF5

        base_dir is the directory of this module; it's used to resolve paths
        when the caller uses a relative name but the files live alongside the
        package (e.g. streamlit_app/anxiety_model.json).
        """
        # helper to try candidate paths in order
        def candidates(path_str):
            p = Path(path_str)
            # direct
            yield p
            # cwd relative
            yield Path(os.getcwd()) / path_str
            # module directory (utils/)
            yield base_dir / path_str
            # parent of module (streamlit_app/)
            yield base_dir.parent / path_str
        
        try:
            # search for valid pair
            found = False
            for mp in candidates(model_path):
                for wp in candidates(weights_path):
                    if mp.exists() and wp.exists():
                        model_path_real = mp
                        weights_path_real = wp
                        found = True
                        break
                if found:
                    break
            if found:
                with open(model_path_real, 'r') as json_file:
                    loaded_model_json = json_file.read()
                model = tf.keras.models.model_from_json(
                    loaded_model_json,
                    custom_objects={
                        'Sequential': tf.keras.models.Sequential
                    }
                )
                model.load_weights(weights_path_real)
                print(f"✅ Model loaded from {model_path_real} and {weights_path_real}")
                return model

            # Fallback to model directory under base_dir
            model_dir = base_dir / "model"
            if model_dir.exists():
                model_json_path = model_dir / "streamlit_app/anxiety_model.json"
                model_h5_path = model_dir / "streamlit_app/anxiety_model.h5"
                if model_json_path.exists() and model_h5_path.exists():
                    with open(model_json_path, 'r') as json_file:
                        loaded_model_json = json_file.read()
                    model = tf.keras.models.model_from_json(
                        loaded_model_json,
                        custom_objects={
                            'Sequential': tf.keras.models.Sequential
                        }
                    )
                    model.load_weights(str(model_h5_path))
                    print(f"✅ Model loaded from {model_json_path} and {model_h5_path}")
                    return model

            raise FileNotFoundError(f"Model files not found at {model_path} or model/")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            raise
    
    def detect(self, frame):
        """
        Detect anxiety level in a frame
        
        Parameters:
        -----------
        frame : numpy.ndarray
            Input frame from webcam (BGR format)
        
        Returns:
        --------
        tuple : (anxiety_label, confidence)
            anxiety_label : str
                Predicted anxiety level
            confidence : float
                Confidence score (0-1)
        """
        try:
            # Resize frame for processing
            frame = cv2.resize(frame, (500, 500))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray_frame, 
                scaleFactor=1.3, 
                minNeighbors=5
            )
            
            if len(faces) == 0:
                return None, 0.0
            
            # Process first face detected
            (x, y, w, h) = faces[0]
            roi_gray = gray_frame[y:y+h, x:x+w]
            
            # Prepare image for model
            cropped_img = cv2.resize(roi_gray, (48, 48))
            cropped_img = np.expand_dims(np.expand_dims(cropped_img, -1), 0)
            cropped_img = cropped_img / 255.0  # Normalize
            
            # Predict anxiety
            prediction = self.model.predict(cropped_img, verbose=0)
            max_index = int(np.argmax(prediction))
            confidence = float(np.max(prediction))
            
            anxiety_label = self.anxiety_dict[max_index]
            
            return anxiety_label, confidence
        
        except Exception as e:
            print(f"❌ Error during detection: {str(e)}")
            return None, 0.0
    
    def detect_with_visualization(self, frame):
        """
        Detect anxiety and draw on frame
        
        Parameters:
        -----------
        frame : numpy.ndarray
            Input frame from webcam (BGR format)
        
        Returns:
        --------
        numpy.ndarray : Frame with detection drawn
        """
        try:
            original_frame = frame.copy()
            frame = cv2.resize(frame, (500, 500))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = self.face_cascade.detectMultiScale(
                gray_frame, 
                scaleFactor=1.3, 
                minNeighbors=5
            )
            
            for (x, y, w, h) in faces:
                # Draw rectangle
                cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 4)
                
                # Process region
                roi_gray = gray_frame[y:y+h, x:x+w]
                cropped_img = cv2.resize(roi_gray, (48, 48))
                cropped_img = np.expand_dims(np.expand_dims(cropped_img, -1), 0)
                cropped_img = cropped_img / 255.0
                
                # Predict
                prediction = self.model.predict(cropped_img, verbose=0)
                max_index = int(np.argmax(prediction))
                confidence = float(np.max(prediction))
                anxiety_label = self.anxiety_dict[max_index]
                
                # Draw text
                text = f"{anxiety_label} ({confidence:.2f})"
                cv2.putText(frame, text, (x+5, y-20), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_4)
            
            return frame
        
        except Exception as e:
            print(f"❌ Error during visualization: {str(e)}")
            return frame

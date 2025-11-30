try:
    import cv2
    import mediapipe as mp
    import numpy as np
    import math
except Exception as e:
    print("Error importing required packages:")
    print(" ", e)
    print("\nHint: this script expects the virtual environment at './hand_gesture_env' to be active or the dependencies installed there.")
    print("To run using the venv: \n  cd gesture && source hand_gesture_env/bin/activate && python index.py")
    print("Or run directly with the venv Python:\n  ./hand_gesture_env/bin/python index.py")
    print("To install dependencies into the venv (when activated):\n  pip install opencv-python mediapipe numpy")
    raise

class HandGestureDetector:
    def __init__(self):
        # Inisialisasi MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def calculate_distance(self, point1, point2):
        """Menghitung jarak antara dua titik"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_finger_up(self, landmarks, finger_tip_id, finger_pip_id):
        """Mengecek apakah jari terangkat"""
        return landmarks[finger_tip_id].y < landmarks[finger_pip_id].y
    
    def detect_gesture(self, landmarks):
        """Mendeteksi gestur berdasarkan landmark tangan"""
        # ID landmark untuk ujung jari
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        finger_pips = [3, 6, 10, 14, 18]  # PIP joints
        
        # Hitung jari yang terangkat
        fingers_up = []
        
        # Ibu jari (khusus karena orientasi berbeda)
        if landmarks[4].x > landmarks[3].x:  # Tangan kanan
            fingers_up.append(1)
        else:
            fingers_up.append(0)
            
        # Jari lainnya
        for i in range(1, 5):
            if self.is_finger_up(landmarks, finger_tips[i], finger_pips[i]):
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        total_fingers = sum(fingers_up)
        
        # Deteksi gestur
        # Peace (2 jari: telunjuk dan tengah)
        if total_fingers == 2 and fingers_up[1] == 1 and fingers_up[2] == 1:
            return "Peace ✌️"
        
        # Hi Five (5 jari terbuka)
        elif total_fingers == 5:
            return "Hi Five 🖐️"
        
        # Mengepal (0 jari terbuka)
        elif total_fingers == 0:
            return "Mengepal ✊"
        
        # Thumbs up
        elif total_fingers == 1 and fingers_up[0] == 1:
            return "Thumbs Up 👍"
        
        # OK gesture (ibu jari dan telunjuk membentuk lingkaran)
        elif total_fingers == 3 and fingers_up[0] == 1 and fingers_up[1] == 0:
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            distance = self.calculate_distance(thumb_tip, index_tip)
            if distance < 0.05:
                return "OK 👌"
        
        return f"Jari terbuka: {total_fingers}"
    
    def draw_landmarks(self, image, landmarks):
        """Menggambar landmark tangan dengan warna yang menarik"""
        h, w, c = image.shape
        
        # Warna untuk setiap jari
        colors = [
            (255, 0, 0),    # Ibu jari - Merah
            (0, 255, 0),    # Telunjuk - Hijau
            (0, 0, 255),    # Tengah - Biru
            (255, 255, 0),  # Manis - Kuning
            (255, 0, 255)   # Kelingking - Magenta
        ]
        
        # Grup landmark untuk setiap jari
        finger_groups = [
            [1, 2, 3, 4],           # Ibu jari
            [5, 6, 7, 8],           # Telunjuk
            [9, 10, 11, 12],        # Tengah
            [13, 14, 15, 16],       # Manis
            [17, 18, 19, 20]        # Kelingking
        ]
        
        # Gambar koneksi antar landmark
        connections = [
            [0, 1, 2, 3, 4],        # Ibu jari
            [0, 5, 6, 7, 8],        # Telunjuk
            [0, 9, 10, 11, 12],     # Tengah
            [0, 13, 14, 15, 16],    # Manis
            [0, 17, 18, 19, 20],    # Kelingking
            [5, 9, 13, 17]          # Koneksi horizontal
        ]
        
        # Gambar garis koneksi
        for connection in connections:
            for i in range(len(connection) - 1):
                start_idx = connection[i]
                end_idx = connection[i + 1]
                
                start_point = (int(landmarks[start_idx].x * w), 
                              int(landmarks[start_idx].y * h))
                end_point = (int(landmarks[end_idx].x * w), 
                            int(landmarks[end_idx].y * h))
                
                cv2.line(image, start_point, end_point, (255, 255, 255), 2)
        
        # Gambar landmark points
        for i, landmark in enumerate(landmarks):
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            # Tentukan warna berdasarkan jari
            color = (255, 255, 255)  # Default putih
            for finger_idx, group in enumerate(finger_groups):
                if i in group:
                    color = colors[finger_idx]
                    break
            
            # Gambar titik landmark
            cv2.circle(image, (x, y), 5, color, -1)
            cv2.circle(image, (x, y), 7, (0, 0, 0), 2)
            
    def add_info_panel(self, image, gesture, hand_count):
        """Menambahkan panel informasi"""
        h, w, c = image.shape
        
        # Background panel
        cv2.rectangle(image, (10, 10), (400, 100), (0, 0, 0), -1)
        cv2.rectangle(image, (10, 10), (400, 100), (255, 255, 255), 2)
        
        # Teks informasi
        cv2.putText(image, f"Jumlah Tangan: {hand_count}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(image, f"Gestur: {gesture}", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Instruksi
        instructions = "Tekan 'q' untuk keluar"
        cv2.putText(image, instructions, (20, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def main():
    # Inisialisasi kamera dan detector
    cap = cv2.VideoCapture(0)
    detector = HandGestureDetector()
    
    print("=== Hand Gesture Recognition ===")
    print("Gestur yang dapat dideteksi:")
    print("✌️  Peace: Angkat 2 jari (telunjuk + tengah)")
    print("✊  Mengepal: Kepalkan tangan")
    print("🖐️  Hi Five: Buka semua jari")
    print("👍 Thumbs Up: Angkat ibu jari")
    print("👌 OK: Bentuk lingkaran dengan ibu jari dan telunjuk")
    print("\nTekan 'q' untuk keluar")
    print("="*40)
    
    while True:
        success, image = cap.read()
        if not success:
            print("Gagal membaca dari kamera")
            break
        
        # Flip gambar untuk efek mirror
        image = cv2.flip(image, 1)
        h, w, c = image.shape
        
        # Konversi BGR ke RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = detector.hands.process(rgb_image)
        
        gesture = "Tidak ada tangan"
        hand_count = 0
        
        if results.multi_hand_landmarks:
            hand_count = len(results.multi_hand_landmarks)
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Deteksi gestur
                gesture = detector.detect_gesture(hand_landmarks.landmark)
                
                # Gambar landmark custom
                detector.draw_landmarks(image, hand_landmarks.landmark)
                
                # Gambar bounding box
                x_coords = [landmark.x for landmark in hand_landmarks.landmark]
                y_coords = [landmark.y for landmark in hand_landmarks.landmark]
                
                x_min, x_max = int(min(x_coords) * w), int(max(x_coords) * w)
                y_min, y_max = int(min(y_coords) * h), int(max(y_coords) * h)
                
                # Expand bounding box
                margin = 20
                x_min = max(0, x_min - margin)
                y_min = max(0, y_min - margin)
                x_max = min(w, x_max + margin)
                y_max = min(h, y_max + margin)
                
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        
        # Tambahkan panel informasi
        detector.add_info_panel(image, gesture, hand_count)
        
        # Tampilkan hasil
        cv2.imshow('Hand Gesture Recognition', image)
        
        # Keluar jika tombol 'q' ditekan
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
import cv2
import numpy as np

class VisionEnhancer:
    """
    JSM Safety Engine - Vision Enhancer Module
    Solves: 
    1. Weather Hazards (Fog/Rain dehazing)
    2. Dynamic Range Glare (Tunnel exit brightness transition)
    """
    def __init__(self):
        # Adaptive Histogram Equalization for contrast tuning
        self.clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

    def apply_hdr_dehaze(self, frame):
        """
        Enhances raw camera frames by removing glare and boosting road clarity.
        """
        if frame is None:
            return None

        # Step 1: Convert to LAB Color Space to isolate luminosity
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Step 2: Apply CLAHE on L-channel to normalize harsh highlights
        cl = self.clahe.apply(l_channel)
        merged_lab = cv2.merge((cl, a_channel, b_channel))
        enhanced_bgr = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)

        # Step 3: Gamma Correction to mitigate sudden sunlight blinding (Glare)
        gamma = 0.85
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        final_frame = cv2.LUT(enhanced_bgr, table)

        return final_frame

if __name__ == "__main__":
    # Quick Test Block
    enhancer = VisionEnhancer()
    dummy_input = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
    processed = enhancer.apply_hdr_dehaze(dummy_input)
    print("[SUCCESS] VisionEnhancer Module Ready. Output Shape:", processed.shape)
  

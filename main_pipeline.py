import numpy as np
import time

# Core modules import
from core.vision_enhancer import VisionEnhancer
from core.perception_filter import PerceptionFilter
from core.safety_guardrails import SafetyGuardrails

class JSMUnifiedSafetyLayer:
    """
    JSM Safety Engine - Main Integrated Pipeline
    Unifies Vision Enhancement, Perception Filtering, and Deterministic Guardrails.
    """
    def __init__(self):
        print("[INFO] Initializing JSM Tesla Safety Engine...")
        self.enhancer = VisionEnhancer()
        self.perception = PerceptionFilter()
        self.guardrails = SafetyGuardrails()

    def process_pipeline_frame(self, raw_frame, current_speed=40.0, driver_focused=True):
        """
        Executes full safety pipeline on each telemetry frame.
        """
        if raw_frame is None:
            return None, 0.0, 0.0, "FRAME_ERROR"

        # Step 1: Weather and Glare Correction
        enhanced_frame = self.enhancer.apply_hdr_dehaze(raw_frame)

        # Step 2: Critical Perception Analysis
        detections = self.perception.detect_critical_objects(enhanced_frame)

        # Step 3: Safety Guardrails Actuation Decision
        throttle, brake, status = self.guardrails.evaluate_controls(
            detections=detections,
            current_speed=current_speed,
            driver_focused=driver_focused
        )

        return enhanced_frame, throttle, brake, status

if __name__ == "__main__":
    pipeline = JSMUnifiedSafetyLayer()
    mock_frame = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
    
    frame_out, throttle_cmd, brake_cmd, sys_status = pipeline.process_pipeline_frame(
        raw_frame=mock_frame,
        current_speed=45.0,
        driver_focused=True
    )
    
    print("\n[PIPELINE TEST SUCCESSFUL]")
    print(f"-> Throttle Command: {throttle_cmd}")
    print(f"-> Brake Command: {brake_cmd}")
    print(f"-> System Status: {sys_status}")
  

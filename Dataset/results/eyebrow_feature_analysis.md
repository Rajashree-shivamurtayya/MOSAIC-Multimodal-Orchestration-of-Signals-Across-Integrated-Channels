# Eyebrow Feature Analysis
The naive features `naive_left_eyebrow_delta_camera_frame` and `naive_right_eyebrow_delta_camera_frame` are confirmed EXCLUDED from the model.
Normalized eyebrow geometry is preferable because raw camera-frame measurements are confounded by head pose changes (e.g. leaning back). Baseline-relative measurements normalize out physiological baseline differences.
Eyebrow features alone should not be interpreted as a lie detector, as they merely correlate with conversational emphasis and cognitive load.

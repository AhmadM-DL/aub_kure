from prometheus_client import Histogram, Gauge


speech_to_text_latency_ms = Gauge(
    'speech_to_text_latency_ms',
    'Most recent STT processing time in milliseconds'
)

suicide_detection_latency_ms = Gauge(
    'suicide_detection_latency_ms',
    'Most recent suicide detection time in ms'
)

mood_tracker_latency_ms = Gauge(
    'mood_tracker_latency_ms',
    'Most recent mood detection time in ms'
)


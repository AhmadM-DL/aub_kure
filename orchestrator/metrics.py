from prometheus_client import Summary

speech_to_text_time = Summary('speech_to_text_duration_ms', 'Time spent on speech-to-text')
suicide_detection_time = Summary('suicide_detection_duration_ms', 'Time spent on suicide check')
mood_tracker_time = Summary('mood_tracker_duration_ms', 'Time spent on mood check')

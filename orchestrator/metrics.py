from prometheus_client import Summary

transcription_time = Summary('transcription_duration_ms', 'Time spent on speech-to-text')
suicide_check_time = Summary('suicide_detection_duration_ms', 'Time spent on suicide check')
mood_detection_time = Summary('mood_detection_duration_ms', 'Time spent on mood check')

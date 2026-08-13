import speech_recognition as sr

def get_text_from_microphone():
    """Thu âm và chuyển giọng nói Tiếng Việt thành văn bản"""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Chờ người dùng nói (tối đa 5s), thu trong 10s
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            # Nhận diện tiếng Việt
            text = recognizer.recognize_google(audio, language="vi-VN")
            return text, None
    except sr.WaitTimeoutError:
        return None, "Không nghe thấy tiếng bạn nói."
    except sr.UnknownValueError:
        return None, "Không rõ lời nói, thử lại nhé."
    except sr.RequestError:
        return None, "Lỗi mạng (Cần Internet để nhận diện)."
    except Exception as e:
        return None, f"Lỗi mic: {str(e)}"
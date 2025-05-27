
from ai_core.learner import learn_sentence

def start_ai(vision_enabled, audio_enabled, chat_enabled):
    if vision_enabled:
        import cv2
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("BabyAI Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    if audio_enabled:
        print("Audio input started (TODO: Add speech recognition with confirmation)")

    if chat_enabled:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            learn_sentence(user_input)

if __name__ == "__main__":
    from gui.main_gui import run_gui
    run_gui()

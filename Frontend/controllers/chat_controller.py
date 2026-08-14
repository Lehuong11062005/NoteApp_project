from Frontend.services.chat_api import ChatAPI


class ChatController:

  def __init__(self):
    self.chat_api = ChatAPI()

  def ask_chatbot(self, user_id: str, message: str):
    if not message.strip():
      return False, "Vui lòng nhập câu hỏi."

    return self.chat_api.send_message(user_id, message)
#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import whisper


class WhisperNode(Node):
    def __init__(self, lang="en"):
        super().__init__("whisper")
        
        self.pub_text = self.create_publisher(String, "/whisper/text", 10)
        self.sub_path = self.create_subscription(String, "/mr_voice2/audio_path", self.callback_path, 10)
        
        self.lang = lang
        self.model = whisper.load_model("base")
        self.queue = []
        
    def callback_path(self, msg):
        audio_path = msg.data
        
        self.queue.append(audio_path)
        audio_path = self.queue.pop(0)
        print(audio_path, len(self.queue))
        
        res = self.model.transcribe(audio_path, language=self.lang, fp16=False)
        if len(res["text"]) > 0 and res["segments"][0]["no_speech_prob"] < 0.3:
            print(res)
            data = String()
            data.data = res["text"]
            self.pub_text.publish(data)


if __name__ == "__main__":
    rclpy.init()
    rclpy.spin(WhisperNode())
    

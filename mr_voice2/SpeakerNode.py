#/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import edge_tts
import asyncio
import os
from playsound3 import playsound
import threading


class SpeakerNode(Node):
    def __init__(self, voice="zh-HK-HiuMaanNeural", output_dir="/tmp/mr_voice2/"):
        super().__init__("speaker")
        self.sub_say = self.create_subscription(String, "/speaker/say", self.callback_say, 10)
        
        self.voice = voice
        self.output_dir = output_dir
        self.output_path = os.path.join(output_dir, "output.mp3")
        os.makedirs(output_dir, exist_ok=True)
        self.is_playing = False
        self.text = ""
        self.get_logger().info("Ready!")

    def callback_say(self, data):
        self.text = data.data
        print("Receive:", self.text)
        asyncio.run(self.say(self.text, self.voice, self.output_path))
        self.text = ""
        
        sound_thread = threading.Thread(target=self.play_sound, args=(self.output_path,))
        sound_thread.start()
        
    async def say(self, text, voice, output_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
    def play_sound(self, sound_path):
        self.is_playing = True
        print("Sound is playing...")
        sound = playsound(sound_path, block=False)
        while sound.is_alive():
            if self.text != "": 
                print(self.text)
                sound.stop()
                break
        print("Sound Stop!")
        self.is_playing = False
        
        
def main():
    rclpy.init()
    rclpy.spin(SpeakerNode())
    

if __name__ == "__main__":
    main()
    

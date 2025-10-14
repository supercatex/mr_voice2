#/usr/bin/python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String
import edge_tts
import asyncio
import os
from playsound3 import playsound
import threading

# Voice List
# https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
'''
en-US-AriaNeural        Female  Positive
en-US-AnaNeural         Female  Cute
en-US-GuyNeural         Male    Passion
en-US-SteffanNeural     Male    Rational
zh-HK-HiuGaaiNeural     Female  Friendly
zh-HK-WanLungNeural     Male    Friendly
zh-CN-YunxiNeural       Male    Lively
zh-CN-YunxiaNeural      Male    Cute
zh-CN-XiaoxiaoNeural    Female  Warm
zh-CN-liaoning-XiaobeiNeural
'''
class SpeakerNode(Node):
    def __init__(self):
        super().__init__("SpeakerNode")
        
        self.p = {
            "topic_name"    : "/speaker/say",
            "voice"         : "zh-HK-HiuMaanNeural",
            "output_dir"    : "/tmp/mr_voice2/",
            "output_file"   : "SpeakerNode.mp3",
            "is_playing"    : False
        }
        self.declare_parameters(
            namespace="",
            parameters=[(k, v) for k, v in self.p.items()]
        )
        for k, v in self.p.items():
            self.p[k] = self.get_parameter(k).value
        self.add_on_set_parameters_callback(self.callback_params)
        
        self.text = ""
        self.sub_say = self.create_subscription(String, self.p["topic_name"], self.callback_say, 10)
        
        os.makedirs(self.p["output_dir"], exist_ok=True)
        self.get_logger().info("Ready!")

    def callback_params(self, params):
        for param in params:
            self.p[param.name] = param.value
        return SetParametersResult(successful=True)
        
    def callback_say(self, data):
        self.text = data.data
        print("Receive:", self.text)
        self.output_path = os.path.join(self.p["output_dir"], self.p["output_file"])
        asyncio.run(self.say(self.text, self.p["voice"], self.output_path))
        self.text = ""
        
        sound_thread = threading.Thread(target=self.play_sound, args=(self.output_path,))
        sound_thread.start()
        
    async def say(self, text, voice, output_path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        
    def play_sound(self, sound_path):
        self.is_playing = Parameter("is_playing", Parameter.Type.BOOL, True)
        self.set_parameters([self.is_playing])
        print("Sound is playing...")
        
        sound = playsound(sound_path, block=False)
        while sound.is_alive():
            if self.text != "": 
                print(self.text)
                sound.stop()
                break
        
        self.is_playing = Parameter("is_playing", Parameter.Type.BOOL, False)
        self.set_parameters([self.is_playing])
        print("Sound Stop!")
        
def main():
    rclpy.init()
    rclpy.spin(SpeakerNode())
    

if __name__ == "__main__":
    main()
    

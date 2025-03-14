""" ROS RGB image publisher for DIGIT sensor """

import hydra
from cv_bridge import CvBridge
from pathlib import Path
import rospy
from sensor_msgs.msg import CompressedImage, Image
from digit_depth.digit.digit_sensor import DigitSensor

base_path = Path(__file__).parent.parent.parent.resolve()


class ImageFeature:
    def __init__(self):
        self.image_pub = rospy.Publisher("/digit/rgb/image_raw/compressed",
                                         CompressedImage, queue_size=10)
        self.image_raw_pub = rospy.Publisher("/digit/rgb/image_raw",
                                             Image, queue_size=10)
        self.br = CvBridge()

# @hydra.main(config_path=base_path / "config", config_name="digit.yaml")
def rgb_pub(cfg):
    digit_sensor = DigitSensor(cfg.sensor.fps, "QVGA", cfg.sensor.serial_num)
    ic = ImageFeature()
    # node_name = f"pub_rgb_digit_{cfg.sensor.serial_num}"
    # rospy.init_node(node_name, anonymous=True)
    digit_call = digit_sensor()
    br = CvBridge()
    while True:
        frame = digit_call.get_frame()
        # publish raw image
        msg = br.cv2_to_imgmsg(frame, "bgr8")
        msg.header.stamp = rospy.Time.now()
        ic.image_raw_pub.publish(msg)
        # publish compressed image
        # msg = br.cv2_to_compressed_imgmsg(frame, "png")
        # msg.header.stamp = rospy.Time.now()
        # ic.image_pub.publish(msg)
        # rospy.loginfo("Published image")


if __name__ == "__main__":
    rgb_pub()
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import Twist


class MonitorVelocidade(Node):
    def __init__(self):
        super().__init__('monitor_velocidade')
        perfil_qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.create_subscription(Twist, '/cmd_vel', self.processar_velocidade, perfil_qos)

    def processar_velocidade(self, mensagem):
        velocidade_linear = math.sqrt(mensagem.linear.x**2 + mensagem.linear.y**2 + mensagem.linear.z**2)
        sentido = 'horário' if mensagem.angular.z < 0 else 'anti-horário'
        self.get_logger().info(f'v={velocidade_linear:.2f} m/s, sentido={sentido}')


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(MonitorVelocidade())
    rclpy.shutdown()
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocidadePub(Node):
    def __init__(self):
        super().__init__('velocidade_pub')
        self.publicador = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_timer(0.5, self.publicar_velocidade)

    def publicar_velocidade(self):
        mensagem = Twist()
        mensagem.linear.x = 0.0
        mensagem.angular.z = 0.5
        self.publicador.publish(mensagem)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(VelocidadePub())
    rclpy.shutdown()
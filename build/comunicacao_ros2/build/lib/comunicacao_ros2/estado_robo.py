import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D, Twist
from std_msgs.msg import Float32, String


class EstadoRobo(Node):
    def __init__(self):
        super().__init__('estado_robo')
        self.publicador_pose = self.create_publisher(Pose2D, '/pose', 10)
        self.publicador_velocidade = self.create_publisher(Twist, '/velocidade', 10)
        self.publicador_bateria = self.create_publisher(Float32, '/bateria', 10)
        self.publicador_status = self.create_publisher(String, '/status', 10)
        self.posicao_x = 0.0
        self.nivel_bateria = 100.0
        self.create_timer(1.0, self.publicar_estado)
        self.get_logger().info('nó iniciado')

    def publicar_estado(self):
        self.posicao_x += 0.1
        pose = Pose2D()
        pose.x = self.posicao_x
        self.publicador_pose.publish(pose)

        velocidade = Twist()
        velocidade.linear.x = 0.3
        self.publicador_velocidade.publish(velocidade)

        self.nivel_bateria = max(0.0, self.nivel_bateria - 2.0)
        bateria = Float32()
        bateria.data = self.nivel_bateria
        self.publicador_bateria.publish(bateria)

        status = String()
        status.data = 'bateria_critica' if self.nivel_bateria < 20.0 else 'operando'
        self.publicador_status.publish(status)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(EstadoRobo())
    rclpy.shutdown()
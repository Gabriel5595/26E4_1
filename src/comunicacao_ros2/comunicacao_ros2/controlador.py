import threading

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_srvs.srv import SetBool


class Controlador(Node):
    def __init__(self):
        super().__init__('controlador')
        self.trava_estado = threading.Lock()
        self.estado = 'parado'
        self.servico_estado = self.create_service(SetBool, 'mudar_estado', self.tratar_mudanca_estado)
        self.assinante_bateria = self.create_subscription(Float32, '/bateria', self.tratar_bateria, 10)
        self.publicador_comando = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_timer(0.5, self.publicar_comando_velocidade)
        self.get_logger().info('nó iniciado')

    def tratar_mudanca_estado(self, requisicao, resposta):
        with self.trava_estado:
            if self.estado != 'emergencia':
                self.estado = 'movendo' if requisicao.data else 'parado'
            resposta.success = True
            resposta.message = f'Estado alterado para {self.estado}'
        self.get_logger().info(resposta.message)
        return resposta

    def tratar_bateria(self, mensagem):
        with self.trava_estado:
            if mensagem.data < 20.0 and self.estado != 'emergencia':
                self.estado = 'emergencia'
                self.get_logger().warn('BATERIA CRÍTICA: emergencia')

    def publicar_comando_velocidade(self):
        with self.trava_estado:
            estado_atual = self.estado
        comando = Twist()
        comando.linear.x = 0.5 if estado_atual == 'movendo' else 0.0
        self.publicador_comando.publish(comando)


def main(args=None):
    rclpy.init(args=args)
    no = Controlador()
    executor = MultiThreadedExecutor()
    executor.add_node(no)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        no.destroy_node()
        rclpy.shutdown()
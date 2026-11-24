import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import String
from std_srvs.srv import SetBool


class CoordenadorVigilancia(Node):
    def __init__(self):
        super().__init__('coordenador_vigilancia')
        self.alarme_ativo = False
        self.assinante_distancia = self.create_subscription(Range, '/distancia_frontal', self.tratar_distancia, 10)
        self.assinante_status = self.create_subscription(String, '/status_patrulha', self.tratar_status, 10)
        self.servico_alarme = self.create_service(SetBool, '/ligar_alarme', self.tratar_alarme)
        self.publicador_alertas = self.create_publisher(String, '/alertas', 10)
        self.get_logger().info('nó iniciado')

    def tratar_alarme(self, requisicao, resposta):
        self.alarme_ativo = requisicao.data
        resposta.success = True
        estado = 'ativado' if self.alarme_ativo else 'desativado'
        resposta.message = f'Alarme {estado}'
        return resposta

    def tratar_status(self, mensagem):
        self.get_logger().info(f'status_patrulha: {mensagem.data}')

    def tratar_distancia(self, mensagem):
        if mensagem.range < 0.5 and self.alarme_ativo:
            alerta = String()
            alerta.data = 'INTRUSO DETECTADO'
            self.publicador_alertas.publish(alerta)
            self.get_logger().warn(alerta.data)


def main(args=None):
    rclpy.init(args=args)
    no = CoordenadorVigilancia()
    executor = MultiThreadedExecutor()
    executor.add_node(no)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        no.destroy_node()
        rclpy.shutdown()
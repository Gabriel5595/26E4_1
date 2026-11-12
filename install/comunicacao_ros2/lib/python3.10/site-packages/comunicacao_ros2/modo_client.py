import sys
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ModoClient(Node):
    def __init__(self):
        super().__init__('modo_client')
        self.cliente = self.create_client(SetBool, 'modo')
        while not self.cliente.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('aguardando modo_server...')


def main(args=None):
    rclpy.init(args=args)
    cliente_modo = ModoClient()
    requisicao = SetBool.Request()
    requisicao.data = sys.argv[1].lower() == 'true'
    futuro = cliente_modo.cliente.call_async(requisicao)
    rclpy.spin_until_future_complete(cliente_modo, futuro)
    print(futuro.result().message)
    rclpy.shutdown()
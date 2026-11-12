import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class ModoServer(Node):
    def __init__(self):
        super().__init__('modo_server')
        self.create_service(SetBool, 'modo', self.tratar_requisicao)

    def tratar_requisicao(self, requisicao, resposta):
        if requisicao.data:
            resposta.message = 'Robô em modo autônomo ativado'
        else:
            resposta.message = 'Robô em modo manual ativado'
        resposta.success = True
        return resposta


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ModoServer())
    rclpy.shutdown()
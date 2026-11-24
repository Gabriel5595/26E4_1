import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class PatrulhaClient(Node):
    def __init__(self):
        super().__init__('patrulha_client')
        self.cliente_acao = ActionClient(self, Fibonacci, 'patrulha')

    def enviar_goal(self, total_pontos):
        self.total_pontos = total_pontos
        goal = Fibonacci.Goal()
        goal.order = total_pontos
        self.cliente_acao.wait_for_server()
        futuro = self.cliente_acao.send_goal_async(goal, feedback_callback=self.feedback_callback)
        futuro.add_done_callback(self.resposta_goal_callback)

    def resposta_goal_callback(self, futuro):
        goal_handle = futuro.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejeitado')
            return
        futuro_resultado = goal_handle.get_result_async()
        futuro_resultado.add_done_callback(self.resultado_callback)

    def feedback_callback(self, feedback_msg):
        visitados = len(feedback_msg.feedback.sequence)
        self.get_logger().info(f'Visitando ponto {visitados} de {self.total_pontos}')

    def resultado_callback(self, futuro):
        resultado = futuro.result().result
        self.get_logger().info(f'Resultado: {resultado.sequence}')


def main(args=None):
    rclpy.init(args=args)
    cliente = PatrulhaClient()
    cliente.enviar_goal(int(sys.argv[1]))
    rclpy.spin(cliente)
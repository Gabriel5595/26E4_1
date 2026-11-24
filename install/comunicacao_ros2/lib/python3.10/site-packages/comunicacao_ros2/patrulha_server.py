import time

import rclpy
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from example_interfaces.action import Fibonacci


class PatrulhaServer(Node):
    def __init__(self):
        super().__init__('patrulha_server')
        self.servidor_acao = ActionServer(self, Fibonacci, 'patrulha', self.execute_callback)
        self.get_logger().info('nó iniciado')

    def execute_callback(self, goal_handle):
        total_pontos = goal_handle.request.order
        feedback = Fibonacci.Feedback()
        feedback.sequence = []
        for ponto_atual in range(1, total_pontos + 1):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Fibonacci.Result()
            time.sleep(1.0)
            feedback.sequence.append(ponto_atual)
            self.get_logger().info(f'Visitando ponto {ponto_atual} de {total_pontos}')
            goal_handle.publish_feedback(feedback)
        goal_handle.succeed()
        resultado = Fibonacci.Result()
        resultado.sequence = feedback.sequence
        return resultado


def main(args=None):
    rclpy.init(args=args)
    no = PatrulhaServer()
    executor = MultiThreadedExecutor()
    executor.add_node(no)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        no.destroy_node()
        rclpy.shutdown()
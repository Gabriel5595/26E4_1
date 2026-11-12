import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gabrielcarvalho/Documents/INFNET/Fundamentos de Sistemas Robóticos com ROS2/Códigos/TPs/TP1/tp1_ws/install/comunicacao_ros2'

from setuptools import find_packages, setup

package_name = 'comunicacao_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gabrielcarvalho',
    maintainer_email='gabriel.vcarvalho@al.infnet.edu.br',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'velocidade_pub = '
            'comunicacao_ros2.velocidade_pub:main',
            'monitor_velocidade = '
            'comunicacao_ros2.monitor_velocidade:main',
        ],
    },
)

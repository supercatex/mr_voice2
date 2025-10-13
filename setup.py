from setuptools import find_packages, setup

package_name = 'mr_voice2'

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
    maintainer='pcms',
    maintainer_email='pcms@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'SpeakerNode = mr_voice2.SpeakerNode:main',
            'RespeakerNode = mr_voice2.RespeakerNode:main',
            'WhisperNode = mr_voice2.WhisperNode:main',
        ],
    },
)

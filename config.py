import os
__DIR__ = os.path.dirname(os.path.realpath(__file__))


c = {
    'max_threads': 256,
    'listen_ports': [
        25,
        465,
        587,

        53,

        80,
        8080,
        443,
    ],
    'max_thread_alive': 10,

    'log_file': __DIR__ + '/data/default.log',
    'report_file': __DIR__ + '/data/stats.txt',
}
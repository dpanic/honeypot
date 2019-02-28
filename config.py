import os
__DIR__ = os.path.dirname(os.path.realpath(__file__))


c = {
    'max_threads': 4096,
    'listen_port': 80,
    'max_thread_alive': 10,

    'log_file': __DIR__ + '/data/default.log',
    'report_file': __DIR__ + '/data/stats.txt',
    'report_file_raw': __DIR__ + '/data/stats_raw.txt',
}
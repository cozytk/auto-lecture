"""데이터 분석 패키지"""

from .reader import read_csv
from .statistics import compute_stats
from .outlier import detect_outliers
from .reporter import print_report, save_report

__all__ = ['read_csv', 'compute_stats', 'detect_outliers', 'print_report', 'save_report']

import os
try:
    from googlesearch import search
    import argparse
except ImportError:
    os.system("pip install google")
    os.system("pip install argparse")
    exit()
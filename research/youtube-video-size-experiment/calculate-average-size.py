import os
import math
from collections import Counter
# from scipy as sp

# Implement basic stat to avoid dependancies.

def mean(xs):
    return sum(xs)/len(xs)

def variance(xs, g=None):
    """
    E[X] = sum[i=1 to inf]{xi*pi}

    E[g(X)] = sum[i=1 to inf]{g(xi)*pi}
    """
    if g is None:
        g = lambda x: x

    n = len(xs)
    fs = Counter(xs) # Frequencies
    ps = {} # Probabilities
    for x,f in fs.items():
        ps[x] = float(f)/n

    return sum(map(lambda x: g(x)*ps[x], xs))

def std(x):
    return math.sqrt(variance(x))

def main():

    out_dir = "/tmp/youtube-video-size-experiment"

    videos = filter(os.path.isfile, map(lambda f: os.path.join(out_dir, f), os.listdir(out_dir)))
    video_sizes = map(os.path.getsize, videos) # bytes
    video_sizes = map(lambda s: s/(2**20), video_sizes) # MB

    print "count: %s" % len(video_sizes)
    print "min: %s" % min(video_sizes)
    print "max: %s" % max(video_sizes)
    # print "mean: %s" % sp.mean(video_sizes)
    print "mean: %s MB" % (sum(video_sizes)/len(video_sizes))
    # print "std. deviation: %s" % sp.std(video_sizes)
    print "std. deviation: %0.2f MB" % std(video_sizes)

if __name__ == "__main__":
    main()
#!/usr/bin/env python

import argparse
import itertools
import logging
import math
import os
import sys
import time

from PIL import Image
import vokram


def remix(paths, ngram_size, output_size):
    imgs = map(prep_image, paths)
    out_w, out_h = output_size

    tokens_iters = []
    for img in imgs:
        w, h = img.size
        tokens_iters.append(tokenize(w, h, img.load()))

    sentinal = 0
    tokens = itertools.chain.from_iterable(tokens_iters)
    model = vokram.build_model(tokens, ngram_size, sentinal)
    logging.info('%d images, model size: %d', len(paths), len(model))

    img = Image.new('RGB', output_size)
    target_pix = img.load()

    pix_stream = vokram.markov_chain(model)
    fill(out_w, out_h, target_pix, pix_stream)
    return img.crop((1, 1, out_w - 1, out_h - 1))


def prep_image(path):
    # reduce all input images to 256 colors, hoping for smaller and more
    # interesting Markov models
    return Image.open(path).quantize(colors=256).convert('RGB')


def fill(w, h, target_pix, color_stream):
    # pick the center of the circle, offset from the center of the image
    cx = int(w * .66)
    cy = h / 2

    # precalculate every coordinate in the output image, sorting by distance
    # from our chosen center
    sort = lambda (x, y), hypot=math.hypot: hypot(x - cx, y - cy)
    coords = precalculate_coords(w, h, sort=sort)

    # precalculate the colors we'll use at each coordinate, sorted by their
    # values
    colors = sorted(next(color_stream) for _ in xrange(w * h))

    # fill the output image in the order of our sorted coordinates, paired with
    # our sorted colors
    for (x, y), c in itertools.izip(coords, colors):
        target_pix[x, y] = c


def precalculate_coords(w, h, sort=None):
    x_range = xrange(0, w)
    y_range = xrange(0, h)
    coords = itertools.product(x_range, y_range)
    return sorted(coords, key=sort) if callable(sort) else coords


def tokenize(w, h, pix):
    """We tokenize an image such that there is a token for each pixel and each
    of its neighboring pixels, so that each neighbor is equally likely to occur
    after any given pixel.

    (And we ignore the outermost pixels for simplicity's sake.)
    """
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            for nx, ny in iter_neighbors(x, y):
                yield pix[x, y]
                yield pix[nx, ny]


def iter_neighbors(x, y):
    return [
        (x - 1, y),
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1),
    ]


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='markovangelo',
        description='Uses Markov chains to remix images.')
    arg_parser.add_argument(
        '-n', '--ngram-size', type=int, default=4)
    arg_parser.add_argument(
        '--width', type=int, required=True,
        help='Output image width')
    arg_parser.add_argument(
        '--height', type=int, required=True,
        help='Output image height')
    arg_parser.add_argument(
        '-o', '--output-dir',
        help='Optional output dir. If given, a path will be chosen for you.')
    arg_parser.add_argument(
        '--show', action='store_true', help='Open result in image viewer')
    arg_parser.add_argument(
        'source_file', nargs='+', help='Input image(s)')

    args = arg_parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    img = remix(args.source_file, args.ngram_size, (args.width, args.height))
    if args.show:
        img.show()
    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            os.makedirs(args.output_dir)
        filename = '%d.png' % time.time()
        outpath = os.path.join(args.output_dir, filename)
        logging.info(os.path.abspath(outpath))
        outfile = open(outpath, 'wb')
    else:
        outfile = sys.stdout
    img.save(outfile, 'png')

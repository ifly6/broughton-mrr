# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:15:14 2024
@author: ifly6
"""
import copy
import random
import re
import sys
import os

from glob import glob
from os import path
from subprocess import run

import pandas as pd
from PIL import Image


def split_path(f):
    _, extension = path.splitext(f)
    folder, basename = path.split(f)
    return folder, basename.removesuffix(extension), extension


def classify_image(f, fallback='pbm'):
    _, bn, _ = split_path(f)
    if any(bn.endswith(i) for i in ['cover', 'colour', 'color', 'cl']):
        return 'ppm'
    if any(bn.endswith(i) for i in
            ['grey', 'gray', 'greyscale', 'grayscale', 'gs']):
        return 'pgm'
    return fallback


def cut(size_string, by=0, factor=0.87):
    # ACTUAL = '150mm,233mm'
    sizes = [int(re.sub('mm$', '', i)) * factor - by for i 
             in size_string.split(',')]
    return ','.join(f'{int(i)}mm' for i in sizes)


def load_images(paths, return_path=False):  # pillow (PIL) leaks file handles!
    KEEP = []
    for file in paths:
        keep = copy.deepcopy(Image.open(file))
        KEEP.append(keep)
    return KEEP if return_path is False else zip(KEEP, paths)


if __name__ == '__main__':

    PREFIX = 'broughton1952'

    # assess distribution of paper widths
    if not path.exists(f'{PREFIX}_raw_fileaudit.xlsx'):
        _i = []
        for i, _path in load_images(
                sorted(glob(f'{PREFIX}_raw/*')), return_path=True
            ):
            _i.append({
                'image': split_path(_path)[1],
                'w': i.width, 'h': i.height, 'aspr': i.width / i.height})

        file_df = pd.DataFrame(_i).sort_values(by=['aspr'], ascending=False)
        file_df.to_csv(f'{PREFIX}_raw_fileaudit.csv', index=False)
        print('file audit created; review it')
        sys.exit(0)

    # set the paper size; measure this from actual!
    ACTUAL = '150mm,216mm'  # real 150mm,233mm
    OFFSET = '18mm'

    # run unpaper with various parameters mask the images
    os.makedirs(f'{PREFIX}_unpaper', exist_ok=True)
    for f in sorted(glob(f'{PREFIX}_raw/*')):

        # intermediate and new (ie final) types
        i_ext = '.' + classify_image(f, fallback='pgm')  # must be pgm or better
        n_ext = '.' + classify_image(f, fallback='pbm')  # final, bit data pls

        # get basename
        _, bn, _ = split_path(f)
        new_f = path.join(f'{PREFIX}_unpaper', bn + n_ext)
        if path.exists(new_f) or bn.endswith('skip'):
            continue

        print(f'unpapering file {bn}')

        # convert to ppm
        i_pth = bn + i_ext
        if not path.exists(i_pth):
            run(['magick', f, i_pth])
            print(f'converting {bn} to {i_ext}')

        # do unpaper
        run(
            [
                'unpaper', '--mask-scan-size', '250,100',
                '--black-threshold', '0.50',  # default: 0.33
                '--border-scan-threshold', '20',
                '--pre-border', '60,60,60,60',  # --pre-border left,top,right,bottom
                '--noisefilter-intensity', '10',
                '--deskew-scan-direction', 'left,bottom,top',
                '--deskew-scan-deviation', '2',
                '--border-scan-direction', 'v,h',  # must have to centre properly
                '--type', classify_image(f),  # change image type
            ]
            + [i_pth, new_f]
        )
        os.remove(i_pth)  # delete intermediate file

    print('cutting size to ' + cut(ACTUAL, factor=0.875))

    # for each image run unppaper on it with these parameters
    top = ['--border-align', 'top', '--border-margin', '13mm']
    btm = ['--border-align', 'bottom', '--border-margin', '11mm']
    lft = ['--border-align', 'left', '--border-margin', '13mm']
    special_params = {
        # 'image00001_cover':
        #     ['--no-noisefilter', '--no-blurfilter', '--no-grayfilter',
        #      '--no-border-scan', '--no-border', '--no-deskew'],
        # 'image00020': ['--mask-scan-size', '500,100'],
        'image00002': top + ['--deskew-scan-direction', 'top'],
        'image00003': ['--deskew-scan-direction', 'bottom'],
        'image00010': btm,
        'image00011': top,
        'image00012': btm + [
            '--mask-scan-size', '400,100', 
            '--deskew-scan-direction', 'right'],
        'image00014': btm,
        'image00139': ['--deskew-scan-direction', 'left,top'],
        'image00468': ['--deskew-scan-direction', 'left'],
        'image00475': top, 'image00478': btm,
        'image00510': top, 'image00513': btm,
        'image00537': top, 'image00538': btm,
        'image00549': top, 'image00550': btm,
        'image00574': top, 'image00575': btm,
        'image00628': ['--deskew-scan-direction', 'left'],
        'image00695': top, 'image00696': btm, 'image00698': top
    }

    # run unpaper to centre and clean up any remaining border gunk
    os.makedirs(f'{PREFIX}_unpaper2', exist_ok=True)
    for f in sorted(glob(f'{PREFIX}_unpaper/*')):
        _, bn, _ext = split_path(f)
        new_f = path.join(f'{PREFIX}_unpaper2', bn + _ext)
        if path.exists(new_f):
            continue

        print(f'unpaper2ing file {bn}')
        _c = (
            [
                'unpaper',
                '--sheet-size', cut(ACTUAL, factor=0.875),
                # place on uniform fake smaller paper
                # everything should be pre-centred so that this works well
                '--deskew-scan-direction', 'left,top',
                '--deskew-scan-deviation', '2',
                '--border-scan-direction', 'v,h',  # must have to centre properly
                # masks are automatically scanned with defaults
            ]
            + (special_params[bn] if bn in special_params else []) 
            + [f, new_f]
            + (['--overwrite'] if bn in special_params else [])
        )
        run(_c)

    # wrap output into a pdf
    images = load_images(sorted(glob(f'{PREFIX}_unpaper2/*')))
    images[0].save(
        f'{PREFIX}_unpaper.pdf', 'PDF', resolution=100.0, save_all=True,
        append_images=images[1:]
    )
    print('created pdf with size {:.2f} MB'.format(
        path.getsize(f'{PREFIX}_unpaper.pdf') / 1e6))

    # run ocr on the whole business
    run([
        'ocrmypdf', '--optimize', '3', '--jbig2-lossy', '-l', 'eng+grc+lat',
        '--output-type', 'pdf',
        f'{PREFIX}_unpaper.pdf', f'{PREFIX}_ocr.pdf'])

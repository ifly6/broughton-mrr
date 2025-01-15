#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue 14 Jan 2025 08:09:01
@author: ifly6
"""
import copy
import io
import lzma
import random
import re
import os
import shutil
import sys

from glob import glob
from os import path
from subprocess import run

import fitz
from PIL import Image


def split_path(f):
    _, extension = path.splitext(f)
    folder, basename = path.split(f)
    return folder, basename.rstrip(extension), extension


def classify_image(f, fallback='pbm'):
    _, bn, _ = split_path(f)
    if any(bn.endswith(i) for i in ['cover', 'colour', 'color', 'cl']):
        return 'ppm'
    if any(bn.endswith(i) for i in
            ['grey', 'gray', 'greyscale', 'grayscale', 'gs']):
        return 'pgm'
    return fallback


def load_images(paths):  # pillow (PIL) leaks file handles!
    KEEP = []
    for file in paths:
        keep = copy.deepcopy(Image.open(file))
        KEEP.append(keep)
    return KEEP


if __name__ == '__main__':

    REGEN = False
    PREFIX = 'broughton1960'

    # must wrap like this to read compressed file properly
    doc = fitz.open(
        stream=io.BytesIO(lzma.open(f'{PREFIX}_raw.pdf.xz', 'rb').read()),
        filetype='pdf')

    os.makedirs(f'{PREFIX}_raw', exist_ok=True)
    for i, page in enumerate(doc):
        _sp = path.join(f'{PREFIX}_raw', f'page_{i:03d}.pbm')
        if not path.exists(_sp) or REGEN is True:
            pix = page.get_pixmap(dpi=300)
            pix.save(_sp)
        if i % 10 == 0 or REGEN is True:
            print(f'saving page {i}')

    # delete these pages
    del_pp = '''
        page_001.pbm
        page_000.pbm
        page_102.pbm
        page_103.pbm
        page_104.pbm
        page_105.pbm
        page_106.pbm
        page_107.pbm
    '''.split('\n')
    for i in [i.strip() for i in del_pp if len(i.strip()) != 0]:
        _sp = path.join(f'{PREFIX}_raw', i)
        if path.exists(_sp):
            os.remove(_sp)

    # set the paper size
    ACTUAL = '156mm,215mm'  # measured actual is 156mm,225mm
    OFFSET = '20mm'  # measured actual is 14mm

    # for each image run unppaper on it with these parameters
    top = ['--border-align', 'top', '--border-margin', '15mm']
    btm = ['--border-align', 'bottom', '--border-margin', '15mm']
    lft = ['--border-align', 'left', '--border-margin', '20mm']
    special_params = {
        'page_002': ['--pre-border', '200,20,20,200'],
        'page_004': ['--deskew-scan-direction', 'bottom'],
        'page_006': btm,
        'page_007': top,
        'page_008': btm + ['--pre-border', '200,200,40,200'],
        'page_010': btm,
        'page_012': ['--pre-border', '200,20,40,250'],  # ltrb
        'page_015': ['--pre-border', '200,20,40,200'],
        'page_017': ['--pre-border', '200,20,40,200'],
        'page_019': ['--pre-border', '200,20,40,200'],
        'page_021': ['--pre-border', '200,20,40,200'],
        'page_028': ['--pre-border', '220,20,40,200'],
        'page_069': ['--pre-border', '220,20,120,200'],
        'page_074': ['--pre-border', '180,20,40,200'],
        'page_077': ['--deskew-scan-direction', 'left'],
        'page_080': top + ['--pre-border', '180,20,40,200'],
        'page_081': btm, 'page_083': top, 'page_084': btm, 'page_090': top,
        'page_091': btm, 'page_093': lft,
        'page_094': [
            '--mask-scan-size', '600,100',
            '--pre-border', '0,0,0,0', '--noisefilter-intensity', '0'],
        'page_095': lft + ['--deskew-scan-direction', 'top'],
        'page_098': top, 'page_101': top
    }

    # run unpaper with various parameters
    os.makedirs(f'{PREFIX}_unpaper', exist_ok=True)
    for f in sorted(glob(f'{PREFIX}_raw/*')):

        # get basename
        _, bn, _ = split_path(f)
        n_ext = '.' + classify_image(f, fallback='pbm')
        new_f = path.join(f'{PREFIX}_unpaper', bn + n_ext)
        if path.exists(new_f):
            continue

        print(f'unpapering file {bn}')
        run(
            [
                'unpaper',
                '--black-threshold', '0.4',  # default: 0.33
                '--border-scan-threshold', '20',
                '--pre-border', '80,20,20,200',  # --pre-border left,top,right,bottom
                '--noisefilter-intensity', '20',
                '--mask-scan-size', '200',
                '--deskew-scan-direction', 'left,bottom',
                '--deskew-scan-deviation', '2',
                '--border-scan-direction', 'v,h',
                '--sheet-size', ACTUAL,  # resize
                # get the right image type
                '--type', classify_image(f, fallback='pbm'),
            ]
            + (special_params[bn] if bn in special_params else [])
            + [f, new_f]
        )

    # wrap output into a pdf
    images = load_images(sorted(glob(f'{PREFIX}_unpaper/*')))
    images[0].save(
        f'{PREFIX}_unpaper.pdf', 'PDF', resolution=100.0, save_all=True,
        append_images=images[1:]
    )
    print('created pdf with size {:.2f} MB'.format(
        path.getsize(f'{PREFIX}_unpaper.pdf') / 1e6))

    # run ocr on the whole business
    run([
        'ocrmypdf', '--optimize', '3', '--jbig2-lossy', '-l', 'eng+grc',
        '--output-type', 'pdf',
        f'{PREFIX}_unpaper.pdf', f'{PREFIX}_ocr.pdf'])

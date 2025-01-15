# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:15:14 2024
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
    PREFIX = 'broughton1951'

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

    # remove these pages if present
    del_pp = '''page_005.pbm
    page_004.pbm
    page_003.pbm
    page_002.pbm
    page_001.pbm
    page_000.pbm
    page_561.pbm
    page_562.pbm
    page_632.pbm
    page_633.pbm
    page_634.pbm
    page_635.pbm
    page_636.pbm
    page_637.pbm'''.split('\n')
    for i in del_pp:
        _sp = path.join(f'{PREFIX}_raw', i.strip())
        if path.exists(_sp):
            os.remove(_sp)

    # # two pages are really bad
    # # -- turns out these pages are just repeats; delete them
    # run([
    #     'unpaper',
    #     '--layout', 'double', '--output-pages', '2', '--overwrite',
    #     '--pre-border', '10,10,10,10', '--deskew-scan-direction', 'top,bottom',
    #     'pp\ 512\,\ 513.pbm', 'output%03d.pbm'
    # ])
    # shutil.copy('output001.pbm', path.join(f'{PREFIX}_raw', 'page_561.pbm'))
    # shutil.copy('output002.pbm', path.join(f'{PREFIX}_raw', 'page_562.pbm'))

    # set the paper size
    # these are measured from actual
    ACTUAL = '156mm,225mm'  # measured actual is 156mm,225mm
    OFFSET = '20mm'  # measured actual is 14mm

    # for each image run unppaper on it with these parameters
    special_bm = {  # special border margins
        # 'IMG_2024_11_20_20_55_43_149_cover': '0mm',  # cover
        # 'IMG_2024_11_20_17_50_32_516L': '51mm',  # series intro
        # 'IMG_2024_11_20_17_50_32_516R': '54mm',  # title 1
        # 'IMG_2024_11_20_17_50_40_371R': '28mm',  # title 2
        # 'IMG_2024_11_20_17_50_48_088L': '52mm',  # verso
        # 'IMG_2024_11_20_17_50_48_088R': '52mm',  # dedication
        # 'IMG_2024_11_20_17_50_54_100R': '41mm',  # preface
        # 'IMG_2024_11_20_17_51_10_270R': '41mm',  # contents
        # 'IMG_2024_11_20_17_51_16_002R': '41mm',  # illustrations
        # 'IMG_2024_11_20_17_51_20_497R': '41mm',  # abbreviations
        # 'IMG_2024_11_20_17_51_25_585R': '32mm',  # ch 1
        # 'IMG_2024_11_20_17_51_56_666R': '30mm',  # ch 2
        # 'IMG_2024_11_20_17_53_27_550L': '20mm',  # figure
        # 'IMG_2024_11_20_17_53_47_942R': '30mm',  # ch 3
        # 'IMG_2024_11_20_18_00_31_923R': '32mm',  # ch 4
        # 'IMG_2024_11_20_18_02_32_640L': '34mm',  # ch 5
        # 'IMG_2024_11_20_18_05_30_786L': '34mm',  # ch 6
        # 'IMG_2024_11_20_18_08_24_345R': '32mm',  # ch 7
        # 'IMG_2024_11_20_18_10_29_110R': '32mm',  # ch 8
        # 'IMG_2024_11_20_18_12_32_037R': '40mm',  # sub idx
        # 'IMG_2024_11_20_18_12_47_410R': '42mm',  # lit idx
        # 'IMG_2024_11_20_18_12_55_025L': '15mm',
        # 'IMG_2024_11_20_18_12_55_025R': '15mm',
        # 'IMG_2024_11_20_18_13_03_411L': '15mm',
        # 'IMG_2024_11_20_18_13_03_411R': '15mm',
        # 'IMG_2024_11_20_18_13_10_534L': '15mm',
    }
    special_params = {
        # 'IMG_2024_11_20_20_55_43_149_cover':
        #     ['--no-noisefilter', '--no-blurfilter', '--no-grayfilter',
        #      '--no-border-scan', '--no-border', '--no-deskew'],
        'IMG_2024_11_20_21_05_37_128R': ['--mask-scan-size', '300'],
        # 'IMG_2024_11_19_21_28_47_669R': ['--mask-scan-threshold', '0.00001'],
        # 'IMG_2024_11_20_17_51_25_585L': ['--mask-scan-size', '100,100'],
        # 'IMG_2024_11_20_18_10_42_441R': 
        #     ['--blurfilter-size', '50,50', '--blurfilter-step', '25,25'],
        # 'IMG_2024_11_20_18_12_47_410R': 
        #     ['--no-mask-center'], # '--no-mask-scan', '--no-border-scan'],
        # 'IMG_2024_11_20_18_12_55_025L': 
        #     ['--no-mask-center', '--no-mask-scan', '--no-border-scan'],
        # 'IMG_2024_11_20_18_12_55_025R': 
        #     ['--mask-scan-threshold', '0.00001', '--mask-scan-size', '400,100',
        #      '--deskew-scan-size', '1100'],
        # 'IMG_2024_11_20_18_13_03_411L': 
        #     ['--no-mask-center', '--no-mask-scan', '--no-border-scan'],
        # 'IMG_2024_11_20_18_13_03_411R': 
        #     ['--no-mask-center', '--no-mask-scan', '--no-border-scan'],
        # 'IMG_2024_11_20_18_13_10_534L': 
        #     ['--no-mask-center', '--no-mask-scan', '--no-border-scan'],
        # 'IMG_2024_11_19_17_08_58_104R': ['--mask-scan-threshold', '0.0001'],
        # 'IMG_2024_11_19_17_02_59_184L': ['--border-scan-threshold', '10'],
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
                '--dpi', '300',
                '--black-threshold', '0.4',  # default: 0.33
                '--pre-border', '80,10,10,200',  # --pre-border left,top,right,bottom
                # '--blurfilter-size', '50,50',
                '-noisefilter-intensity', '20',
                '--mask-scan-size', '200',
                '--deskew-scan-direction', 'left,bottom,top',
                '--deskew-scan-deviation', '2',
                '--border-scan-direction', 'v,h',
                '--border-align', 'top',  # put to top
                '--border-margin', special_bm[bn] if bn in special_bm else OFFSET,
                '--stretch', ACTUAL,
                '--post-size', ACTUAL,  # resize
                '--type', classify_image(f, fallback='pbm'),  # get the right image type
            ] + (special_params[bn] if bn in special_params else [])
            # + (['--no-grayfilter'] if classify_image(f, fallback='pgm') == 'pgm' else [])
            #+ (['--overwrite'] if bn in special_bm.keys() else [])
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
        'ocrmypdf', '--optimize', '3', '--jbig2-lossy', '-l', 'eng+lat+grc',
        '--output-type', 'pdf',
        f'{PREFIX}_unpaper.pdf', f'{PREFIX}_ocr.pdf'])

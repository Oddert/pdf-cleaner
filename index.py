import fitz
import re

from typing import List

from pypdf import PdfReader

from join_test import filter_invalid_words, re_process_block_text

from spellchecker import SpellChecker

spell = SpellChecker()

reader = PdfReader('DeLanda_Manuel_A_Thousand_Years_of_Nonlinear_History.pdf')

print(len(reader.pages))

page = reader.pages[11]

print(page.extract_text())
# print(page.extract_text(extraction_mode='layout'))

# print('     ')
# print('==============')
# print('     ')

# page = reader.pages[20]

# print(page.extract_text())

# for x in range(0, 50):
#     print('Page ========> ', x)
#     txt = reader.pages[x].extract_text(extraction_mode='layout')
#     srch = re.search(pattern='Iberall', string=txt)
#     if srch:
#         print(txt)
#         break


doc = fitz.open('DeLanda_Manuel_A_Thousand_Years_of_Nonlinear_History.pdf')
page = doc[11]
raw = page.get_text('rawdict')

# all_blocks = []


def process_text(threshold_distance: float | int = 2):
    all_blocks: List[str] = []
    for block in raw['blocks']:
        for line in block.get('lines', []):
            chars = [char for span in line['spans'] for char in span['chars']]
            chars.sort(key=lambda char: char['bbox'][0])
            blocks = [
                (char['c'], round(char['bbox'][0], 1), round(char['bbox'][2], 1))
                for char in chars
            ]
            # print(''.join(char['c'] for char in chars))
            # print(blocks)
            line_result = ' '.join(
                re_process_block_text(
                    filter_invalid_words(blocks), threshold_distance=threshold_distance
                )
            )
            # print(blocks)
            all_blocks.append(line_result)
    return ' '.join(all_blocks)


ranges: List[float] = [2.0, 1.0]

for value in ranges:
    chunk = process_text(value)
    print(chunk)
    # print(spell.unknown(chunk.split(' ')))
    print('### Invalid Words: ', len(spell.unknown(chunk.split(' '))))
    print('               ')
    print('==================================')
    print('               ')

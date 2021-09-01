# Your imports go here
import logging
import os
import re
import json

logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def extract_amount(dirpath: str) -> float:

    logger.info('extract_amount called for dir %s', dirpath)
    # Your logic goes here.
    word_list = ['total', 'amount', 'credit', 'payment', 'debit']
    def has_numbers(inputString):
        return bool(re.search(r'\d', inputString))
    with open(os.path.join(dirpath, 'ocr.json'), 'r', encoding="utf8") as f:
        json_file = json.load(f)
    blocks = json_file['Blocks']
    res = ''
    cand_res = []
    for i, _ in enumerate(blocks):
        if blocks[i]['BlockType'] == 'LINE' and any(w in blocks[i]['Text'].lower() for w in word_list):
            if has_numbers(blocks[i]['Text'].lower()):
                res = [blocks[i]['Text'].lower() for c in word_list if c in blocks[i]['Text'].lower()][0]
                break
            for j in range(i, i+2):
                if blocks[j]['BlockType'] == 'LINE' and has_numbers(blocks[j]['Text'].lower()):
                    res = blocks[j]['Text'].lower()
                    break
        if blocks[i]['BlockType'] == 'LINE' and has_numbers(blocks[i]['Text'].lower()):
            cand_res.append(blocks[i]['Text'].lower())
    if res == '':
        for k in cand_res:
            if any('$' in t for t in cand_res):
                res = [a for a in cand_res if '$' in a][0]
            else:
                try:
                    res = str(float(k))
                    break
                except ValueError:
                    pass
    res = re.sub(r",", "", res)
    res = float(re.findall(r"\d+\.\d+", res)[0])
    return res

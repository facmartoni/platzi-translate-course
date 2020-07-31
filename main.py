from googletrans import Translator
import re
import os

# Files paths
VTT_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'vtt_files')
SRT_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'srt_files')
INPUT_FILES = os.listdir(VTT_PATH)

# Regex
MINUTE_LINE = re.compile(r'^\d.*$')
MINUTE = re.compile(r'([\d\.:]+) --> ([\d\.:]+)')
TEXT_LINE = re.compile(r'^\w.*$')


def translate_text_list(text_list):
    condensed_str = ' (1) '.join(text_list)
    translator = Translator()
    translated_text = translator.translate(
        condensed_str, src='en', dest='es').text
    translated_text_list = translated_text.split('(1)')
    translated_text_list = [string.strip() for string in translated_text_list]
    return translated_text_list


def vttmin_to_srtmin(minute_list):
    srt_minute_list = []
    for line in minute_list:
        minutes = re.match(MINUTE, line)
        start_minute = '00:' + minutes.group(1).replace('.', ',')
        final_minute = '00:' + minutes.group(2).replace('.', ',')
        srt_line = start_minute + ' --> ' + final_minute
        srt_minute_list.append(srt_line)
    return srt_minute_list


def write_srt_file(output_file, minute_list, text_list):
    with open(os.path.join(SRT_PATH, output_file), 'w', encoding='utf-8') as srt:
        for i in range(len(minute_list)):
            srt.write(f'{i + 1}')
            srt.write('\n')
            srt.write(minute_list[i])
            srt.write('\n')
            srt.write(text_list[i])
            srt.write('\n')
            if i != len(minute_list) - 1:
                srt.write('\n')
    print(f'Archivo {output_file} escrito satisfactoriamente ;)')


def run():
    for input_file in INPUT_FILES:

        minute_list = []
        text_list = []

        with open(os.path.join(VTT_PATH, input_file), 'r', encoding='utf-8') as vtt:
            for line in vtt:
                if line.strip() == "WEBVTT":
                    continue
                elif re.match(MINUTE_LINE, line):
                    minute_list.append(line.strip())
                elif re.match(TEXT_LINE, line):
                    text_list.append(line.strip())

        translated_text_list = translate_text_list(text_list)
        srt_minute_list = vttmin_to_srtmin(minute_list)

        # print(len(translated_text_list))
        # print(len(srt_minute_list))

        output_file_en = re.match(r'\w+', input_file).group(0) + '_en.srt'
        output_file_es = re.match(r'\w+', input_file).group(0) + '_es.srt'

        write_srt_file(output_file_en, srt_minute_list, text_list)
        write_srt_file(output_file_es, srt_minute_list, translated_text_list)


if __name__ == '__main__':
    run()

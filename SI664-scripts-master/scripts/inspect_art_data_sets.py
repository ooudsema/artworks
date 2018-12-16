import chardet
import logging
import os
import pandas as pd
import sys as sys


def main(argv=None):
    source_in = os.path.join('input', 'csv', 'artworksjson.csv')
    encoding = find_encoding(source_in)

    source = read_csv(source_in, encoding, ',')
    source_trimmed = trim_columns(source)

    subject = extract_filtered_series(source_trimmed, ['subject'])
    subject['subject'] = subject['subject'].str.split(',', n=-1, expand=False)
    subject_split = subject['subject'].apply(pd.Series)\
        .reset_index()\
        .melt(id_vars=['index'], value_name='subject')\
        .dropna(axis=0, how='any')[['index', 'subject']]\
        .drop_duplicates(subset=['subject'])\
        .set_index('index')\
        .sort_values(by=['subject'])

    subject_out = os.path.join('output', 'subjects_unique.csv')
    write_series_to_csv(subject_split, subject_out, ',', False)
    #logging.info(msg[7].format(os.path.abspath(genres_out)))


    art_subjects = source_trimmed[['accession', 'subject']]\
        .dropna(axis=0, subset=['subject']) \
        .drop_duplicates(subset=['accession', 'subject']) \
        .sort_values(by=['accession', 'subject'])
    art_subjects['accession'] = art_subjects['accession'].astype(str)
    art_subjects['subject'] = art_subjects['subject'].str.split(',', n=-1, expand=False)
    art_subjects_split = art_subjects.subject.apply(pd.Series)\
        .merge(art_subjects, left_index=True, right_index=True)\
        .drop(['subject'], axis=1)\
        .melt(id_vars=['accession'], value_name='subject')\
        .drop('variable', axis=1) \
        .dropna(axis=0, subset=['subject']) \
        .drop_duplicates(subset=['accession', 'subject'])\
        .sort_values(by=['accession', 'subject'])
    art_subjects_out = os.path.join('output', 'artwork_subjects.csv')
    write_series_to_csv(art_subjects_split, art_subjects_out, ',', False)









def extract_filtered_series(data_frame, column_list, drop_rule='all'):
    """
    Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
    Duplicate values and NaN or blank values are dropped from the result set which is
    returned sorted (ascending).
    :param data_frame: Pandas DataFrame
    :param column_list: list of columns
    :param drop_rule: dropna rule
    :return: Panda Series one-dimensional ndarray
    """

    return data_frame[column_list].drop_duplicates().dropna(axis=0, how=drop_rule).sort_values(
        column_list)
    # return data_frame[column_list].str.strip().drop_duplicates().dropna().sort_values()


def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc


def read_csv(path, encoding, delimiter=','):
    """
    Utilize Pandas to read in *.csv file.
    :param path: file path
    :param delimiter: field delimiter
    :return: Pandas DataFrame
    """

    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x96 in position 450: invalid start byte
    # return pd.read_csv(path, sep=delimiter, encoding='utf-8', engine='python')

    return pd.read_csv(path, sep=delimiter, encoding=encoding, engine='python')
    # return pd.read_csv(path, sep=delimiter, engine='python')


def trim_columns(data_frame):
    """
    :param data_frame:
    :return: trimmed data frame
    """

    trim = lambda x: x.strip() if type(x) is str else x
    return data_frame.applymap(trim)


def write_series_to_csv(series, path, delimiter=',', row_name=True):
    """
    Write Pandas DataFrame to a *.csv file.
    :param series: Pandas one dimensional ndarray
    :param path: file path
    :param delimiter: field delimiter
    :param row_name: include row name boolean
    """

    series.to_csv(path, sep=delimiter, index=row_name)


if __name__ == '__main__':
    sys.exit(main())
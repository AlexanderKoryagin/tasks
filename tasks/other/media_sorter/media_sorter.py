# -*- coding: utf-8 -*-
"""Small media sorter (For Windows only).

Will sort files according EXIF creation date and copy files to new directories
like this:
    2016
        01_january
            2017-01-01_12-00-00.jpg
            2017-01-02_12-10-00.jpg
        02_february
            2017-02-01_12-00-00.jpg
            2017-02-02_12-10-00.jpg
    2017
        01_january
            2017-01-01_12-00-00.jpg
            2017-01-02_12-10-00.jpg
        02_february
            2017-02-01_12-00-00.jpg
            2017-02-02_12-10-00.mp4
"""
from collections import namedtuple
import filecmp
import json
import os
import shutil
import subprocess


# START_DIR = 'd:/Dropbox/Camera Uploads'  # from where to take files
# START_DIR = 'd:/YandexDisk/Photos/_foto2'  # from where to take files
START_DIR = 'd:/YandexDisk/Photos/_foto0'  # from where to take files
# START_DIR = 'd:/YandexDisk/Photos/_foto2/2_2011 papa DR'  # from where to take files
# START_DIR = 'd:/YandexDisk/Photos/__SORT ME Raya'  # from where to take files
# START_DIR = 'd:/YandexDisk/Photos/foto_2011'  # from where to take files
# START_DIR = 'd:/YandexDisk/Photos/_foto2/30_2014_mart moskva'  # from where to take files

DESTINATION_DIR = 'd:/_time_sorted'      # where to put sorted files
EXTENSIONS = ['jpg', 'mp4', 'mov']       # search only these files


class SorterHelpers(object):
    """Helpers for Sorter."""

    MONTHS = {
        '00': 'WRONG',
        '01': 'january',
        '02': 'february',
        '03': 'march',
        '04': 'april',
        '05': 'may',
        '06': 'june',
        '07': 'july',
        '08': 'august',
        '09': 'september',
        '10': 'october',
        '11': 'november',
        '12': 'december'
    }

    @staticmethod
    def get_files_with_date():
        """Find all files, get time and convert result to jSON.

        :return:
            list if dictionaries.
            Like:
                [
                {u'CreateDate': u'2016:04:15 19:53:23',  # May present or not
                 u'ModifyDate': u'2016:04:15 19:53:23',  # May present or not
                 u'SourceFile': u'd:/dirname/dirname/2016-04-15 19.53.23.jpg'},
                 ...
                 ]
         :raise:
            ValueError: If start folder is not exist.
                        If no files were found in start dir.
        """
        if not os.path.exists(START_DIR):
            raise ValueError('No such directory: %s' % START_DIR)

        # http://www.sno.phy.queensu.ca/~phil/exiftool/exiftool_pod.html
        cmd = (
            '{root_dir}/'
            'exiftool/exiftool.exe '
            '-quiet -recurse "{media_dir}" '
            '-ignore "{ignore}" '
            '-DateTimeOriginal -CreateDate '
            '-json'.format(
                root_dir=os.path.dirname(os.path.realpath(__file__)),
                ignore='ignore_me_dir',  # TODO: Add ignore
                media_dir=START_DIR))
        # Add required extensions
        for ext in EXTENSIONS:
            cmd += ' -ext %s' % ext
        print cmd

        # Run tool
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        files_raw = proc.stdout.read().strip()
        proc.kill()
        if files_raw:
            files = json.loads(files_raw)
            return files
        else:
            raise ValueError('No files were found in %s' % START_DIR)

    @staticmethod
    def get_date(one_file_dict):
        """Get date from generated dictionary.

        :param one_file_dict:
        :return:
        """
        exif_date_dto = one_file_dict.get('DateTimeOriginal', None)
        exif_date_cd = one_file_dict.get('CreateDate', None)

        exif_date = None
        for date in (exif_date_dto, exif_date_cd):
            if date and '0000' not in str(date):
                exif_date = date

        return exif_date

    def parse_date(self, date_time):
        """Parse provided date_time and convert in to named tuple.

        :param date_time: string like '2017:01:21 12:15:45'
        :return: named tuple
        """
        # pylint: disable=invalid-name
        date, time = date_time.split()
        _year = date.split(':')[0]
        _month_num = date.split(':')[1]
        _month_txt = '{0}_{1}'.format(_month_num, self.MONTHS[_month_num])
        _date = date.split(':')[2]
        _hours = time.split(':')[0]
        _minutes = time.split(':')[1]
        _seconds = time.split(':')[2]

        Date = namedtuple(
            'Date',
            ['year', 'month_num', 'month_txt', 'date', 'h', 'm', 's'])
        nt_date = Date(
            year=_year,
            month_num=_month_num,
            month_txt=_month_txt,
            date=_date,
            h=_hours,
            m=_minutes,
            s=_seconds)
        return nt_date

    @staticmethod
    def parse_file_path(file_path):
        """Parse and convert str filename to namedtuple.

        :param file_path: full path to file
        :return: named tuple
        """
        # pylint: disable=invalid-name
        _dir = os.path.split(file_path)[0]     # /home/alex/dir/dir
        _name = os.path.split(file_path)[1]    # 2013-10-04 11:21:39.jpg
        _name = os.path.splitext(_name)[0]     # 2013-10-04 11:21:39
        _ext = os.path.splitext(file_path)[1]  # .jpg

        File = namedtuple('File', ['dir', 'name', 'ext', 'f_path'])
        nt_file = File(
            dir=_dir,
            name=_name,
            ext=_ext,
            f_path=file_path)
        return nt_file

    @staticmethod
    def format_filename_from_data(date):
        """Prepare and convert date.

        :param date: named tuple date
        :return: string formatted like: 2016-12-10_17-57-35
        """
        file_name = '{Y}-{M}-{D}_{h}-{m}-{s}'.format(
            Y=date.year,
            M=date.month_num,
            D=date.date,
            h=date.h,
            m=date.m,
            s=date.s)
        return file_name

    @staticmethod
    def is_the_same_file(file1, file2):
        """Check if file1 is the same as file2.

        :param file1: full path to file1
        :param file2: full path to file1
        :return: True if same file
                 False if files are different
        """
        return filecmp.cmp(file1, file2)

    def change_filename_if_exists(self, orig_f_path, future_f_path):
        """change filename if both files has the same time."""
        nt_future_f_path = self.parse_file_path(future_f_path)
        i = 0
        while os.path.isfile(future_f_path):
            if self.is_the_same_file(orig_f_path, future_f_path):
                os.remove(future_f_path)
            else:
                i += 1
                future_f_path = '{dir}/{name}-{counter}{ext}'.format(
                    dir=nt_future_f_path.dir,
                    name=nt_future_f_path.name,
                    counter=i,
                    ext=nt_future_f_path.ext)
        return future_f_path


class Sorter(SorterHelpers):
    """Sorting tool mail logic."""

    def run(self):
        """Run media sorter."""
        files = self.get_files_with_date()

        for one_file in files:
            exif_date = self.get_date(one_file)

            orig_f_path = one_file.get('SourceFile', None)
            print('\n{0}'.format(orig_f_path))

            if exif_date:

                date = self.parse_date(exif_date)
                future_dir = '{dir}/{year}/{month}'.format(
                    dir=DESTINATION_DIR,
                    year=date.year,
                    month=date.month_txt)
                future_name = '{name}{ext}'.format(
                    name=self.format_filename_from_data(date),
                    ext=os.path.splitext(orig_f_path)[-1])

                if not os.path.exists(future_dir):
                    os.makedirs(future_dir)
                future_f_path = os.path.join(future_dir, future_name)

                # Change filename if both files has the same time
                future_f_path = self.change_filename_if_exists(
                    orig_f_path, future_f_path)

                # Move file to a new place
                shutil.copyfile(orig_f_path, future_f_path)
                os.remove(orig_f_path)
                # pylint: disable=superfluous-parens
                print('{0}\n  -> {1}'.format(orig_f_path, future_f_path))

            else:
                # do nothing with files with no EXIF data
                pass
                '''
                # if we do not have date in EXIF
                future_dir = '{dir}/no_exif'.format(
                    dir=DESTINATION_DIR)
                future_name = os.path.split(orig_f_path)[1]
                if not os.path.exists(future_dir):
                    os.makedirs(future_dir)
                future_f_path = os.path.join(future_dir, future_name)

                # Change filename if both files has the same time
                future_f_path = self.change_filename_if_exists(
                    orig_f_path, future_f_path)

                # Copy file to a new place
                shutil.copyfile(orig_f_path, future_f_path)
                '''


if __name__ == "__main__":
    SORTER = Sorter()
    SORTER.run()

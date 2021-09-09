from alphanumeric import *
import random
import subprocess


def num_days(year, month=13):
    '''
        Returns number of days in given year (optionally, given year and month)

        Args:
            year (int): year in Gregorian calendar
            month (int): (optional) month 
    '''
    modifier = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 28 + modifier, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if month != 13:
        return days[month - 1]
    return sum(days)


def epoch_converter(y: int, m: int, d: int) -> int:
    '''
        Returns UNIX epoch time
        
        Args:
            y (int): year in Gregorian calendar
            m (int): month in Gregorian calendar
            d (int): day in Gregorian calendar
    '''
    ey, em, ed = 1970, 1, 1
    epoch = 0
    epoch += 86400 * sum(num_days(i) for i in range(ey, y))
    epoch += 86400 * sum(num_days(y, i) for i in range(em, m))
    epoch += 86400 * (d - ed)
    return epoch


def jan_first(year:int, base=1899) -> int:
    '''
        Returns the day of the week on January 1, year
        (Sunday == 0, Saturday == 6)

        Args:
            year (int): year in Gregorian calendar
    '''
    backward = (year < base)
    sum_days = 0 - 2 * backward
    for y in range(base, year - backward, 1 - 2 * backward):
        sum_days += num_days(y)
    return sum_days % 7 if not backward else 6 - (sum_days % 7)


def get_graph(year: int) -> list[int]:
    '''
        Returns a blank graph for the year, 1 represents valid day.

        Args:
            year (int): year in Gregorian calendar

        Warning:
            It tries to mimic the contribution graph of GitHub.com.
            But GitHub.com has a bug on year 2000.
            https://github.com/username?tab=overview&from=2000-01-01
            The graph started on Sunday, but it should start on Saturday.
            The other years seems okay.
    '''
    graph = [[1 for _ in range(53)] for _ in range(7)]
    start = jan_first(year)
    days = num_days(year)
    for i in range(start):
        graph[i][0] = 0
    for i in range(6, start + (days == 366), -1):
        graph[i][-1] = 0
    return graph


def draw_on_graph(year: int, s: str, daily_commits=9) -> list[int]:
    '''
        Returns a drawing for the year, number represents # of commits for the day.

        Args:
            year (int): year in Gregorian calendar
            s (str): things to write (len < 9, English alphanumeric only)
    '''
    assert len(s) < 9, 's should be shorter than 10 characters'
    assert all(1 if c.encode().isalpha() or c.isdigit() else 0 for c in s), \
                                            's should be English alphanumeric'
    graph = get_graph(year)
    line = [[0] for _ in range(7)]
    for i in range(7):
        for c in ''.join(c.lower() if c.isalpha() else c for c in s):
            line[i] += [daily_commits if n else 2 for n in cmap[c][i]] + [1]
        graph[i] = [graph[i][0]] + line[i][1:-1] + graph[i][len(line[i]) - 1:]
    return graph


def num_commits(graph: list[int]) -> list[int]:
    '''
        Returns number of commits from Jan 1 to Dec 31

        Args:
            graph (list): what you got from draw_on_graph()
    '''
    start, end = float('inf'), -float('inf')
    for i in range(7):
        if graph[i][0]:
            start = min(start, i)
        if graph[-i - 1][-1]:
            end = max(end, -i)
    return [graph[y][x] for x in range(53) for y in range(7)][start:end]


def commit(y: int, cmts: list[int], limit: int, fname: str, c: str) -> None:
    '''
        Make automated commits and returns None

        Args:
            y (int): the year you want to make automated commits (YYYY)
            cmts (list[int]): a list you got from num_commits which contains
                a number of commits from Jan 1 to Dec 31 in the given year
            limit (int): maximum daily commit
            fname (str): the name of dummy file you want to make commit
            c (str): commit comment

    '''
    c = '"' + c + '"'
    epoch_day = epoch_converter(y, 1, 1)
    subprocess.run(f'touch {fname}')
    for cmt_today in cmts:
        rand_num = limit - random.randint(0, limit // 10)
        randomized_time = epoch_day
        for _ in range(rand_num if cmt_today > 2 else cmt_today):
            with open(fname, 'a+') as f:
                f.write('1')
            subprocess.run(f'git add {fname}')
            randomized_time += random.randint(1, 86399 // cmt_today)
            commit_cmd = f'git commit --date {randomized_time} -S -m {c}'
            subprocess.run(commit_cmd)
        epoch_day += 86400


def main():
    year = 2020
    draw = 'e1630m'
    max_daily_commits = 50
    dummy_file_name = 'dummy.txt'
    comment = 'Automated Commit'
    cmt_lst = num_commits(draw_on_graph(year, draw, max_daily_commits))
    commit(year, cmt_lst, 10, dummy_file_name, comment)


if __name__ == '__main__':
    main()

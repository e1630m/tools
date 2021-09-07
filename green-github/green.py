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


def repo_creator(repo_name='git-greener', option='priv') -> str:
    # TODO 
    # Create (private) repo for those dummy commits
    '''
        Create a (private) repo on GitHub and returns local path of the repo

        Args:
            repo_name (str): (optional) name of the repo
            option (str): (optional) 'pub' for public repo,
                                     'priv' for private repo (default) 
    '''
    pass
    username = ''   # EDIT THIS (Your GitHub username)
    ghp = ''        # EDIT THIS (Your GitHub PAT, which has repo access)
    base_path = ''  # EDIT THIS (/path/to/parent/dir/of/your/repo)
    return base_path + '/' + repo_name


def commit(year: int, cmt_lst: list[int], daily_cmt: int, path: str) -> None:
    # TODO
    # Generate dummy file / content and commit set number of times (commits_to_do) for each day 
    # command: git commit --date “Fri Jan 15 00:01 2021 +0000"
    pass
    subprocess.run('cd ' + path)
    subprocess.run('touch dummy.txt')
    pre = 'git commit --date "'
    post = '" -S -m "Automated Commit"'
    t = epoch_converter(year, 1, 1)
    for day in cmt_lst:
        num_commit_today = day
        if day > 2:
            num_commit_today = daily_cmt - random.randint(0, daily_cmt // 10)
        tmp = t
        for _ in range(num_commit_today):
            subprocess.run('echo 1 >> dummy.txt')
            subprocess.run('git add dummy.txt')
            tmp += random.randint(1, 86399 // num_commit_today)
            cmd = pre + str(tmp) + post
            subprocess.run(cmd)
        t += 86400


def main():
    year = 2021
    word = 'e1630m'
    daily_commits = 50
    cmt_lst = num_commits(draw_on_graph(year, word, daily_commits))
  #  print(num_days(year), len(commmits_to_do), commmits_to_do[0], commmits_to_do[-1])
    print(epoch_converter(2021, 9, 7))


if __name__ == '__main__':
    main()

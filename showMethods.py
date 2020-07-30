<<<<<<< HEAD
<<<<<<< HEAD
import click


# 给出一个总长度 给出一个现在进度 打印进度条
def progressBar(current, total, text):
    percent_fl = current / total
    percent = int(percent_fl * 100)
    left = 100 - percent
    x = ["#" for i in range(percent + 1)]
    y = [" " for i in range(left + 1)]
    click.echo(
        click.style("[{}{}][%{:.1f}] {}:{}/{}".format("".join(x), "".join(y), percent_fl * 100, text, current, total),
        fg='green'))
=======
import click


# 给出一个总长度 给出一个现在进度 打印进度条
def progressBar(current, total, text):
    percent_fl = current / total
    percent = int(percent_fl * 100)
    left = 100 - percent
    x = ["#" for i in range(percent + 1)]
    y = [" " for i in range(left + 1)]
    click.echo(
        click.style("[{}{}][%{:.1f}] {}:{}/{}".format("".join(x), "".join(y), percent_fl * 100, text, current, total),
        fg='green'))
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
=======
import click


# 给出一个总长度 给出一个现在进度 打印进度条
def progressBar(current, total, text):
    percent_fl = current / total
    percent = int(percent_fl * 100)
    left = 100 - percent
    x = ["#" for i in range(percent + 1)]
    y = [" " for i in range(left + 1)]
    click.echo(
        click.style("[{}{}][%{:.1f}] {}:{}/{}".format("".join(x), "".join(y), percent_fl * 100, text, current, total),
        fg='green'))
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db

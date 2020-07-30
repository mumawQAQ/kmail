<<<<<<< HEAD
<<<<<<< HEAD
import imaplib
import click
import reMethods
import echoError
import emailMethods
import pickle
import os


# 登录邮箱的方法
@click.group()
def cli1():
    pass


@cli1.command(help='login in email')
@click.option('-e', '--email', help='[Email] request')
@click.option('-p', '--password', hide_input=True, prompt='password', confirmation_prompt=True,
              help='[Email Password/Access code] option')
@click.option('-g', '--group', default='inbox', help='[Email group] option default=inbox')
def login(email, password, group):
    """
    --------------------------------------------------------------------

    currently only support Gmail

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")
    if email is None:
        echoError.errorStatement('Error: you have to enter a email by using -e/--email [email]')
    else:
        if reMethods.MatchEmail(email) is None:
            echoError.errorStatement('Error: please enter a email in right format')
        else:
            url = 'imap.gmail.com'
            m = emailMethods.loginEmail(email, password, group, url)
            if m is not None:
                emailMethods.storeInfo(email, password, group, url)

    click.echo(" ")
    echoError.finishStatement('--Finished init--')


@click.group()
def cli2():
    pass


@cli2.command(help='start to gather infomations')
@click.option('-o', '--options', help='[infos options] request', type=click.Choice(
    ["All","date", "tracking", "order_number", "shipped_name_and_address", "product_name_and_qty"]), multiple=True)
@click.option('-t', '--target', help='[shipping target] request', type=click.Choice(["Target", "BestBuy"]))
@click.option('-n', '--name', help='[saving name] option', default='result.xlsx')
@click.option('-e', '--email', help='[Email] option')
@click.option('-p', '--password', help='[Email Password/Access code] option')
@click.option('-g', '--group', help='[Email group] option')
@click.option('-S', '--start', help='[Start date] option (time format: year/month/day or '
                                    'year/month/day/hour/minute/second)')
@click.option('-E', '--end', help='[End date] option (time format: year/month/day or '
                                  'year/month/day/hour/minute/second)')
def start(options, target, name, email, password, group, start, end):
    """
    --------------------------------------------------------------------

    Start to read emails and form a excel file

    by default start and end should be all the emails in the email group

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")

    # 如果没有输入目标信息则报错
    if target is None:
        echoError.errorStatement('Error: You have to enter a target by using -t/--target [Target/BestBuy]')
    else:
        # 处理开始时间和结束时间
        if start is not None:
            stime = reMethods.getTime(start)
        else:
            stime = start
        if end is not None:
            etime = reMethods.getTime(end)
        else:
            etime = end

        # 如果输入了邮箱和密码
        # 则使用当前邮箱和密码
        if email is not None and password is not None:
            if reMethods.MatchEmail(email) is None:
                echoError.errorStatement('Error: Please enter a email in right format')
            else:
                url = 'imap.gmail.com'
                # 如果用户没有输入group则设为默认值inbox
                if group is None:
                    group = 'inbox'
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m,items,target,{"startTime":stime,"endTime":etime,"options":options},name)

        else:
            # 如果没有输入邮箱和密码
            # 获取保存的邮箱和密码
            path = os.getcwd()
            try:
                f = open(path + '/src/info', 'rb')
                info = pickle.load(f)
            except:
                echoError.errorStatement('Error: Fail to read login in information [you need to login or use -e ['
                                         'email] -p [password]]')
            else:
                email = info[0]
                password = info[1]
                if group is None:
                    group = info[2]
                url = info[3]
                # 因为之前保存过基本信息了 所以不用重复保存
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m, items, target, {"startTime": stime, "endTime": etime, "options": options},name)


    click.echo(" ")
    echoError.finishStatement('--Finished init--')


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
=======
import imaplib
import click
import reMethods
import echoError
import emailMethods
import pickle
import os


# 登录邮箱的方法
@click.group()
def cli1():
    pass


@cli1.command(help='login in email')
@click.option('-e', '--email', help='[Email] request')
@click.option('-p', '--password', hide_input=True, prompt='password', confirmation_prompt=True,
              help='[Email Password/Access code] option')
@click.option('-g', '--group', default='inbox', help='[Email group] option default=inbox')
def login(email, password, group):
    """
    --------------------------------------------------------------------

    currently only support Gmail

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")
    if email is None:
        echoError.errorStatement('Error: you have to enter a email by using -e/--email [email]')
    else:
        if reMethods.MatchEmail(email) is None:
            echoError.errorStatement('Error: please enter a email in right format')
        else:
            url = 'imap.gmail.com'
            m = emailMethods.loginEmail(email, password, group, url)
            if m is not None:
                emailMethods.storeInfo(email, password, group, url)

    click.echo(" ")
    echoError.finishStatement('--Finished init--')


@click.group()
def cli2():
    pass


@cli2.command(help='start to gather infomations')
@click.option('-o', '--options', help='[infos options] request', type=click.Choice(
    ["All","date", "tracking", "order_number", "shipped_name_and_address", "product_name_and_qty"]), multiple=True)
@click.option('-t', '--target', help='[shipping target] request', type=click.Choice(["Target", "BestBuy"]))
@click.option('-n', '--name', help='[saving name] option', default='result.xlsx')
@click.option('-e', '--email', help='[Email] option')
@click.option('-p', '--password', help='[Email Password/Access code] option')
@click.option('-g', '--group', help='[Email group] option')
@click.option('-S', '--start', help='[Start date] option (time format: year/month/day or '
                                    'year/month/day/hour/minute/second)')
@click.option('-E', '--end', help='[End date] option (time format: year/month/day or '
                                  'year/month/day/hour/minute/second)')
def start(options, target, name, email, password, group, start, end):
    """
    --------------------------------------------------------------------

    Start to read emails and form a excel file

    by default start and end should be all the emails in the email group

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")

    # 如果没有输入目标信息则报错
    if target is None:
        echoError.errorStatement('Error: You have to enter a target by using -t/--target [Target/BestBuy]')
    else:
        # 处理开始时间和结束时间
        if start is not None:
            stime = reMethods.getTime(start)
        else:
            stime = start
        if end is not None:
            etime = reMethods.getTime(end)
        else:
            etime = end

        # 如果输入了邮箱和密码
        # 则使用当前邮箱和密码
        if email is not None and password is not None:
            if reMethods.MatchEmail(email) is None:
                echoError.errorStatement('Error: Please enter a email in right format')
            else:
                url = 'imap.gmail.com'
                # 如果用户没有输入group则设为默认值inbox
                if group is None:
                    group = 'inbox'
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m,items,target,{"startTime":stime,"endTime":etime,"options":options},name)

        else:
            # 如果没有输入邮箱和密码
            # 获取保存的邮箱和密码
            path = os.getcwd()
            try:
                f = open(path + '/src/info', 'rb')
                info = pickle.load(f)
            except:
                echoError.errorStatement('Error: Fail to read login in information [you need to login or use -e ['
                                         'email] -p [password]]')
            else:
                email = info[0]
                password = info[1]
                if group is None:
                    group = info[2]
                url = info[3]
                # 因为之前保存过基本信息了 所以不用重复保存
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m, items, target, {"startTime": stime, "endTime": etime, "options": options},name)


    click.echo(" ")
    echoError.finishStatement('--Finished init--')


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
=======
import imaplib
import click
import reMethods
import echoError
import emailMethods
import pickle
import os


# 登录邮箱的方法
@click.group()
def cli1():
    pass


@cli1.command(help='login in email')
@click.option('-e', '--email', help='[Email] request')
@click.option('-p', '--password', hide_input=True, prompt='password', confirmation_prompt=True,
              help='[Email Password/Access code] option')
@click.option('-g', '--group', default='inbox', help='[Email group] option default=inbox')
def login(email, password, group):
    """
    --------------------------------------------------------------------

    currently only support Gmail

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")
    if email is None:
        echoError.errorStatement('Error: you have to enter a email by using -e/--email [email]')
    else:
        if reMethods.MatchEmail(email) is None:
            echoError.errorStatement('Error: please enter a email in right format')
        else:
            url = 'imap.gmail.com'
            m = emailMethods.loginEmail(email, password, group, url)
            if m is not None:
                emailMethods.storeInfo(email, password, group, url)

    click.echo(" ")
    echoError.finishStatement('--Finished init--')


@click.group()
def cli2():
    pass


@cli2.command(help='start to gather infomations')
@click.option('-o', '--options', help='[infos options] request', type=click.Choice(
    ["All","date", "tracking", "order_number", "shipped_name_and_address", "product_name_and_qty"]), multiple=True)
@click.option('-t', '--target', help='[shipping target] request', type=click.Choice(["Target", "BestBuy"]))
@click.option('-n', '--name', help='[saving name] option', default='result.xlsx')
@click.option('-e', '--email', help='[Email] option')
@click.option('-p', '--password', help='[Email Password/Access code] option')
@click.option('-g', '--group', help='[Email group] option')
@click.option('-S', '--start', help='[Start date] option (time format: year/month/day or '
                                    'year/month/day/hour/minute/second)')
@click.option('-E', '--end', help='[End date] option (time format: year/month/day or '
                                  'year/month/day/hour/minute/second)')
def start(options, target, name, email, password, group, start, end):
    """
    --------------------------------------------------------------------

    Start to read emails and form a excel file

    by default start and end should be all the emails in the email group

    --------------------------------------------------------------------
    """
    echoError.startStatment('--Start to init--')
    click.echo(" ")

    # 如果没有输入目标信息则报错
    if target is None:
        echoError.errorStatement('Error: You have to enter a target by using -t/--target [Target/BestBuy]')
    else:
        # 处理开始时间和结束时间
        if start is not None:
            stime = reMethods.getTime(start)
        else:
            stime = start
        if end is not None:
            etime = reMethods.getTime(end)
        else:
            etime = end

        # 如果输入了邮箱和密码
        # 则使用当前邮箱和密码
        if email is not None and password is not None:
            if reMethods.MatchEmail(email) is None:
                echoError.errorStatement('Error: Please enter a email in right format')
            else:
                url = 'imap.gmail.com'
                # 如果用户没有输入group则设为默认值inbox
                if group is None:
                    group = 'inbox'
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m,items,target,{"startTime":stime,"endTime":etime,"options":options},name)

        else:
            # 如果没有输入邮箱和密码
            # 获取保存的邮箱和密码
            path = os.getcwd()
            try:
                f = open(path + '/src/info', 'rb')
                info = pickle.load(f)
            except:
                echoError.errorStatement('Error: Fail to read login in information [you need to login or use -e ['
                                         'email] -p [password]]')
            else:
                email = info[0]
                password = info[1]
                if group is None:
                    group = info[2]
                url = info[3]
                # 因为之前保存过基本信息了 所以不用重复保存
                m = emailMethods.loginEmail(email, password, group, url)
                if m is not None:
                    items = emailMethods.getIdList(m)
                    # 这段为测试代码 可以删除
                    click.echo(click.style('Total email:{}'.format(len(items)), fg='green'))
                    emailMethods.getInfo(m, items, target, {"startTime": stime, "endTime": etime, "options": options},name)


    click.echo(" ")
    echoError.finishStatement('--Finished init--')


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db

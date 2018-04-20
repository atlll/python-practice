# -*- coding: utf-8 -*-
'''登录系统&猜大小2.0'''

import random
import pymysql
import re

'''
author：atlll
email：1337286582@11.com
date：2018-4-12
'''

#连接数据库
try:
    coo = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='19960327zt',
        db = 'test2',
        charset='utf8'
        )
except Exception as e:
    print '\n',str.center('( Waring!!! )',60,'*'),'\n'*2,str.center('If The Operation Is Improper, Please Connect The Database First',60,' '),'\n',str.center('o((⊙﹏⊙))o',50,' ')
    #print e
else:
    cursor = coo.cursor()    

    sql_show_table = 'show tables'
    #查看所有数据表
    sql_select_table = 'select * from pytest'
    #查看数据表pytest内的信息
    sql_insert_table = 'insert into pytest(username,passwd) values(%s , sha(%s))'
    #向数据表pytest中插入信息
    sql_select_username = 'select username from pytest where username = %s'
    #查看数据表中username为***的信息
    sql_select_passwd = 'select passwd from pytest where passwd = sha(%s)'
    #查看数据表中的passwd为***的信息
    #sql_truncate = 'truncate table pytest'
    sql_delete_user = 'delete from pytest where username = %s'
    sql_create_table1 = 'create table pytest(id smallint unsigned not null auto_increment key,\
                                            username varchar(20) not null,\
                                            passwd varchar(40) not null )'
    sql_select_all_user = 'select username from pytest'
    sql_select_all_passwd = 'select passwd from pytest'

    #创建数据表
    cursor.execute(sql_show_table)
    rs = cursor.fetchall()
    #print rs
    dbtable = (u'pytest',)
    if dbtable in rs:
        pass
    else:
        cursor.execute(sql_create_table1)        
        coo.commit()


    def new_username():
        '''创建用户名
        '''
        input_username = raw_input('请输入用户名(首字母为英文&下划线)：\n')
        if re.match(r'^[a-zA-Z_].{2,9}$', input_username):
            #匹配一个首字母是英文or下划线的input_username
            if cursor.execute(sql_select_username,input_username):
                print '\n','用户名以存在!\n'
                new_username()
            else:
                return input_username
            #返回创建用户名
        else:
            print '输入格式有错误！重新输入：\n'
            new_username()

    def new_passwd():
        '''创建用户密码
        '''
        input_passwd = raw_input('请输入密码：\n')
        return input_passwd
        #返回创建用户名密码

    #注册用户
    def create_user():
        '''用户注册并将注册信息存入数据库'''
        try:
            cursor.execute(sql_insert_table,[new_username(),new_passwd()])
            coo.commit()
        except Exception as e:
            print e
        else:
            print '注册成功！','\n','-'*43
        

    def login_usename():
        '''输入用户名
        '''
        set_username = raw_input('请输入你的用户名：\n')
        return set_username
        #返回输入用户名

    def login_passwd():
        '''输入用户密码
        '''
        set_passwd = raw_input('请输入你的密码：\n')
        return set_passwd
        #返回输入用户名密码

    #登录用户
    def login_game():
        i = 0
        #密码输入次数初始值
        if cursor.execute(sql_select_username,[login_usename()]):
            #判断用户名是否在数据库中
            print '账号输入成功！'
            coo.commit()
            if cursor.execute(sql_select_passwd,[login_passwd()]):
                #判断用户密码是否在数据库中
                coo.commit()
                print '登录成功!'  
                start_game()
            else:
                while  i < 3:
                    in_while = raw_input('please enter your passwd:\n')
                    if cursor.execute(sql_select_passwd,[in_while]):
                        start_game()
                        break
                    else:
                        print '密码错误，您还有{}次机会：\n'.format(2 - i)
                        i += 1
                else:
                   print '已输入错误密码3次！(＞﹏＜)'
              #  cursor.close()
               # coo.close()        
        else:
            print '账号输入失败！请重新输入：\n'
            login_game()
      

    #总开始
    def all_start():
        print str.center('欢迎进入猜大小游戏！',55,'-')
        print 'PS: ╮(๑•́ ₃•̀๑)╭ 在进入游戏之前，你需要登录游戏','\n',' '*10,'*输入 0 注册游戏！','\n',' '*10,'*输入 1 登录游戏！','\n',' '*10,'*输入 2 退出游戏！','\n'
        for i in xrange(4):
            for j in xrange(11):
                print '*','\t',
            print '\n'
        starts = raw_input('请填入你的选择( ｡ớ ₃ờ):\n')
        startres = [0,1,2]
        if starts.isdigit():
            start = int(starts)
            if start in startres:
                if start == 0:
                    create_user()
                    print '\n',str.center('如果您注册成功，请选择登录游戏(1) & 退出游戏(2):',50,'-'),'\n','(๑•̀ㅂ•́)و✧','\n'
                    create_login_func()
                elif start == 1:
                    login_game()
                elif start == 2:
                    print '您已退出游戏！'
                    cursor.close()
                    coo.close()
            else: 
                print '-'*40
                print '请输入0 & 1：'
                print '-'*40,'\n'
                all_start()
        else:
            print '-'*40
            print 'WTF?输入错误？请按照指示输入(≧口≦)：'
            print '-'*40,'\n'
            all_start()

    #注册后的选择
    def create_login_func():
        create_login = raw_input('请输入你的选择：\n')
        create_loginres = [1,2]
        if create_login.isdigit():
            created_login = int(create_login)
            if created_login in create_loginres:
                if created_login == 1:
                    login_game()
                elif created_login == 2:
                    print '您已退出游戏！'
                    cursor.close()
                    coo.close()
            else:
                print '格式错误！：\n'
                create_login_func()
        else:
            print '格式错误！：\n'
            create_login_func()



    def roll_dict(numbers=3, points=None):
        '''摇骰子
        '''
        print str.center('摇骰子', 50,'-')
        if points is None:
            points = []
        while numbers > 0:
            point = random.randrange(1, 7)
            points.append(point)
            numbers = numbers - 1
        return points


    def roll_result(total):
        '''选定大小
        '''
        is_Big = 11 <= total <= 18
        is_Small = 3 <= total <= 10
        if is_Big:
            return '大'
        elif is_Small:
            return '小'


    def start_game():
        '''开始游戏
        '''
        your_money = 1000
        while your_money > 0:
            print str.center('游戏开始', 50, '-')
            print '你目前有本金{}元'.format(your_money)
            choice = ['大', '小']
            your_choice = raw_input('请下注 ，大 & 小：')
            if your_choice not in choice:
                print '格式错误，请重新输入：\n'
                your_choice = raw_input('请下注 ，大&小：')
            your_bet = input('下注金额：')
            if your_choice in choice:
                points = roll_dict()
                total = sum(points)
                youWin = your_choice == roll_result(total)
                if youWin:
                    print '骰子点数', points
                    print '恭喜！你赢了{}钱，你现在有{}元本金'.format(your_bet, your_money + int(your_bet))
                    your_money = your_money+int(your_bet)
                else:
                    print '骰子点数', points
                    print '很遗憾，你输了{}钱，你现在有{}元本金'.format(your_bet, your_money - int(your_bet))
                    your_money = your_money-int(your_bet)
            else:
                print '格式错误，请重新输入'
        else:
            print '游戏结束，祝好运！( ｡ớ ₃ờ)'

    if __name__ == '__main__':
        all_start()

#1.简单的注册登录功能
#2.
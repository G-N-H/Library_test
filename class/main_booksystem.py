'''
图书管理系统的编写:
'''
import csv

import json

from datetime import datetime

from LibrarySystem.basic.path import FILE_PATH1, FILE_PATH2


class Book(object):
    """
    属性：书名name 作者author 是否借出 isborrow 书籍ID bookID 书籍类型category
    注意：书籍ID不能重复
    """

    @property
    def name(self):
        book_name = input("请输入书名：")
        return book_name

    @property
    def author(self):
        book_author = input("请输入书籍作者：")
        return book_author

    # 根据书库判断是否借出
    @property
    def is_borrow(self):
        # 根据书籍id查询是否已经借出
        book_id = input("请输入确认书籍的ID:")
        with open(FILE_PATH1, mode='r+', encoding='GBK') as read_object:
            for line in read_object:
                if book_id == line.strip().split('-')[-1]:
                    with open(FILE_PATH2, mode='r+', encoding='GBK') as borrow_object:
                        for borrow_line in borrow_object:
                            if book_id in borrow_line:
                                print("此书已借出")
                                break
                        else:
                            print("{}此书在馆".format(line))
                            return line

            else:
                print("请确认输入的书籍ID是否正确")

    @property
    def book_ID(self):
        # 生成唯一的bookID,
        generate_bookID = "MINIB" + datetime.now().strftime("%Y%m%d%H%M%S")
        print("书本的ID是：{}".format(generate_bookID))
        return generate_bookID

    @property
    def category(self):
        book_type_list = ["文学类", "科技类", "艺术类", "医学类"]
        book_category = input("请选择书籍的类型:\n1.文学类\n2.科技类\n3.艺术类\n4.医学类\n:")
        for _ in book_type_list:
            if book_category.strip() == "1":
                return book_type_list[0]
            elif book_category.strip() == "2":
                return book_type_list[1]
            elif book_category.strip() == "3":
                return book_type_list[2]
            elif book_category.strip() == "4":
                return book_type_list[3]
            else:
                print("请选择以上其中一种类型")
                continue


class BookManager(Book):
    """
    图书管理员使用——图书管理系统
    """

    def add_book(self):
        """
        1.添加图书：把添加的图书信息写进book_base.csv文件，写进原始书库
        :return:None
        """
        # 把新添加的书籍写入book_base.csv中
        with open(FILE_PATH1, mode='a', encoding='GBK') as book_object:
            # 执行Book类中的属性：name author book_ID category
            book_object.write('{}-{}-{}-{}\n'.format(self.name, self.author, self.category, self.book_ID))
            book_object.flush()
            print("书本添加入库成功！")

    def borrow_book(self):
        """
        2.借书 （根据图书名字借书）先检验图书是否存在、后图书是否已经借出:
            借书的时候先去读取保存的书籍中是否存在，
        :return:
        """

        borrow_name = input("请输入要借的书名：")
        with open(FILE_PATH1, mode='r+', encoding='GBK') as read_object:
            for borrow_line in read_object:
                # 判断是否存在这本书
                if borrow_name in borrow_line:
                    borrow_choice = input("请问您是要借：{}这本书吗？Y/N:".format(borrow_line))
                    if borrow_choice.upper() == "Y":
                        # 图书已借出
                        if self.is_borrow is None:
                            print("您可以尝试借其他书")
                        # 借出书籍，写进借书库borrow_base中
                        else:
                            with open(FILE_PATH2, mode='a', encoding='GBK') as borrow_object:
                                borrow_object.write(borrow_line.split('-')[-1])
                                print("借书成功！")
                                break
            else:
                print("抱歉，未找到这本书，您可以看下其他的书")

    def return_book(self):
        """
        3.还书：根据book_ID校验还书
        :return:
        一次还一本，还书成功，会在borrow_base.csv中删除相应bookID
        """
        return_list = []
        return_id = input("请输入要还的书本的ID：")
        return_list.append(return_id)
        with open(FILE_PATH2, mode='r', encoding='GBK') as return_object:
            # 注：csv列表删除行操作，新功能
            reader = csv.reader(return_object)
            lines = list(reader)  # 将所有行保存为列表
            for index, line in enumerate(lines):
                # 获取当前要还书的那一行的索引和内容
                if return_list == line:
                    del lines[index]
                    # 写进文件，更新借书ID
                    with open(FILE_PATH2, 'w', newline='') as new_borrow_object:
                        writer = csv.writer(new_borrow_object)
                        writer.writerows(lines)
                        print("还书成功！")  # 将未删除（除了要还的书的那个ID）的所有行写入文件
                        break
            else:
                print("请确认您要还的书籍的ID")

    def search_book(self):
        """
         4.查询书籍 （根据名字查询， 根据类别查询）：
            查询book_base.csv数据
        :return:
        """
        with open(FILE_PATH1, mode='r', encoding='GBK') as search_object:
            search_choice = input("请输入需要查询的书籍：1.名称 2.类别:")
            if search_choice == "1":
                search_name = input("请输入书名：")
                # 输出只要有与搜索名字相关的书籍
                for line in search_object:
                    if search_name in line:
                        print(line)
                    continue
            elif search_choice == "2":
                # 匹配选择的有相同的类型的文字输出这些书
                search_type = self.category
                for line in search_object:
                    category_type = line.split('-')[-2]
                    if search_type == category_type:
                        print(line)
            else:
                print("请您以上您想查询的方式")
                # 提醒选择1、2搜索方式


    def edit_book(self):
        """
        5.修改书籍信息（根据书籍ID修改）
        :return:
        """
        edit_list = []
        edit_id = input("请输入要修改的书本的ID：")
        with open(FILE_PATH1, mode='r+', encoding='GBK') as edit_object:
            for edit_line in edit_object:
                if edit_line.strip().split('-')[-1] == edit_id:
                    edit_list.append(edit_line.strip())
                    # 确定要修改的内容
                    print(edit_list)
                    with open(FILE_PATH1, mode='r+', encoding='GBK') as edit2_object:
                        reader = csv.reader(edit2_object)
                        lines = list(reader)  # 读取所有行保存为列表
                        for index, line in enumerate(lines):
                            # 确定是哪一行
                            if edit_list == line:
                                new_book_info = ["{}-{}-{}-{}".format(self.name, self.author, self.category, edit_id)]
                                lines[index] = new_book_info
                                # 修改写入
                                with open(FILE_PATH1, mode='w', newline='') as new_book_base_object:
                                    writer = csv.writer(new_book_base_object)
                                    writer.writerows(lines)  # 将所有行写入文件
                                    print("修改成功！")
                                    break
            else:
                print("请确定您要修改的书籍信息")

    def jason_save(self):
        """
                6.本地化保存数据信息(json格式)
                :return:
                """
        data = []
        data_dict = {}
        # 读取原始书库所有书籍信息
        with open(FILE_PATH1, mode='r', encoding='GBK') as jason_file_object:
            for line in jason_file_object:
                # 把每一行都分割成字符串
                line_data = line.strip().split('-')
                data_dict['name'] = line_data[0]
                data_dict['author'] = line_data[1]
                data_dict['category'] = line_data[2]
                data_dict['bookID'] = line_data[3]
                data.append(data_dict)
            # 数据类型 -> json ，序列化
            res = json.dumps(data, ensure_ascii=False)
            print(res)


def run():
    obj = BookManager()
    while True:
        choice = input(
            "请选择：\n1.添加书籍\n2.借书\n3.还书\n4.查询书籍\n5.修改书籍信息\n6.查看本地化保存数据信息(json格式):")

        if choice == "1":
            while True:
                obj.add_book()
                exit_choice = input("请问要继续添加吗？退出Q/q：")
                if exit_choice.upper() == "Q":
                    break

        elif choice == "2":
            while True:
                obj.borrow_book()
                exit_choice = input("请问要继续借书吗？退出Q/q：")
                if exit_choice.upper() == "Q":
                    break
        elif choice == "3":
            while True:
                obj.return_book()
                exit_choice = input("请问要继续还书吗？退出Q/q：")
                if exit_choice.upper() == "Q":
                    break
        elif choice == "4":
            while True:
                obj.search_book()
                exit_choice = input("请问还要查询吗？退出Q/q：")
                if exit_choice.upper() == "Q":
                    break
        elif choice == "5":
            while True:
                obj.edit_book()
                exit_choice = input("请问还要修改吗？退出Q/q：")
                if exit_choice.upper() == "Q":
                    break
        elif choice == "6":
            while True:
                obj.jason_save()
                exit_choice = input("退出Q/q：")
                if exit_choice.upper() == "Q":
                    break


if __name__ == '__main__':
    run()

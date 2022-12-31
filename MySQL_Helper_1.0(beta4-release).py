'''
-*- coding: utf-8 -*-
#                                                                                                 #
#            / __________/      (*)       _________.     _________.                               #
#           / /__________.     / /       / _____  /     / _____  /                                #
#          / /________  /     / /       / /____/ /     / /____/ /        ___.    ____    __*      #
#         / /                / /     . / /______.     / /______.        /___/    ___|   |  |      #
#         \_                / /        \__**___/      \__**___/         ___/    |____   |__|      # 
#                                                                                                 #

@File  : MySQL_Helper_1.0(beta4-release).py
@author: Fiee920
@Feedback: 2356854247@qq.com
@Time  : 2022/12/31 12:50
'''
import re


class dev:
    @staticmethod
    def dicAdd():
        dic = []
        while True:
            val = input()
            if val != "0":
                dic.append(val)
            else:
                break
        print(dic)


class Test:
    @staticmethod
    def main():
        while True:
            words = input("键入中文指令[0停止] -> ")
            if words != "0":
                logic.init()
                wordsSet = participle(words)
                key = logic.do(wordsSet)
                key = logic.KeyFix(key)
                produce.getIndex(words)
                print(" DEBUG ===== > @Test.main ===== > run '{}'".format(str(key)))
                funX = getattr(produce, key)
                print("\n Result ->\n")
                print(funX(words).upper())
            else:
                break

    @staticmethod
    def func1():
        dn = decisionNode()
        dn.setRUN(Test, "run")
        func = dn.getRUN()
        func(12)

    @staticmethod
    def run(index):
        print("create database if not exists {};".format(index))

    @staticmethod
    def func2():
        logic.init()
        logic.do("创建一些表")

    @staticmethod
    def func3():
        words = input("键入指令 -> ")
        logic.init()
        result = ""
        wordsSet = participle(words)
        funName = logic.do(wordsSet)
        produce.getIndex(words)
        funX = getattr(produce, funName)
        print(funX(words))

    @staticmethod
    def func4():
        wordsSet = participle("删除xx列中的xxx数据")
        logic.init()
        key = logic.do(wordsSet)
        logic.KeyFix(key)


# =================================================== ↑ 开发测试
# =================================================== ↓ 程序主体


class resource:
    CN_KEY_DIC = ['查', '查询', '建', '创建', '改', '更改', '修改', '改为', '变为', '加', '添加', '删', '删除', '删掉', '搜索', '查找', '数据', '表',
                  '表格',
                  '数据库', '类型', '结构', '内容', '库', '列', '全部列', '全部', '所有']
    EN_KEY_DIC = ['Create', 'Modify', 'Add', 'Delete', 'Search', 'Table', 'Base', 'Data', 'Column', 'Type', 'Structure',
                  'Content', 'All']


class decisionNode:
    def __init__(self):
        self.symbol = None
        self.KeyWord = []
        self.ExcludePoint = []  # TODO 待开发
        self.Point = []
        self.run = None

    def addKeyWord(self, newKeyWd):
        self.KeyWord.append(newKeyWd)

    def addKeyWords(self, Keywords):
        for Keyword in Keywords:
            self.KeyWord.append(Keyword)

    def addPoint(self, newPoint):
        self.Point.append(newPoint)

    def addPoints(self, points):
        for point in points:
            self.Point.append(point)

    def addExcludePoint(self, newEkeywd):
        self.ExcludePoint.append(newEkeywd)

    def addExcludePoints(self, newEkeywds):
        for Ekeywd in newEkeywds:
            self.ExcludePoint.append(Ekeywd)

    def hasPoint(self):
        return len(self.Point) != 0

    def setSymbol(self, value):
        self.symbol = value

    def runSetting(self, key):
        self.run = key

    def runGetter(self):
        return self.run


class logic:
    @staticmethod
    def init():
        global TABLE, BASE, DATA, COLUMN, TYPE, STRUCTURE, CONTENT, CREATE, MODIFY, ADD, DELETE, SEARCH, HEAD, ALL
        TABLE = decisionNode()
        TABLE.addKeyWords(["表", "表格"])
        TABLE.addExcludePoints([])
        TABLE.setSymbol("Table")

        BASE = decisionNode()
        BASE.addKeyWords(["数据库", "库"])
        BASE.addExcludePoints([])
        BASE.setSymbol("Base")

        DATA = decisionNode()
        DATA.addKeyWords(["数据"])
        # DATA.addExcludePoints([COLUMN, TABLE])  TODO : 逻辑问题...
        DATA.setSymbol("Data")

        COLUMN = decisionNode()
        COLUMN.addKeyWords(["列", "栏"])
        COLUMN.addExcludePoints([])
        COLUMN.setSymbol("Column")

        TYPE = decisionNode()
        TYPE.addKeyWords(["类型"])
        TYPE.addExcludePoints([])
        TYPE.setSymbol("Type")

        STRUCTURE = decisionNode()
        STRUCTURE.addKeyWords(["结构"])
        STRUCTURE.addExcludePoints([])
        STRUCTURE.setSymbol("Structure")

        CONTENT = decisionNode()
        CONTENT.addKeyWords(["内容"])
        CONTENT.addExcludePoints([])
        CONTENT.setSymbol("Content")

        ALL = decisionNode()
        ALL.addKeyWords(['所有', '全部'])
        ALL.setSymbol("All")

        CREATE = decisionNode()
        CREATE.addKeyWords(["建", "创建"])
        CREATE.addExcludePoints([])
        CREATE.addPoints([TABLE, BASE])
        CREATE.setSymbol("Create")

        MODIFY = decisionNode()
        MODIFY.addKeyWords(["修改", "改为", "改"])
        MODIFY.addExcludePoints([])
        MODIFY.addPoints([TABLE, DATA, TYPE])  # TODO 添加ALL 待开发
        MODIFY.setSymbol("Modify")

        ADD = decisionNode()
        ADD.addKeyWords(["加", "增加", "添加", "加入"])
        ADD.addExcludePoints([])
        ADD.addPoints([DATA, COLUMN])
        ADD.setSymbol("Add")

        DELETE = decisionNode()
        DELETE.addKeyWords(["删除", "删", "去除"])
        DELETE.addExcludePoints([])
        DELETE.addPoints([DATA, TABLE, BASE, ALL])
        DELETE.setSymbol("Delete")

        SEARCH = decisionNode()
        SEARCH.addKeyWords(["查询", "查", "查找", "搜索", "找", "搜"])
        SEARCH.addExcludePoints([])
        SEARCH.addPoints([CONTENT, STRUCTURE, BASE, TABLE, DATA, ALL])  # TODO SearchData DQL语句开发
        SEARCH.setSymbol("Search")

        HEAD = decisionNode()
        HEAD.addPoints([CREATE, MODIFY, ADD, DELETE, SEARCH])
        HEAD.addExcludePoints([])
        HEAD.setSymbol("<==HEAD==>")

    @staticmethod
    def do(KeyWords):
        global TABLE, BASE, DATA, COLUMN, TYPE, STRUCTURE, CONTENT, CREATE, MODIFY, ADD, DELETE, SEARCH, HEAD, ALL
        Flag = True
        Key = ""
        preKey = 0
        cur = HEAD
        print(" DEBUG ===== > @logic.do " + "KeyWords = " + str(KeyWords))
        while Flag:
            for each in cur.Point:
                print(" DEBUG ===== > @logic.do " + "each.symbol = " + str(each.symbol))
                print(" DEBUG ===== > @logic.do " + "KeyWord = " + str(each.KeyWord))
                if preKey == 0:
                    preKey = 1
                    for e in each.KeyWord:
                        if preKey == 1:
                            print(" DEBUG ===== > @logic.do " + "each.KeyWord.e = " + str(e))
                            if e in KeyWords:
                                cur = each
                                Key += each.symbol
                                print(" DEBUG ===== > @logic.do {} has been added KEY".format(str(each.symbol)))
                                preKey = 2
                preKey = 0

                if not each.hasPoint():
                    Flag = False
        print(" DEBUG ===== > @logic.do " + "runKey -> " + str(Key))
        return Key

    @staticmethod
    def KeyFix(key):
        keySet = participle(key, dic=resource.EN_KEY_DIC, MAX_LENGTH=10)
        print(" DEBUG ===== > " + "@logic.KeyFix keySet = " + str(keySet))

        def Splicing(arr):
            res = ""
            for each in arr:
                res += each
                print(" DEBUG ===== > @logic.KeyFix.Splicing 修正后的KEY -> {}".format(str(res)))
            return res

        Flag_1 = True
        run_level = len(keySet)
        cur_level = 1
        while Flag_1:
            if keySet[0] not in ["Add", "Delete", "Modify", "Search", "Create"]:
                if cur_level < run_level:
                    keySet[0], keySet[cur_level] = keySet[cur_level], keySet[0]
                    cur_level += 1
                else:
                    Flag_1 = False
            else:
                Flag_1 = False
        if "Delete" in keySet:
            if len(keySet) > 2:
                if "Data" in keySet and "Table" in keySet:
                    keySet.pop(keySet.index("Table"))
                    return Splicing(keySet)
            else:
                return Splicing(keySet)
        if "Add" in keySet:  # TODO 全部列添加数据 add column all data
            if len(keySet) > 2:
                if "Column" in keySet and "Data" in keySet:
                    keySet.pop(keySet.index("Column"))
                    return Splicing(keySet)
            else:
                return Splicing(keySet)
        if "Modify" in keySet:
            if len(keySet) > 2:
                if "Table" in keySet:
                    keySet.pop(keySet.index("Table"))
        if "Search" in keySet:
            if len(keySet) > 2:
                if "Table" in keySet:
                    keySet.pop(keySet.index("Table"))
                if "Content" in keySet:
                    keySet[keySet.index("Content")] = "Data"
                if "All" in keySet and "Data" in keySet:
                    if keySet.index("All") > keySet.index("Data"):
                        i1 = keySet.index("All")
                        i2 = keySet.index("Data")
                        keySet[i1], keySet[i2] = "Data", "All"
                        return Splicing(keySet)
                return Splicing(keySet)
            else:
                return Splicing(keySet)
        return Splicing(keySet)

        pass

    @staticmethod
    def getIndex(string):
        rule = re.compile("%.*?%")
        try:
            result = rule.findall(string)
            result2 = []
            for each in result:
                result2.append(each[1:-1])
        except:
            result2 = None
        return result2

    @staticmethod
    def dataType(line_end, userInputType=None):  # line_end: ',' | '' | ';'
        uIT = userInputType
        res = ""
        if uIT != None:
            if uIT == "tinyint" or uIT == "int":
                res += uIT
            elif "double" in uIT:
                if "(" in uIT:
                    res += uIT
                else:
                    Selected = input("double(?总长度,?小数点后保留的长度)")
                    SList = Selected.split(",")
                    res += "double({},{})".format(SList[0], SList[1])
            elif "char" in uIT:
                if "var" in uIT:
                    if "(" in uIT:
                        res += uIT
                    else:
                        Selected = input("varchar(?最大长度)")
                        res += "varchar({})".format(Selected)
                else:
                    if "(" in uIT:
                        res += uIT
                    else:
                        Selected = input("char(?长度)")
                        res += "char({})".format(Selected)
            else:
                print("date类型暂不支持 OR 键入错误")  # TODO 适配日期格式
        else:
            tip = """
            #11 tinyint(1字节) | #12 int(4字节) | #13 double(*,**)
            #21 char(*) | #22 varchar(*)
            #31 日期格式(暂不支持)
            """
            print(tip)
            item = input("请选择数据类型 -> ")
            if item == "11":
                res += "tinyint"
            if item == "12":
                res += "int"
            if item == "13":
                Selected = input("double(?总长度,?小数点后保留的长度)")
                SList = Selected.split(",")
                res += "double({},{})".format(SList[0], SList[1])
            if item == "21":
                Selected = input("char(?长度)")
                res += "char({})".format(Selected)
            if item == "22":
                Selected = input("varchar(?最大长度)")
                res += "varchar({})".format(Selected)
        res += line_end
        return res

    @staticmethod
    def match_WHERE(words: str):  # 生成SQL语句中WHERE后的数据集
        # TODO "为"->"="的智能转换
        # 把%demo%表%sex%=1,%age%>30的数据 修改为/删除/找出来 ······
        words = words.replace("，", ",")
        words = words.replace("。", ",")
        words = words.replace(".", ",")
        matchWords = words.split("的数据")[0]
        matchWords += ","
        KeyName = logic.getIndex(matchWords)
        tableName = KeyName[0]
        KeyName.pop(0)
        valueRE = re.compile("[(<)>=].*?,")
        resList = valueRE.findall(matchWords)
        result = []
        for columnName in KeyName:
            res = resList[KeyName.index(columnName)]
            resSet = []
            resSet.append(columnName)
            resSet.append(res[0])
            resSet.append(res[1:-1])
            result.append(resSet)
        return tableName, result


class produce:
    @staticmethod
    def getIndex(words):
        global KeyIndex, result
        result = ""
        KeyIndex = logic.getIndex(words)

    @staticmethod
    def CreateTable(words=None):
        global result, KeyIndex
        Flag2 = True
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
        else:
            tableName = input("请输入表名 -> ")
        result += "create table " + tableName + "("
        while Flag2:
            item01 = input("请输入字段名称 OR 字段%类型(若添加完毕键入0) -> ")
            if item01 != "0":
                if "%" in item01:
                    itemList = item01.split('%')
                    columnName = itemList[0]
                    columnType = itemList[1]
                else:
                    columnName = input("输入字段名 -> ")
                    columnType = None
                result += "\n\t" + columnName + " "
                result += logic.dataType(",", columnType)
            else:
                Flag2 = False
        result = result[:-1]
        result += "\n);"
        return result

    @staticmethod
    def CreateBase(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            dbName = KeyIndex[0]
        else:
            dbName = input("请输入数据库名称 -> ")
        result += "create database if not exists " + dbName + ";"
        return result

    @staticmethod
    def DeleteData(words=None):
        """
        :param words:
        :return:
        """
        global result, KeyIndex
        tableName, whereSet = logic.match_WHERE(words)
        # tip: 举例~删除%demo%表中%name%="张三"，%sex%=1的数据 [keyword: 删除~数据, =~的]
        result += "delete from {} where ".format(KeyIndex[0])
        KeyIndex.pop(0)
        for each in range(len(whereSet)):
            KeyIndex.pop(0)
        for each in whereSet:
            result += "{}{}{},".format(each[0], each[1], each[2])
        result = result[:-1]
        result += ";"
        return result

    @staticmethod
    def DeleteBase(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            dbName = KeyIndex[0]
        else:
            dbName = input("请输入数据库名称 -> ")
        result += "drop database if exists " + dbName + ";"
        return result

    @staticmethod
    def DeleteTable(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
        else:
            tableName = input("请输入表名称 -> ")
        result += "drop table if exists {};".format(tableName)
        return result

    @staticmethod
    def AddColumn(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
            columnName = KeyIndex[1]
        else:
            tableName = input("表名 -> ")
            columnName = input("新列名 -> ")
        result += "alter table {} add {} ".format(tableName, columnName)
        columnType = None
        result += logic.dataType(":", columnType)
        return result

    @staticmethod
    def AddData(words=None):
        """
        举例：
        ·给表%demo%全部列添加数据=数据1=数据2=...... [keyword: 全部列, 添加数据]
        ·给表%demo%的%列名1%%列名2%......添加数据=数据1=数据2[<可选项:>+=数据1=数据2]=...... [keyword: 列, 添加数据]  # TODO
        ·给表%demo%添加数据=数据1=数据2=+=数据1=数据2[<可选项:>+=数据1=数据2]=...... [keyword: 添加数据]
        :param words:
        :return:
        """
        global result, KeyIndex
        valueList = []
        columnList = []
        # TODO 逻辑标准化
        if "全部列" in words:
            result += "insert into {} values(".format(KeyIndex[0])
            valueList = words.split("=")[1:]
            for value in valueList:
                result += "{},".format(value)
            result = result[:-1]
            result += ");"
            return result
        elif "列" in words:
            result += "insert into {}(".format(KeyIndex[0])
            KeyIndex.pop(0)
            for eachColumn in KeyIndex:
                result += "{},".format(eachColumn)
            result = result[:-1]
            result += ") values"
            arr = words.split("+")
            for each in arr:
                arr_ = each.split("=")[1:]
                result += "("
                for value in arr_:
                    result += "{},".format(value)
                result = result[:-1]
                result += "),"
            result = result[:-1]
            result += ";"
            return result
        else:
            result += "insert into {} values".format(KeyIndex[0])
            arr = words.split("+")
            for each in arr:
                arr_ = each.split("=")[1:]
                result += "("
                for value in arr_:
                    result += "{},".format(value)
                result = result[:-1]
                result += "),"
            result = result[:-1]
            result += ";"
            return result

    @staticmethod
    def ModifyTable(words=None):
        global result, KeyIndex
        try:
            if len(KeyIndex) != 0:
                oldName = KeyIndex[0]
                newName = KeyIndex[1]
            else:
                oldName = input("原表名 -> ")
                newName = input("新表名 -> ")
        except:
            oldName = input("原表名 -> ")
            newName = input("新表名 -> ")
        result += "alter table {} rename to {};".format(oldName, newName)
        return result

    @staticmethod
    def ModifyType(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
            columnName = KeyIndex[1]
            newDataType = KeyIndex[2]
        else:
            tableName = input("请输入表名 -> ")
            columnName = input("请输入列名 -> ")
            newDataType = None
        result += "alter table {} modify {} {}".format(tableName, columnName, logic.dataType(";", newDataType))
        return result

    @staticmethod
    def ModifyData(words=None):
        """
        举例：
        ·%demo%表把%name%="张三"的数据%id%修改为30,%money%修改为200 [keyword: 把~的, =, 数据, 修改为] warning: 字符串加""
        ·%demo%表把%sex%=1,%age%>50的数据%id%修改为30,%money%修改为200
        :param words:
        :return:
        """
        global result, KeyIndex
        if "的" in words or "把" in words or "将" in words:  # TODO 类似这样的旧版本遗留内部逻辑限制还有 del
            if words[-1] != "，" or words[-1] != "。" or words[-1] != "," or words[-1] != ".":
                words += ","
            else:
                words = words[:-1] + ","
            tableName, whereSet = logic.match_WHERE(words)
            valueRule = re.compile("修改为.*?,")
            valueList = valueRule.findall(words)
            """modifyRule = re.compile("=.*?的")
            key1 = modifyRule.findall(words)[0][1:-1]"""
            result += "update {} set ".format(KeyIndex[0])
            KeyIndex.pop(0)
            """key2 = KeyName.pop(0)"""
            for each in range(len(whereSet)):
                KeyIndex.pop(0)
            for columnName in KeyIndex:
                valueList[0] = valueList[0].replace("修改为", "")
                result += "{}={},".format(columnName, valueList[0][:-1])
                valueList.pop(0)
            result = result[:-1]
            result += " where "
            for each in whereSet:
                result += "{}{}{},".format(each[0], each[1], each[2])
            result = result[:-1]
            result += ";"
            return result

    @staticmethod
    def SearchBase(words=None):
        global result, KeyIndex
        result += "show databases;"
        return result

    @staticmethod
    def SearchTable(words=None):
        global result, KeyIndex
        result += "show tables;"
        return result

    @staticmethod
    def SearchStructure(words=None):
        global result, KeyIndex
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
        else:
            tableName = input("请输入表名称 -> ")
        result += "desc " + tableName + ";"
        return result

    @staticmethod
    def SearchAllData(words=None):  # Data <==> Content
        global result, KeyIndex
        if len(KeyIndex) != 0:
            tableName = KeyIndex[0]
        else:
            tableName = input("请输入表名称 -> ")
        result += "select * from " + tableName + ";"
        return result

    @staticmethod
    def SearchData(words=None):  # Data <==> Content
        """
        举例：
        ·查询%demo%表中的数据
        ·查询%demo%表中%col1%%col2%...的数据[可选：并去除重复数据] [keyword: 并~重复]
        ·查询%demo%表中%列1%%列2%...的数据并为/给%列1%%列3%起别名/命名为=列X=列Y [keyword: 命名/别名, =]
        ·查询%demo%表中%age%<30，%sex%=1，列%col1%%col2%中的数据，给列%col2%命名为="COL" [keyword: %~=, %%]
        test: 查询%demo%表中%列1%%列2%...的数据并为%列1%起别名=列X TODO 列名出现“列”的处理
        test: 查询%demo%中%1%%2%...的数据并为%1%起别名=X并去除重复数据
        test:
        :param words:
        :return:
        """
        global result, KeyIndex
        words += ","
        strinfo = re.compile("[^(%<)(%>)(%=)][=]")
        words = strinfo.sub(",=", words)
        words = words.replace("并", ",")
        words = words.replace("，", ",")
        isWHERE = False
        whereSet = []
        equalNum = 0
        for each in KeyIndex:
            REtext = each + "%[(<)>=)]"
            whereRE = re.compile(REtext)
            res = whereRE.findall(words)
            if len(res) > 0:
                whereSet.append(each)
                if words[words.index(each) + 1 + len(each)] == "=":
                    equalNum += 1
        for each in whereSet:
            KeyIndex.pop(KeyIndex.index(each))
        if len(whereSet) > 0:
            isWHERE = True
        tableName = KeyIndex[0]
        KeyIndex.pop(0)
        if len(KeyIndex) == 0:
            KeyIndex.append(tableName)
            return produce.SearchAllData()
        result += "select "
        if "重复" in words:
            result += "distinct "
        otherNameNum = len(words.split("=")) - 1 - equalNum
        otherNameArr = []
        otherNameArr2 = []
        if otherNameNum > 0:
            otherNameNum *= -1
            otherNameArr = KeyIndex[otherNameNum:]
            KeyIndex = KeyIndex[:otherNameNum]
            RErule = re.compile("[^%=]=.*?,")
            otherNameArr2 = RErule.findall(words)
        columns = []
        otherNames = []
        for column in KeyIndex:
            result += "{},".format(column)
            columns.append(column)
            if column in otherNameArr:
                result = result[:-1]
                result += " as {}".format(otherNameArr2[otherNameArr.index(column)][1:-1])
                otherNames.append(otherNameArr2[otherNameArr.index(column)][1:-1])
                result += ","
        result = result[:-1]
        result += " from {};".format(tableName)
        if isWHERE:
            result = result[:-1]
            arr = ['命名', '取名', '别名']
            for each in arr:
                if each in words:
                    words = words.split(each)[0]
            for column in columns:
                index = "%{}%".format(column)
                words = words.replace(index, "")
            for otherName in otherNames:
                index = "%{}%".format(otherName)
                words = words.replace(index, "")
            tableName, whereSet = logic.match_WHERE(words)
            result += " where "
            for each in whereSet:
                result += "{}{}{},".format(each[0], each[1], each[2])
            result = result[:-1]
            result += ";"
        return result


def participle(words, dic=resource.CN_KEY_DIC, MAX_LENGTH=5):
    indexL = 0
    indexR = indexL + MAX_LENGTH
    curStr = ""
    resSet = []
    Flag = True

    def move(mode, length=1):  # mode=1 缩小1 mode=2 进位length mode=0 初始化 前向最大匹配算法
        nonlocal curStr, indexL, indexR
        if mode == 0:
            if indexR <= len(words):
                curStr = words[indexL:indexR]
            else:
                curStr = words
        elif mode == 1:
            if indexR > len(words):
                indexR = len(words)
            indexR -= length
            if indexR < indexL:
                indexL += 1
                indexR = indexL + MAX_LENGTH
            if indexL == len(words) - 1:
                if words[-1] in dic:
                    resSet.append(words[-1])
                return False
            curStr = words[indexL:indexR]
            return True
        elif mode == 2:
            indexL += length
            indexR = indexL + MAX_LENGTH
            if indexR > len(words):
                indexR = len(words)
            # if indexR-indexL > MAX_LENGTH:
            if indexL < len(words):
                curStr = words[indexL:indexR]
                return True
            elif indexL == len(words):
                if words[-1] in dic:
                    resSet.append(words[-1])
                return False

    move(0)
    while Flag:
        if curStr in dic:
            resSet.append(curStr)
            indexR = indexL + MAX_LENGTH
            Flag = move(2, len(curStr))
        else:
            Flag = move(1)
    resSet = list(set(resSet))
    return resSet


def main():
    tip = """
    欢迎使用MySQL Helper
    目前支持以下转换：
    创建操作：表, 库
    删除操作：表, 库, 某表中(某条件)的数据
    增加操作：表中添加列, 给表中的某(些）列/所有列添加数据
    修改操作：表名称, 表中(某条件)的数据, 表中某列的数据类型
    查询操作：所有表, 所有库, 表结构, 表中的内容(条件查询,起别名,排除重复值)

    DML DDL基础功能多数已支持, DQL正在开发......

    !!! 关键词用%引用起来, 涉及到值引用/值修改在值前加= !!!

    当前为测试版, DEBUG打印未关闭, 调用测试类中的main函数
    """
    print(tip)
    Test.main()


if __name__ == '__main__':
    print(__doc__)
    main()

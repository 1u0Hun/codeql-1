#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid
import tempfile
from utils.log       import log
from utils.option    import qlConfig
from utils.functions import execute

def checkQL(database):
    if not os.path.isdir(qlConfig("qlpath")):
        log.error("qlpath is not exists, check it at config/config.ini")
        return False

    # 生成临时的ql查询文件
    temp_path       = tempfile.TemporaryDirectory(dir=qlConfig("qlpath"))
    ql_filecontent  = '''import java\n\nselect "Hello World"\n'''
    ql_filepath     = os.path.join(temp_path.name, uuid.uuid4().hex + ".ql")
    with open(ql_filepath, 'w') as w:
        w.write(ql_filecontent)

    # 查询ql文件，判断文件查询结果是否正确
    content = execute(f"codeql query run -d {database} {ql_filepath}")
    if "Hello World" in content:
        return True
    else:
        log.error("qlpath is not correct, check the qlpack.yml file exists. For example ~/CodeQL/ql/java/ql/test/.")
        return False

def check_maven():
    content = execute("mvn -version")
    if "Apache Maven" not in content:
        log.error("Maven is not install or the Maven is not in environment path")
        return False
    return True

def check_codeql():
    content = execute("codeql --version")
    if "release" not in content.lower():
        log.error("codeql is not install or the codeql path is not in environment path")
        return False
    return True

def checkEnv():
    return check_codeql() and check_maven()

def checkDB(database):
    if not os.path.isdir(database):
        log.error("Database dir is not exists")
        return False
    dbyml = os.path.join(database, "codeql-database.yml")
    dbzip = os.path.join(database, "src.zip")

    if not os.path.isfile(dbyml) or not os.path.isfile(dbzip):
        log.error("Database format error")
        return False
    return True

if __name__ == "__main__":
    check_qlpath()

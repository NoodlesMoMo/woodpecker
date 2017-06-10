#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具函数
"""
import re
import os
import cgi
import time
import json
import gzip
import types
import urllib
import urllib2
import decimal
import logging
import random
import string
import zipfile
import StringIO
import urlparse
import datetime
import operator
import HTMLParser
import collections
from xml.etree import ElementTree


def gen_date_range(start_date, end_date):
    """
    生成日期区间，开始-结束日期间的每一天
    注意: 结果是生成器
    :param datetime.datetime stat_date: 开始日期
    :param datetime.datetime end_date: 截止日期
    :return generator: 生成器
    """
    delta = (end_date - start_date).days
    for n in range(delta + 1):
        yield start_date + datetime.timedelta(n)


def short_name(name, length=16, suffix="..."):
    """
    缩减名称
    :param name:
    :param length:
    :param suffix:
    :return:
    """
    name = name.decode("utf-8")
    cur_len, result = 0, ""
    for i in name:
        if cur_len >= length:
            result += suffix
            break
        char_len = len(i.encode("utf-8"))
        if char_len > 2:
            char_len = 2
        cur_len += char_len
        result += i
    return result.encode("utf-8")


def time_min(dtime, time_format="%Y-%m-%d %H:%M"):
    """
    时间精确
    :param datetime.datetime dtime: datetime.datetime对象
    :param str time_format: 时间格式串
    :return: 默认精确到分
    """
    if isinstance(dtime, str):
        if len(dtime) != 19:
            return dtime
        return dtime[:-3]
    return dtime.strftime(time_format)


def strptime(str_dtime, time_format="%Y-%m-%d"):
    """
    字符串转化为 datetime for < 2.6
    :param str str_dtime: 字符串格式的时间
    :param str time_format: 时间格式串
    :return: datetime.datetime
    """
    time_stamp = time.mktime(time.strptime(str_dtime, time_format))
    return datetime.datetime.fromtimestamp(time_stamp)


def strftime(dtime, time_format="%Y-%m-%d"):
    """
    格式化时间
    :param datetime.datetime dtime: 时间对象
    :param str time_format: 时间格式串
    :return: 字符串时间
    """
    return datetime.datetime.strftime(dtime, time_format)


def time_start(dtime, dtype):
    """
    时间取整
    :param datetime.datetime dtime: datetime.datetime对象
    :param str dtype: 取整类型 hour day week month
    :return: 取整后的时间对象
    """
    if dtype == "hour":
        delta = datetime.timedelta(minutes=dtime.minute,
                                   seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    elif dtype == "day":
        delta = datetime.timedelta(hours=dtime.hour, minutes=dtime.minute,
                                   seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    elif dtype == "week":
        delta = datetime.timedelta(days=dtime.weekday(), hours=dtime.hour,
                                   minutes=dtime.minute, seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    elif dtype == "month":
        delta = datetime.timedelta(days=dtime.day - 1, hours=dtime.hour,
                                   minutes=dtime.minute, seconds=dtime.second,
                                   microseconds=dtime.microsecond)
    else:
        raise Exception("wrong type %s" % dtype)
    return dtime - delta


def time_prev(dtime, dtype):
    """
    取上一个‘整’时间
    :param datetime.datetime dtime: datetime.datetime对象
    :param str dtype: 取整类型 hour day week month
    """
    dtime = time_start(dtime, dtype)
    return time_start(dtime - datetime.timedelta(seconds=1), dtype)


def time_next(dtime, dtype):
    """
    取下一个‘整’时间
    :param datetime.datetime dtime: datetime.datetime对象
    :param str dtype: 取整类型 hour day week month
    :return: 下一个整时间
    """
    if dtype == "hour":
        dtime += datetime.timedelta(hours=1)
    elif dtype == "day":
        dtime += datetime.timedelta(days=1)
    elif dtype == "week":
        dtime += datetime.timedelta(days=7)
    elif dtype == "month":
        year = dtime.year + 1 if dtime.month == 12 else dtime.year
        month = 1 if dtime.month == 12 else dtime.month + 1
        dtime = datetime.datetime(year, month, 1)
    else:
        raise Exception("wrong type %s" % dtype)
    return time_start(dtime, dtype)


def time_delta(dtime, days=0, hours=0, seconds=0, time_format="%Y-%m-%d"):
    """
    给指定时间加上增量
    :param datetime.datetime dtime: datetime.datetime对象
    :param int days: 天数
    :param int hours: 小时
    :param int seconds: 秒
    :return: 加上增量后的时间对象
    """
    if isinstance(dtime, str):
        dtime = datetime.datetime.strptime(dtime, time_format)
    return dtime + datetime.timedelta(days=days, hours=hours, seconds=seconds)


def convert_to_timestamp(date_time):
    """
    将日期转换成时间戳
    :param datetime.datetime date_time: datetime.datetime 对象
    :return:
    """
    time_tuple = date_time.timetuple()
    timestamp = time.mktime(time_tuple[:9])
    return timestamp


def time_diff(time1, time2, dtype):
    """
    计算时间差
    :param datetime.datetime time1: 起始时间
    :param datetime.datetime time2: 结束时间
    :return: 分钟
    """
    date_dict = {
        'second': 1,
        'minite': 60,
        'hour': 60 * 60
    }
    if dtype in date_dict.keys():
        diff = time2 - time1
        actual_sec = diff.days * 24 * 3600 + diff.seconds
        return actual_sec / date_dict.get(dtype, 1)
    else:
        diff = time2 - time1
        return diff.days if diff.days > 0 else 0


def gzip_compress(data):
    """
    gzip压缩
    :param data: 带压缩的数据
    :return: 压缩后的数据
    """
    zbuf = StringIO.StringIO()
    zfile = gzip.GzipFile(mode="wb", compresslevel=1, fileobj=zbuf)
    zfile.write(data)
    zfile.close()
    return zbuf.getvalue()


def gzip_decompress(data):
    """
    gzip解压
    :param data: 带解压的数据
    :return: 解压后的数据
    """
    zbuf = StringIO.StringIO(data)
    zfile = gzip.GzipFile(fileobj=zbuf)
    data = zfile.read()
    zfile.close()
    return data


def unzip_winfile(zip_fname, dir_path=''):
    """
    解压windows打包的文件
    :param str zip_fname: 文件名称
    :param str dir_path: 文件路径
    """
    dir_path = dir_path or os.path.dirname(zip_fname)
    file = zipfile.ZipFile(zip_fname, "r")
    for name in file.namelist():
        try:
            tmp_name = name.decode("gbk").encode("utf8")
        except UnicodeDecodeError:
            logging.info("UnicodeDecodeError")
            tmp_name = name.encode("utf8")
        except UnicodeEncodeError:
            logging.info("UnicodeEncodeError")
            tmp_name = name.encode("utf8")
        utf8name = os.path.join(dir_path, tmp_name)
        pathname = os.path.dirname(utf8name)
        if pathname and not os.path.exists(pathname):
            os.makedirs(pathname)
        data = file.read(name)
        if not os.path.exists(utf8name):
            fo = open(utf8name, "w")
            fo.write(data)
            fo.close
    file.close()


def url_add_params(url, escape=True, **params):
    """
    往给定url中添加参数
    :param url: 给定的URL
    :param escape: 是否escape
    :param params: 待添加的参数
    :return: 添加参数后的url
    """
    pr = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(pr.query))
    query.update(params)
    prlist = list(pr)
    if escape:
        prlist[4] = urllib.urlencode(query)
    else:
        prlist[4] = "&".join(["%s=%s" % (k, v) for k, v in query.items()])
    return urlparse.ParseResult(*prlist).geturl()


def write2log(basedir, logtype, *row):
    """
    按天记录日志
    :param basedir: 本目录
    :param logtype: 日志类型
    :param row: 日志内容
    :return: None
    """
    logtype = logtype.lower()
    file_dir = os.path.join(basedir, logtype + "_log")
    os.umask(0)
    if not os.path.lexists(file_dir):
        os.makedirs(file_dir, 0777)
    now = datetime.datetime.now()
    file_name = os.path.join(file_dir, "%s.log" % now.strftime("%Y%m%d"))
    try:
        fd = os.open(file_name, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0777)
        row = [i.encode("utf8") if isinstance(i, unicode) else str(i) for i in row]
        row.insert(0, now.strftime("[%Y-%m-%d %H:%M:%S]"))
        row = "%s\n" % "\t".join(row)
        os.write(fd, row)
    except IOError, e:
        logging.error("fail to write %s log: %s\n", logtype, str(e),
                      exc_info=True)
    finally:
        if fd:
            os.close(fd)


def force_utf8(data):
    """
    数据转换为utf8
    :param data: 待转换的数据
    :param :return: utf8编码
    """
    if isinstance(data, unicode):
        return data.encode("utf-8")
    elif isinstance(data, list):
        return [force_utf8(i) for i in data]
    elif isinstance(data, dict):
        return {force_utf8(i): force_utf8(data[i]) for i in data}
    return data


def del_dict_key(dict_data, key_list):
    """
    清空指定键值
    :param obj: 清空的字典
    :param key_list: 要删除的key列表
    :param :return: 清理后的dict
    """
    for key in key_list:
        if key in dict_data:
            del dict_data[key]
    return dict_data


def sjoin_list(src_list, joiner=","):
    """
    通过指定分隔符连接列表
    :param list src_list: 待连接的列表
    :param str joiner: 连接的字符串
    :return: 连接后的字符串
    """
    return joiner.join([str(i) for i in src_list])


def get_local_ip(ifname='eth0'):
    """
    获取内网IP地址

    :param ifname:
    :return:
    """
    import socket, fcntl, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret


def escape_html(data):
    """
    转义html
    """
    return cgi.escape(data)


def unescape_html(data):
    """
    反转义html
    """
    if not isinstance(data, unicode):
        data = data.decode("utf-8")
    parser = HTMLParser.HTMLParser()
    return parser.unescape(data).encode("utf-8")


def convert(num, meta):
    """
    十进制与其它进制间的转换
    :param num: 十进制数字
    :param meta: 其它进制e.g: "01"--> 二进制
    """
    result, base = "", len(meta)
    while 1:
        b = num % base
        result = meta[b] + result
        num = num / base
        if num <= 0:
            break
    return result


def json_default(obj):
    """
    实现json包对datetime的处理
    """
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        raise TypeError("%r is not JSON serializable" % obj)


def send_request(url, params=None, method="GET", timeout=5):
    """
    发送请求
    :param str url: 请求地址
    :param dict params: 请求参数
    :param str method: 方法
    """
    try:
        if method == "GET":
            if params:
                url = "%s?%s" % (url, urllib.urlencode(params))
                logging.debug("request_url: %s", url)
            resp = urllib2.urlopen(url, timeout=timeout)
        elif method == "POST":
            logging.debug("request url: %s, param: %s", url, params)
            resp = urllib2.urlopen(url, data=urllib.urlencode(params), timeout=timeout)
        res = resp.read()
        resp.close()
        return force_utf8(json.loads(res))
    except Exception, e:
        logging.error("send request error: url: %s error:%s", url, str(e), exc_info=True)
        return None


def is_valid_phone(phone):
    """
    是否是有效的手机号
    :param string phone: 手机号
    """
    if phone.isdigit() and len(phone) == 11:
        return True
    return False


def is_valid_call_number(phone):
    """
    简单是否是有效的手机号或座机号
    """
    p = re.compile(r'^(?:\+86)?(1\d{10})$|^(?:\+86)?(0\d{2,3})(-)?\d{7,8}$')
    phone_match = p.match(phone)
    if phone_match:
        return True
    return False


def is_valid_email(email):
    """
    是否是有效的邮箱地址
    :param str email: 电子邮箱
    """
    if re.match(r"^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$", email) != None:
        return True
    else:
        return False


def is_chinese(uchar):
    """
    判断一个unicode是否是汉字
    """
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """
    判断一个unicode是否是数字
    """
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """
    判断一个unicode是否是英文字母
    """
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or \
            (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """
    判断是否非汉字，数字和英文字符
    """
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def calculate_page(count, count_per_page):
    """
    根据总数量和每页显示数量，返回总共有多少页
    :param count: 总数量
    :param count_per_page: 每页数量
    :return: 返回总共多少页
    """
    return (count + count_per_page - 1) / count_per_page


def get_id_str(id_list):
    """
    将数据元素合并成字符串
    :param id_list:
    :return:
    """
    id_list_buffer = set(id_list)
    return ",".join([str(i) for i in id_list_buffer if i])


def get_id_list(obj_list, id_key="id"):
    """
    获取某个字段列表
    :param obj_list: 数据列表
    :param id_key: 指定标识
    :return:
    """
    return [i[id_key] for i in obj_list]


def get_id_str_from_list(obj_list, id_key="id"):
    """
    获取元素合并字符串
    :param list obj_list: 对象列表
    :param str id_key: 字段key
    :return:
    """
    id_list = [i[id_key] for i in obj_list]
    return get_id_str(id_list)


def sprint(string_format, *args):
    """
    该函数能正常的处理utf和unicode字符串格式化的问题
    :param strign_format: "%s汉字"
    :return: utf8 string
    """
    if isinstance(string_format, types.UnicodeType):
        string_format = string_format.encode("utf8")

    l = list(args) if args else []

    for index, value in enumerate(l):
        if isinstance(value, types.UnicodeType):
            l[index] = value.encode("utf8")

    return operator.mod(string_format, *l)


class _JsonDumps(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "json_dumps"):
            return o.json_dumps()

        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, datetime.time):
            return o.strftime("%H:%M:%S")

        if isinstance(o, datetime.timedelta):
            return o.total_seconds()

        if isinstance(o, float):
            return decimal.Decimal(o)

        if isinstance(o, decimal.Decimal):
            return decimal.Decimal(o)

        if isinstance(o, types.UnicodeType):
            return o.encode("utf8", "ignore")

        if isinstance(o, collections.Set):
            return list(o)

        if isinstance(o, collections.Sequence):
            return list(o)

        return json.JSONEncoder.default(self, o)


def json_dumps(obj, **kwargs):
    """
    return utf8 string
    """
    _kwargs = dict(
        check_circular=True,
        indent=4,
        cls=_JsonDumps,
        encoding="utf-8",
        sort_keys=True,
        ensure_ascii=False)

    if kwargs:
        _kwargs.update(kwargs)

    x = json.dumps(obj, **_kwargs)
    if isinstance(x, types.UnicodeType):
        x = x.encode("utf8")

    return x


class DictObject(object):
    """
    把dict转换成object的访问方式
    """

    def __init__(self, d):
        self.__dict__.update(d)
        pass

    def __str__(self):
        s = json_dumps(self.__dict__)
        return s

    def json_dumps(self):
        return self.__dict__

    def __repr__(self):
        return self.__str__()


def json_unicode_string_hook(d):
    """
    对于任何的unicode string都转换成 utf字符串
    """
    new_d = {}
    for key, value in d.iteritems():
        if isinstance(key, types.UnicodeType):
            new_key = key.encode("utf8")
        else:
            new_key = key

        if isinstance(value, types.UnicodeType):
            new_value = value.encode("utf8")
        else:
            new_value = value
        new_d[new_key] = new_value

    return DictObject(new_d)


def json_loads(obj, **kwargs):
    """
    json加载
    :param obj:
    :param kwargs:
    :return:
    """
    _kwargs = dict(encoding="utf-8",
                   object_hook=json_unicode_string_hook)
    _kwargs.update(kwargs)
    x = json.loads(obj, **_kwargs)
    return x


def get_file_working_dir():
    """
    获取调用该函数的文件所在的目录
    :return: 绝对路径
    """
    import inspect
    frame = inspect.currentframe().f_back
    file_path = os.path.abspath(frame.f_globals["__file__"])
    working_dir = os.path.dirname(file_path)
    return working_dir


def load_env(file_name):
    """
    :param str file_name: 文件路径
    :return: 配置字典
    """
    env_dict = {}
    try:
        with open(file_name) as fd:
            for kv in fd:
                kv = kv.replace("\n", "")
                arr_kv = kv.split("=")
                env_dict[arr_kv[0]] = arr_kv[1]
    except:
        pass
    return env_dict


def get_date_range(_date=None):
    """
    返回一个给定日期的起至时间,例如"2001-01-01 20:00:00",
    返回 date("2010-01-01"),date("2010-01-02")
    :return: date, next_date
    """
    if not _date:
        _date = datetime.datetime.now()

    if isinstance(_date, types.StringTypes):
        date = datetime.datetime.strptime(_date, "%Y-%m-%d")
    elif isinstance(_date, datetime.datetime):
        date = _date.date()
    elif isinstance(_date, datetime.date):
        date = _date
    else:
        raise TypeError("invalid type of argument _date")

    deadline = date + datetime.timedelta(days=1)
    return date, deadline


def replace_phone_number(phone, start, end, repl="*"):
    """
    手机号替换
    :param int start: 开始替换位置
    :param int end:结束位置
    :param string repl: 替换
    :return: 186****7206
    """
    return phone[:start - 1] + repl * (end - start + 1) + phone[end:]


def fen2yuan(amount):
    """
    转换金额分成元
    :param amount: 转换金额
    :return float: 元
    """
    return float(amount) / 100


def convert_fen_to_yuan(fen):
    """
    转换分到元, 保留两位小数
    :param int fen.
    :return str. e.g 1.99
    """
    fen = decimal.Decimal(str(fen))
    a = fen / decimal.Decimal("100")
    return "%0.2f" % a


class Price(long):
    """
    用于表示价格
    # 初始化
    price = Price.init_yuan("66.09")
    price = Price.init_fen(6666)
    price.yuan
    price.fen
    # 加减, 乘除
    price = Price.init_yuan(100) + Price.init_fen(10)
    price = Price.init_yuan(100) / 4
    """

    @classmethod
    def init_yuan(cls, yuan):
        """
        元初始化
        """
        if isinstance(yuan, types.StringTypes):
            yuan = decimal.Decimal(yuan)
            fen = int(100 * yuan)
            return cls(fen)

        elif isinstance(yuan, (types.IntType, types.LongType)):
            return cls(yuan * 100)

        elif isinstance(yuan, types.FloatType):
            fen = decimal.Decimal(str(yuan)) * 100
            return cls(int(fen))
        elif isinstance(yuan, decimal.Decimal):
            return cls(int(100 * yuan))
        else:
            raise TypeError("unknown yuan type: %s", type(yuan))

    @classmethod
    def init_fen(cls, fen):
        """
        分初始化
        """
        fen = int(fen)
        return cls(fen)

    @property
    def yuan(self):
        return decimal.Decimal(self) / decimal.Decimal("100")

    @property
    def fen(self):
        return self

    def __add__(self, other):
        assert isinstance(other, Price)
        s = int(self) + int(other)
        return Price.init_fen(s)

    def __iadd__(self, other):
        assert isinstance(other, Price)
        return self.__add__(other)

    def __sub__(self, other):
        assert isinstance(other, Price)
        s = int(self) - int(other)
        return Price.init_fen(s)

    def __isub__(self, other):
        assert isinstance(other, Price)
        return self.__sub__(other)

    def __mul__(self, other):
        other = decimal.Decimal(str(other))
        s = int(self) * other
        return Price.init_fen(int(s))

    def __imul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        other = decimal.Decimal(str(other))
        s = int(self) / other
        return Price.init_fen(int(s))

    def __idiv__(self, other):
        return self.__div__(other)


class DefaultValue(object):
    pass


def list_first(cmp_fn, lst, default=DefaultValue):
    hit = filter(cmp_fn, lst)

    if len(hit) > 0:
        return hit[0]

    if default is DefaultValue:
        raise IndexError('find value failure')

    return default


def gen_random_code(length, with_letters=False):
    """
    生成指定长度的随即码
    :param int length: 长度
    :param bool with_letters: 是否包含字母
    :return: str_code
    """
    digits = string.digits
    if with_letters:
        digits += string.uppercase
        digits = re.sub(r"[0,I,1,D,G,J,M,R,T]", "", digits)
    return "".join(random.sample(digits, length))


def yuan2fen(number):
    """
    从元转至分
    :param number number: 数值
    :return: int
    """
    return number * 100


def fen2yuan_str(number, ndigits=2):
    """
    分转元, 返回 str
    :param number number: 数值
    :param int ndigits: 保留小数位
    :return: str
    """
    smaller = decimal.Decimal(number) / 100
    f = "%df" % ndigits
    return ("{0:.%s}" % f).format(smaller)


def kg2k(number):
    """
    千克到克
    :param number number: 数值
    :return: int
    """
    return number * 1000


def k2kg(number):
    """
    克到千克
    :param number number: 数值
    :return: float
    """
    return float(number) / 1000


def k2kg_str(number, ndigits=2):
    """
    克到千克, 返回 str
    :param number number: 数值
    :param int ndigits: 保留小数位
    :return: str
    """
    smaller = decimal.Decimal(number) / 1000
    f = "%df" % ndigits
    return ("{0:.%s}" % f).format(smaller)

def integerize_dict_key(any_dict):
    """
    将字典key转换成int类型
    :param dict any_dict: 任何字典
    :return: any_dict
    """
    if not isinstance(any_dict, dict):
        return any_dict

    return {int(k): v for k, v in any_dict.items()}


def parse_xml(node):
    """
    解析XML数据
    :param str node: 待解析的XML文本, 或者结点
    :return: 解析后的JSON数据
    """
    if not isinstance(node, ElementTree.Element):
        node = ElementTree.fromstring(node)

    children = node.getchildren()
    if not children:
        return force_utf8(node.text)
    else:
        return {force_utf8(i.tag): force_utf8(parse_xml(i))
                for i in children}


if __name__ == '__main__':
    assert fen2yuan_str(12345) == "123.45"
    assert fen2yuan_str(12345, 3) == "123.450"

    assert k2kg_str(12345) == "12.34"
    assert k2kg_str(12345, 4) == "12.3450"

    assert kg2k(1) == 1 * 1000
    assert kg2k(1.234) == 1.234 * 1000

    assert k2kg(1234) == 1.234
    assert k2kg(1000) == 1

    import types
    start_date = datetime.datetime.now().replace(year=2016, month=10, day=1)
    end_date = start_date.replace(month=11, day=5)

    drange = gen_date_range(start_date, end_date)
    assert type(drange) == types.GeneratorType

    drange_list = list(drange)
    assert len(drange_list) == 36 # start month 31, end month 5
    assert drange_list[0] == start_date
    assert drange_list[-1] == end_date

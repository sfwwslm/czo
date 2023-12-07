import datetime
import random
import string


class Faker:
    """伪造常用数据"""

    @property
    def __areaCodeDict(self) -> dict:
        """区域文件地址"""
        from .config.area import dataDict
        return dataDict

    def __areaCode(self, dict) -> int:
        """功能：随机生产一个区域码"""
        code_list = list(dict.keys())
        length = len(code_list) - 1
        i = random.randint(0, length)
        return code_list[i]

    @property
    def __birthDay(self) -> str:
        """功能：随机生成1930年之后的出生日期"""
        d1 = datetime.datetime.strptime(
            '1930-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.now()
        delta = d2 - d1
        dys = delta.days
        i = random.randint(0, dys)
        dta = datetime.timedelta(days=i)
        bhday = d1 + dta
        return bhday.strftime('%Y%m%d')

    @property
    def __ordrNum(self) -> tuple[str, int]:
        """功能：随机生成3位序列号"""
        od_num = random.randint(100, 999)  # 随机生成100到999之间的位为数据
        sex = od_num % 2
        return str(od_num), sex

    def __check(self, id_num) -> str:
        """功能：生成校验码"""
        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        check_code = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8',
                      '5': '7', '6': '6', '7': '5', '8': '5', '9': '3', '10': '2'}  # 校验码映射
        for i in range(len(id_num)):
            count = count + int(id_num[i]) * weight[i]
        return check_code[str(count % 11)]  # 算出校验码

    @property
    def info(self) -> dict:
        """生成随机数据，用于测试目的。
        
        `info` 是一个属性，用于生成用于测试目的的随机数据。

        返回值:
            包含随机生成的个人信息的字典，例如姓名、性别、年龄、职业等。
        """
        area_code_dt = self.__areaCodeDict  # 调用生成字典
        area_cd = self.__areaCode(area_code_dt)  # 生成区域码
        area_cd_name = area_code_dt[area_cd]  # 获取区域名称
        birth_dy = self.__birthDay  # 生成出生日期
        (ordNum, sex) = self.__ordrNum  # 生成顺序号和性别
        check_code = self.__check((area_cd + birth_dy + ordNum))  # 生产校验码
        id_card = area_cd + birth_dy + ordNum + check_code  # 拼装身份证号

        gender = '女' if int(id_card[16]) % 2 == 0 else '男'
        # 计算年龄
        birth_date = datetime.datetime.strptime(birth_dy, "%Y%m%d")
        current_date = datetime.datetime.now()
        age = current_date.year - birth_date.year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))

        return {
            'name': self.name, 'gender': gender, 'age': age, 'occupation': self.occupation,
            'ethnicities': self.ethnicities, 'school': self.school, 'religion': self.religion,
            'phone_number': self.phone_number, 'home_phone_number': self.home_phone_number,
            'address': area_cd_name, 'id_card': id_card, 'MAC': self.mac_address,
            'passport_number': self.passport_number, 'latitude': self.latitude, 'longitude': self.longitude,
            'ipv4': self.ipv4, 'msg': self.warning
        }

    @property
    def passport_number(self) -> str:
        """护照号"""
        return 'D' + ''.join(random.choices('0123456789', k=8))

    @property
    def gender(self) -> str:
        """性别

        如果要生成和身份证号一致的数据，应该使用：:func:`Faker().info`。

        """
        return random.choice(["男", "女"])

    @property
    def address(self) -> str:
        """地址信息

        如果要生成和身份证号一致的数据，应该使用：:func:`Faker().info`。

        """
        return self.info['address']

    @property
    def id_area(self) -> str:
        """身份证号"""
        return self.info['id_card']

    @property
    def mac_address(self) -> str:
        """生成MAC地址"""
        mac_parts = [random.randint(0x00, 0xff)
                     for _ in range(6)]  # 生成六个随机的十六进制数
        # 使用冒号分隔，也可以使用 '-' 或其他分隔符
        mac_address = ':'.join(['%02x' % part for part in mac_parts])
        return mac_address

    @property
    def phone_number(self) -> int:
        """生成手机号"""
        prefix = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189'])
        # 随机生成电话号的后缀
        suffix = ''.join(random.choice(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for _ in range(8))
        # 将前缀和后缀组合起来，生成电话号
        return int(prefix + suffix)

    @property
    def home_phone_number(self) -> str:
        """生成座机号码"""
        return f"057{random.choice(string.digits)}-{random.choice(string.digits[1:])}{''.join(random.choice(string.digits) for _ in range(7))}"

    @property
    def latitude(self) -> float:
        """纬度"""
        return round(random.uniform(-90, 90), 6)

    @property
    def longitude(self) -> float:
        """经度"""
        return round(random.uniform(-180, 180), 6)

    @property
    def warning(self) -> str:
        return "数据仅用于测试目的！"

    @property
    def occupation(self) -> str:
        """职业"""
        return random.choice(['教师', '工人', '记者', '演员', '作曲家', '架构师', '营养师', '鼓手', '厨师',
                              '医生', '护士', '司机', '军人', '律师', '商人', '会 计', '店员', '出纳员',
                              '作家', '导游', '警察', '歌手', '画家', '裁缝', '翻译官', '法官', '保安',
                              '花匠', '服务员', '清洁工', '建筑师', '理发师', '采购员', '消防员', '机修工',
                              '推销员', '魔术师', '模特', '邮递员', '售货员', '救生员', '运动员', '工程师',
                              '飞行员', '管理员', '机械师', '经纪人', '歌唱家', '审计员', '漫画家', '园艺师',
                              '科学家', '主持人', '调酒师', '化妆师', '艺术家', '糕点师', '甜品师', '外交官',
                              '舞蹈家', '箭术', '溜冰', '弹钢琴', '古筝手', '钢琴家', '设计师', 'CEO',
                              '机 长', '记者', '赛车手', '教练', '兽医', '特警', '按摩'])

    @property
    def ipv4(self) -> str:
        """生成随机的欧洲国家 IP 地址"""
        europe_ip_prefixes = [
            "1", "2", "5", "25", "31",
            "37", "46", "62", "77", "78",
            "79", "80", "81", "82", "83",
            "84", "85", "86", "87", "88",
            "89", "90", "91", "92", "93",
            "94", "95", "109", "176", "178",
            "185", "188", "193", "194", "195",
            "212", "213", "217"
        ]
        random_ip = random.choice(europe_ip_prefixes)
        for _ in range(3):
            random_ip += f".{random.randint(0, 255)}"
        return random_ip

    @property
    def school(self) -> str:
        """随机的学校名称"""
        return random.choice([
            '麻省理工学院', '牛津大学', '斯坦福大学', '剑桥大学', '哈佛大学', '加州理工学院',
            '帝国理工学院', '苏黎世联邦理工大学', '伦敦大学学院', '芝加哥大学'
        ])

    @property
    def name(self) -> str:
        """随机的姓名"""
        surnames: list[str] = [
            "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨",
            "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜",
            "戚", "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘", "葛", "奚", "范", "彭", "郎",
            "鲁", "韦", "昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳", "酆", "鲍", "史", "唐",
            "费", "廉", "岑", "薛", "雷", "贺", "倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常",
            "乐", "于", "时", "傅", "皮", "卞", "齐", "康", "伍", "余", "元", "卜", "顾", "孟", "平", "黄",
            "郭"
        ]

        # 常见的名字
        given_names: list[str] = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊',
                                  '军', '洋', '勇', '艳', '杰', '娟', '博', '文', '涛', '慧', '明',
                                  '建国', '丽丽'
                                  ]

        # 随机选择姓氏和名字
        surname: str = random.choice(surnames)
        given_name: str = random.choice(given_names)

        # 组合为完整的名字
        full_name: str = surname + given_name

        return full_name

    @property
    def religion(self) -> str:
        """宗教信仰"""
        return random.choice(["道教", "佛教", "伊斯兰教", '基督教', '印度教', '犹太教', '婆罗门教', '耆那教'])

    @property
    def age(self) -> int:
        """年龄

        如果要生成和身份证号一致的数据，应该使用：:func:`Faker().info`。

        """
        return random.randint(16, 101)

    @property
    def ethnicities(self) -> int:
        """民族"""
        chinese_ethnicities = [
            "汉族", "蒙古族", "回族", "藏族", "维吾尔族", "苗族", "彝族", "壮族", "布依族", "朝鲜族",
            "满族", "侗族", "瑶族", "白族", "土家族", "哈尼族", "哈萨克族", "傣族", "黎族", "傈僳族",
            "佤族", "畲族", "高山族", "拉祜族", "水族", "东乡族", "纳西族", "景颇族", "柯尔克孜族",
            "土族", "达斡尔族", "仫佬族", "羌族", "布朗族", "撒拉族", "毛南族", "仡佬族", "锡伯族",
            "阿昌族", "普米族", "塔吉克族", "怒族", "乌孜别克族", "俄罗斯族", "鄂温克族", "崩龙族",
            "保安族", "裕固族", "京族", "塔塔尔族", "独龙族", "鄂伦春族", "赫哲族", "门巴族", "珞巴族",
            "基诺族"
        ]
        return random.choice(chinese_ethnicities)

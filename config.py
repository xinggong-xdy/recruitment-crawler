# 数据库配置
DB_CONFIG = {
    'host': 'localhost',      # MySQL 主机地址
    'user': 'root',           # MySQL 用户名
    'password': 'your_password',  # MySQL 密码
    'database': 'recruitment_db',  # 数据库名称
    'port': 3306
}

# 爬虫配置
CRAWLER_CONFIG = {
    'timeout': 10,
    'retry_count': 3,
    'delay': 1,  # 请求延迟（秒）
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 目标学校配置
UNIVERSITIES = {
    'zhongbei': {
        'name': '中北大学',
        'url': 'https://zb.nuc.edu.cn/',
        'recruitment_url': 'https://zb.nuc.edu.cn/zs/'
    },
    'shanxi_normal': {
        'name': '山西师范大学',
        'url': 'https://www.sxnu.edu.cn/',
        'recruitment_url': 'https://www.sxnu.edu.cn/zs/'
    },
    'northeast': {
        'name': '东北大学',
        'url': 'https://www.neu.edu.cn/',
        'recruitment_url': 'https://www.neu.edu.cn/zs/'
    },
    'hebei_industrial': {
        'name': '河北工业大学',
        'url': 'https://www.hebut.edu.cn/',
        'recruitment_url': 'https://www.hebut.edu.cn/zs/'
    },
    'shanghai_finance': {
        'name': '上海财经大学',
        'url': 'https://www.sufe.edu.cn/',
        'recruitment_url': 'https://www.sufe.edu.cn/zs/'
    }
}

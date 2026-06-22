import requests
from bs4 import BeautifulSoup
import time
from utils.logger import logger
from config import CRAWLER_CONFIG


class BaseCrawler:
    """爬虫基类"""
    
    def __init__(self, university_name, base_url):
        self.university_name = university_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': CRAWLER_CONFIG['user_agent']
        })
        self.timeout = CRAWLER_CONFIG['timeout']
        self.retry_count = CRAWLER_CONFIG['retry_count']
    
    def fetch_page(self, url, params=None):
        """获取页面内容"""
        for attempt in range(self.retry_count):
            try:
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=self.timeout
                )
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    logger.info(f"成功获取页面: {url}")
                    return response.text
                else:
                    logger.warning(f"页面状态码异常: {response.status_code}")
            except requests.RequestException as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.retry_count}): {e}")
                time.sleep(CRAWLER_CONFIG['delay'])
        
        logger.error(f"无法获取页面: {url}")
        return None
    
    def parse_html(self, html_content):
        """解析HTML内容"""
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            return soup
        except Exception as e:
            logger.error(f"HTML解析失败: {e}")
            return None
    
    def crawl(self):
        """爬虫主方法（子类需重写）"""
        raise NotImplementedError("子类必须实现 crawl 方法")

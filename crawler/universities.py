import re
import json
from datetime import datetime
from crawler.base_crawler import BaseCrawler
from utils.logger import logger


class ZhongbeiUniversityCrawler(BaseCrawler):
    """中北大学爬虫"""
    
    def crawl(self):
        """爬取中北大学招生计划"""
        logger.info("开始爬取中北大学数据...")
        recruitment_data = []
        
        try:
            # 爬取招生信息页面
            url = 'https://zb.nuc.edu.cn/zs/'
            html = self.fetch_page(url)
            
            if html:
                soup = self.parse_html(html)
                # 根据实际页面结构调整选择器
                plans = soup.find_all('tr')
                
                for plan in plans[1:]:  # 跳过表头
                    try:
                        tds = plan.find_all('td')
                        if len(tds) >= 3:
                            major_name = tds[0].get_text(strip=True)
                            enrollment = tds[1].get_text(strip=True)
                            province = tds[2].get_text(strip=True) if len(tds) > 2 else ''
                            
                            recruitment_data.append({
                                'university_name': self.university_name,
                                'university_code': '10058',
                                'major_name': major_name,
                                'major_code': '',
                                'enrollment_count': int(enrollment) if enrollment.isdigit() else 0,
                                'year': datetime.now().year,
                                'province': province,
                                'batch_type': '',
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"解析中北大学数据行失败: {e}")
                        continue
            
            logger.info(f"中北大学爬取成功，共 {len(recruitment_data)} 条记录")
            return recruitment_data
            
        except Exception as e:
            logger.error(f"中北大学爬虫异常: {e}")
            return []


class ShanxiNormalUniversityCrawler(BaseCrawler):
    """山西师范大学爬虫"""
    
    def crawl(self):
        """爬取山西师范大学招生计划"""
        logger.info("开始爬取山西师范大学数据...")
        recruitment_data = []
        
        try:
            url = 'https://www.sxnu.edu.cn/zs/'
            html = self.fetch_page(url)
            
            if html:
                soup = self.parse_html(html)
                plans = soup.find_all('tr')
                
                for plan in plans[1:]:
                    try:
                        tds = plan.find_all('td')
                        if len(tds) >= 3:
                            major_name = tds[0].get_text(strip=True)
                            enrollment = tds[1].get_text(strip=True)
                            
                            recruitment_data.append({
                                'university_name': self.university_name,
                                'university_code': '10118',
                                'major_name': major_name,
                                'major_code': '',
                                'enrollment_count': int(enrollment) if enrollment.isdigit() else 0,
                                'year': datetime.now().year,
                                'province': '山西',
                                'batch_type': '',
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"解析山西师范大学数据行失败: {e}")
                        continue
            
            logger.info(f"山西师范大学爬取成功，共 {len(recruitment_data)} 条记录")
            return recruitment_data
            
        except Exception as e:
            logger.error(f"山西师范大学爬虫异常: {e}")
            return []


class NortheastUniversityCrawler(BaseCrawler):
    """东北大学爬虫"""
    
    def crawl(self):
        """爬取东北大学招生计划"""
        logger.info("开始爬取东北大学数据...")
        recruitment_data = []
        
        try:
            url = 'https://www.neu.edu.cn/zs/'
            html = self.fetch_page(url)
            
            if html:
                soup = self.parse_html(html)
                plans = soup.find_all('tr')
                
                for plan in plans[1:]:
                    try:
                        tds = plan.find_all('td')
                        if len(tds) >= 3:
                            major_name = tds[0].get_text(strip=True)
                            enrollment = tds[1].get_text(strip=True)
                            
                            recruitment_data.append({
                                'university_name': self.university_name,
                                'university_code': '10145',
                                'major_name': major_name,
                                'major_code': '',
                                'enrollment_count': int(enrollment) if enrollment.isdigit() else 0,
                                'year': datetime.now().year,
                                'province': '辽宁',
                                'batch_type': '',
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"解析东北大学数据行失败: {e}")
                        continue
            
            logger.info(f"东北大学爬取成功，共 {len(recruitment_data)} 条记录")
            return recruitment_data
            
        except Exception as e:
            logger.error(f"东北大学爬虫异常: {e}")
            return []


class HebeiIndustrialUniversityCrawler(BaseCrawler):
    """河北工业大学爬虫"""
    
    def crawl(self):
        """爬取河北工业大学招生计划"""
        logger.info("开始爬取河北工业大学数据...")
        recruitment_data = []
        
        try:
            url = 'https://www.hebut.edu.cn/zs/'
            html = self.fetch_page(url)
            
            if html:
                soup = self.parse_html(html)
                plans = soup.find_all('tr')
                
                for plan in plans[1:]:
                    try:
                        tds = plan.find_all('td')
                        if len(tds) >= 3:
                            major_name = tds[0].get_text(strip=True)
                            enrollment = tds[1].get_text(strip=True)
                            
                            recruitment_data.append({
                                'university_name': self.university_name,
                                'university_code': '10080',
                                'major_name': major_name,
                                'major_code': '',
                                'enrollment_count': int(enrollment) if enrollment.isdigit() else 0,
                                'year': datetime.now().year,
                                'province': '河北',
                                'batch_type': '',
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"解析河北工业大学数据行失败: {e}")
                        continue
            
            logger.info(f"河北工业大学爬取成功，共 {len(recruitment_data)} 条记录")
            return recruitment_data
            
        except Exception as e:
            logger.error(f"河北工业大学爬虫异常: {e}")
            return []


class ShanghaiFinanceUniversityCrawler(BaseCrawler):
    """上海财经大学爬虫"""
    
    def crawl(self):
        """爬取上海财经大学招生计划"""
        logger.info("开始爬取上海财经大学数据...")
        recruitment_data = []
        
        try:
            url = 'https://www.sufe.edu.cn/zs/'
            html = self.fetch_page(url)
            
            if html:
                soup = self.parse_html(html)
                plans = soup.find_all('tr')
                
                for plan in plans[1:]:
                    try:
                        tds = plan.find_all('td')
                        if len(tds) >= 3:
                            major_name = tds[0].get_text(strip=True)
                            enrollment = tds[1].get_text(strip=True)
                            
                            recruitment_data.append({
                                'university_name': self.university_name,
                                'university_code': '10272',
                                'major_name': major_name,
                                'major_code': '',
                                'enrollment_count': int(enrollment) if enrollment.isdigit() else 0,
                                'year': datetime.now().year,
                                'province': '上海',
                                'batch_type': '',
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"解析上海财经大学数据行失败: {e}")
                        continue
            
            logger.info(f"上海财经大学爬取成功，共 {len(recruitment_data)} 条记录")
            return recruitment_data
            
        except Exception as e:
            logger.error(f"上海财经大学爬虫异常: {e}")
            return []

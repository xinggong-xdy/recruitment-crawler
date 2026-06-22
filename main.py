#!/usr/bin/env python3
"""
招生计划爬虫主程序
功能：爬取5所高校招生计划 -> 处理数据 -> 存储数据库 -> 查询展示
"""

import pandas as pd
from utils.logger import logger
from database.db_handler import DatabaseHandler
from crawler.universities import (
    ZhongbeiUniversityCrawler,
    ShanxiNormalUniversityCrawler,
    NortheastUniversityCrawler,
    HebeiIndustrialUniversityCrawler,
    ShanghaiFinanceUniversityCrawler
)


class RecruitmentCrawlerManager:
    """招生计划爬虫管理器"""
    
    def __init__(self):
        self.db = DatabaseHandler()
        self.crawlers = [
            ('中北大学', ZhongbeiUniversityCrawler('中北大学', 'https://zb.nuc.edu.cn/')),
            ('山西师范大学', ShanxiNormalUniversityCrawler('山西师范大学', 'https://www.sxnu.edu.cn/')),
            ('东北大学', NortheastUniversityCrawler('东北大学', 'https://www.neu.edu.cn/')),
            ('河北工业大学', HebeiIndustrialUniversityCrawler('河北工业大学', 'https://www.hebut.edu.cn/')),
            ('上海财经大学', ShanghaiFinanceUniversityCrawler('上海财经大学', 'https://www.sufe.edu.cn/'))
        ]
        self.all_data = []
    
    def setup_database(self):
        """初始化数据库"""
        logger.info("=" * 50)
        logger.info("初始化数据库...")
        
        if not self.db.connect():
            logger.error("数据库连接失败！")
            return False
        
        if not self.db.create_table():
            logger.error("创建表失败！")
            return False
        
        logger.info("数据库初始化成功")
        return True
    
    def crawl_all(self):
        """爬取所有学校数据"""
        logger.info("=" * 50)
        logger.info("开始爬取招生计划数据...")
        
        for university_name, crawler in self.crawlers:
            try:
                data = crawler.crawl()
                self.all_data.extend(data)
            except Exception as e:
                logger.error(f"爬取 {university_name} 失败: {e}")
                continue
        
        logger.info(f"爬取完成，共获取 {len(self.all_data)} 条数据")
        return len(self.all_data) > 0
    
    def process_data(self):
        """数据处理（清洗、转换）"""
        logger.info("=" * 50)
        logger.info("数据处理中...")
        
        processed_data = []
        for item in self.all_data:
            try:
                # 数据转换为数据库插入格式
                record = (
                    item.get('university_name', ''),
                    item.get('university_code', ''),
                    item.get('major_name', ''),
                    item.get('major_code', ''),
                    item.get('enrollment_count', 0),
                    item.get('year', 0),
                    item.get('province', ''),
                    item.get('batch_type', ''),
                    item.get('url', '')
                )
                processed_data.append(record)
            except Exception as e:
                logger.warning(f"数据处理错误: {e}")
                continue
        
        logger.info(f"数据处理完成，共 {len(processed_data)} 条有效数据")
        return processed_data
    
    def store_data(self, processed_data):
        """存储数据到数据库"""
        logger.info("=" * 50)
        logger.info("存储数据到数据库...")
        
        if not processed_data:
            logger.warning("没有数据要存储")
            return False
        
        # 批量插入数据
        success = self.db.insert_batch(processed_data)
        
        if success:
            logger.info("数据存储成功")
        else:
            logger.error("数据存储失败")
        
        return success
    
    def query_and_display(self):
        """查询数据库并展示结果"""
        logger.info("=" * 50)
        logger.info("查询数据库...")
        
        # 目标学校
        target_universities = [
            '中北大学',
            '山西师范大学',
            '东北大学',
            '河北工业大学',
            '上海财经大学'
        ]
        
        for uni_name in target_universities:
            logger.info(f"\n{'=' * 50}")
            logger.info(f"查询: {uni_name}")
            logger.info('=' * 50)
            
            results = self.db.query_by_university(uni_name)
            
            if results:
                # 转换为DataFrame便于展示
                df = pd.DataFrame(results, columns=['ID', '学校', '专业', '招生数', '年份', '省份', '批次'])
                print(f"\n{uni_name} 招生计划信息:")
                print(df.to_string(index=False))
                print(f"\n总共 {len(results)} 个专业\n")
            else:
                logger.warning(f"{uni_name} 暂无数据")
        
        # 统计信息
        logger.info(f"\n{'=' * 50}")
        logger.info("统计信息")
        logger.info('=' * 50)
        
        stats = self.db.get_statistics()
        if stats:
            df_stats = pd.DataFrame(stats, columns=['学校', '专业数', '总招生人数'])
            print("\n高校招生统计:")
            print(df_stats.to_string(index=False))
            print()
    
    def run(self):
        """运行完整的爬虫流程"""
        try:
            logger.info("\n")
            logger.info("╔" + "=" * 48 + "╗")
            logger.info("║" + " " * 10 + "招生计划爬虫系统启动" + " " * 18 + "║")
            logger.info("╚" + "=" * 48 + "╝")
            
            # 1. 初始化数据库
            if not self.setup_database():
                return False
            
            # 2. 爬取数据
            if not self.crawl_all():
                logger.warning("爬取数据为空，但继续处理...")
            
            # 3. 处理数据
            processed_data = self.process_data()
            
            # 4. 存储数据
            if not self.store_data(processed_data):
                logger.warning("数据存储失败，跳过查询步骤")
                return False
            
            # 5. 查询和展示
            self.query_and_display()
            
            logger.info("\n")
            logger.info("╔" + "=" * 48 + "╗")
            logger.info("║" + " " * 14 + "爬虫程序执行完成" + " " * 16 + "║")
            logger.info("╚" + "=" * 48 + "╝")
            
            return True
            
        except Exception as e:
            logger.error(f"程序执行异常: {e}")
            return False
        finally:
            # 关闭数据库连接
            self.db.close()


def main():
    """主函数"""
    manager = RecruitmentCrawlerManager()
    manager.run()


if __name__ == '__main__':
    main()

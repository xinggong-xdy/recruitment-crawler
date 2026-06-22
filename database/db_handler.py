import mysql.connector
from mysql.connector import Error
from utils.logger import logger
from config import DB_CONFIG


class DatabaseHandler:
    """数据库操作类"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            logger.info("数据库连接成功")
            return True
        except Error as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            logger.info("数据库连接已关闭")
    
    def create_table(self):
        """创建招生计划表"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS recruitment_plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            university_name VARCHAR(100) NOT NULL,
            university_code VARCHAR(50),
            major_name VARCHAR(200) NOT NULL,
            major_code VARCHAR(50),
            enrollment_count INT,
            year INT,
            province VARCHAR(50),
            batch_type VARCHAR(50),
            url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_university (university_name),
            INDEX idx_major (major_name),
            INDEX idx_year (year)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            logger.info("招生计划表创建成功")
            return True
        except Error as e:
            logger.error(f"创建表失败: {e}")
            return False
    
    def insert_recruitment_plan(self, plan_data):
        """插入单条招生计划"""
        insert_sql = """
        INSERT INTO recruitment_plans 
        (university_name, university_code, major_name, major_code, 
         enrollment_count, year, province, batch_type, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_sql, plan_data)
            self.connection.commit()
            logger.info(f"插入数据成功: {plan_data[0]} - {plan_data[2]}")
            return True
        except Error as e:
            logger.error(f"插入数据失败: {e}")
            self.connection.rollback()
            return False
    
    def insert_batch(self, plans_list):
        """批量插入招生计划"""
        insert_sql = """
        INSERT INTO recruitment_plans 
        (university_name, university_code, major_name, major_code, 
         enrollment_count, year, province, batch_type, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.executemany(insert_sql, plans_list)
            self.connection.commit()
            logger.info(f"批量插入 {len(plans_list)} 条数据成功")
            return True
        except Error as e:
            logger.error(f"批量插入失败: {e}")
            self.connection.rollback()
            return False
    
    def query_by_university(self, university_name):
        """查询指定学校的招生计划"""
        query_sql = """
        SELECT id, university_name, major_name, enrollment_count, year, province, batch_type
        FROM recruitment_plans
        WHERE university_name = %s
        ORDER BY year DESC, major_name ASC
        """
        try:
            self.cursor.execute(query_sql, (university_name,))
            results = self.cursor.fetchall()
            logger.info(f"查询 {university_name} 成功，共 {len(results)} 条记录")
            return results
        except Error as e:
            logger.error(f"查询失败: {e}")
            return []
    
    def query_all(self):
        """查询所有招生计划"""
        query_sql = """
        SELECT id, university_name, major_name, enrollment_count, year, province, batch_type
        FROM recruitment_plans
        ORDER BY university_name, year DESC
        """
        try:
            self.cursor.execute(query_sql)
            results = self.cursor.fetchall()
            logger.info(f"查询所有数据成功，共 {len(results)} 条记录")
            return results
        except Error as e:
            logger.error(f"查询失败: {e}")
            return []
    
    def query_by_year(self, year):
        """按年份查询招生计划"""
        query_sql = """
        SELECT id, university_name, major_name, enrollment_count, year, province, batch_type
        FROM recruitment_plans
        WHERE year = %s
        ORDER BY university_name, major_name
        """
        try:
            self.cursor.execute(query_sql, (year,))
            results = self.cursor.fetchall()
            logger.info(f"查询 {year} 年数据成功，共 {len(results)} 条记录")
            return results
        except Error as e:
            logger.error(f"查询失败: {e}")
            return []
    
    def get_statistics(self):
        """获取统计信息"""
        stats_sql = """
        SELECT university_name, COUNT(*) as major_count, SUM(enrollment_count) as total_enrollment
        FROM recruitment_plans
        GROUP BY university_name
        ORDER BY total_enrollment DESC
        """
        try:
            self.cursor.execute(stats_sql)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            logger.error(f"统计查询失败: {e}")
            return []

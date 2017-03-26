# coding = utf-8
# python3中ConfigParser改为configparser
# import ConfigParser
import configparser
import os

config_dir = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(config_dir, 'conf')

conf_object = configparser.ConfigParser()
conf_object.read(config_path)

# 数据库配置
DB_ENGINE = conf_object.get("database", "engine")
DB_NAME = conf_object.get("database", "dbname")
DB_USERNAME = conf_object.get("database", "username")
DB_PASSWORD = conf_object.get("database", "password")
DB_HOST = conf_object.get("database", "host")
DB_PORT = conf_object.get("database", "port")

# xml存放在工程目录中
local_xml_path = project_path + conf_object.get("path", "local_xml_path")
local_xsd_path = project_path + conf_object.get("path", "local_xsd_path")
print("local_xml_path", local_xml_path)
print("local_xsd_path", local_xsd_path)
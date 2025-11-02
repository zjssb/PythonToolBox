import json
import os


class ConfigReader:
    """配置读取类，负责读取和管理界面配置"""
    ins = None

    def __init__(self, config_dir="./res"):
        self.config_dir = config_dir
        self.config_data = {}

    def load_cfg(self, cfg_name):
        """加载配置文件"""
        try:
            config_path = os.path.join(self.config_dir, cfg_name) + ".json"
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self.config_data[cfg_name] = file_config
                print(f"成功加载配置文件: {cfg_name}")
            except Exception as e:
                print(f"加载配置文件 {cfg_name} 时出错: {e}")

        except Exception as e:
            print(f"加载配置时发生错误: {e}")

    def get_cfg(self, cfg_name)->dict:
        """获取配置表

        :return jsonData
        """
        if cfg_name not in self.config_data:
            self.load_cfg(cfg_name)

        cfg = self.config_data[cfg_name]
        return cfg

    def clear(self):
        self.config_data = {}


ConfigReaderInst = ConfigReader()
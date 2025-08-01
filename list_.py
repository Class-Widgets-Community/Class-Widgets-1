import json
import os
from copy import deepcopy
from pathlib import Path
from shutil import copy
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from loguru import logger

from basic_dirs import THEME_DIRS
from data_model import ThemeConfig, ThemeInfo
from file import base_directory, config_center, save_data_to_json

from PyQt5.QtCore import QCoreApplication


week = [QCoreApplication.translate("list_", '周一'), QCoreApplication.translate("list_", '周二'), QCoreApplication.translate("list_", '周三'), QCoreApplication.translate("list_", '周四'), QCoreApplication.translate("list_", '周五'), QCoreApplication.translate("list_", '周六'), QCoreApplication.translate("list_", '周日')]
logger.debug(week)
month = [QCoreApplication.translate("list_", '一月'), QCoreApplication.translate("list_", '二月'), QCoreApplication.translate("list_", '三月'), QCoreApplication.translate("list_", '四月'), QCoreApplication.translate("list_", '五月'), QCoreApplication.translate("list_", '六月'), QCoreApplication.translate("list_", '七月'), QCoreApplication.translate("list_", '八月'), QCoreApplication.translate("list_", '九月'), QCoreApplication.translate("list_", '十月'), QCoreApplication.translate("list_", '十一月'), QCoreApplication.translate("list_", '十二月')]
week_type = [QCoreApplication.translate("list_", '单周'), QCoreApplication.translate("list_", '双周')]
part_type = [QCoreApplication.translate("list_", '节点'), QCoreApplication.translate("list_", '休息段')]
window_status = [QCoreApplication.translate("list_", '无'), QCoreApplication.translate("list_", '置于顶部'), QCoreApplication.translate("list_", '置于底部'), QCoreApplication.translate("list_", '置于次级底部')]
color_mode = [QCoreApplication.translate("list_", '浅色'), QCoreApplication.translate("list_", '深色'), QCoreApplication.translate("list_", '跟随系统')]
hide_mode = [QCoreApplication.translate("list_", '无'), QCoreApplication.translate("list_", '上课时自动隐藏'), QCoreApplication.translate("list_", '窗口最大化时隐藏'), QCoreApplication.translate("list_", '灵活隐藏')]
non_nt_hide_mode = [QCoreApplication.translate("list_", '无'), QCoreApplication.translate("list_", '上课时自动隐藏')]
version_channel = [QCoreApplication.translate("list_", '正式版 (Release)'), QCoreApplication.translate("list_", '测试版 (Beta)')]

theme_folder = []
theme_names = []

subject = {
    QCoreApplication.translate("list_", '语文'): '(255, 151, 135',  # 红
    QCoreApplication.translate("list_", '数学'): '(105, 84, 255',  # 蓝
    QCoreApplication.translate("list_", '英语'): '(236, 135, 255',  # 粉
    QCoreApplication.translate("list_", '生物'): '(68, 200, 94',  # 绿
    QCoreApplication.translate("list_", '地理'): '(80, 214, 200',  # 浅蓝
    QCoreApplication.translate("list_", '政治'): '(255, 110, 110',  # 红
    QCoreApplication.translate("list_", '历史'): '(180, 130, 85',  # 棕
    QCoreApplication.translate("list_", '物理'): '(130, 85, 180',  # 紫
    QCoreApplication.translate("list_", '化学'): '(84, 135, 190',  # 蓝
    QCoreApplication.translate("list_", '美术'): '(0, 186, 255',  # 蓝
    QCoreApplication.translate("list_", '音乐'): '(255, 101, 158',  # 红
    QCoreApplication.translate("list_", '体育'): '(255, 151, 135',  # 红
    QCoreApplication.translate("list_", '信息技术'): '(84, 135, 190',  # 蓝
    QCoreApplication.translate("list_", '电脑'): '(84, 135, 190',  # 蓝
    QCoreApplication.translate("list_", '课程表未加载'): '(255, 151, 135',  # 红

    QCoreApplication.translate("list_", '班会'): '(255, 151, 135',  # 红
    QCoreApplication.translate("list_", '自习'): '(115, 255, 150',  # 绿
    QCoreApplication.translate("list_", '课间'): '(135, 255, 191',  # 绿
    QCoreApplication.translate("list_", '大课间'): '(255, 151, 135',  # 红
    QCoreApplication.translate("list_", '放学'): '(84, 255, 101',  # 绿
    QCoreApplication.translate("list_", '暂无课程'): '(84, 255, 101',  # 绿
}

schedule_dir = os.path.join(base_directory, 'config', 'schedule')

class_activity = [QCoreApplication.translate("list_", '课程'), QCoreApplication.translate("list_", '课间')]
time = [QCoreApplication.translate("list_", '上午'), QCoreApplication.translate("list_", '下午'), QCoreApplication.translate("list_", '晚修')]
class_kind = [
    QCoreApplication.translate("list_", '自定义'),
    QCoreApplication.translate("list_", '语文'),
    QCoreApplication.translate("list_", '数学'),
    QCoreApplication.translate("list_", '英语'),
    QCoreApplication.translate("list_", '政治'),
    QCoreApplication.translate("list_", '历史'),
    QCoreApplication.translate("list_", '生物'),
    QCoreApplication.translate("list_", '地理'),
    QCoreApplication.translate("list_", '物理'),
    QCoreApplication.translate("list_", '化学'),
    QCoreApplication.translate("list_", '体育'),
    QCoreApplication.translate("list_", '班会'),
    QCoreApplication.translate("list_", '自习'),
    QCoreApplication.translate("list_", '早读'),
    QCoreApplication.translate("list_", '大课间'),
    QCoreApplication.translate("list_", '美术'),
    QCoreApplication.translate("list_", '音乐'),
    QCoreApplication.translate("list_", '心理'),
    QCoreApplication.translate("list_", '信息技术')
]

default_widgets = [
    'widget-time.ui',
    'widget-countdown.ui',
    'widget-current-activity.ui',
    'widget-next-activity.ui'
]

widget_width = {  # 默认宽度
    'widget-time.ui': 230,
    'widget-countdown.ui': 200,
    'widget-current-activity.ui': 360,
    'widget-next-activity.ui': 290,
    'widget-countdown-day.ui': 200,
    'widget-weather.ui': 200
}

widget_conf = {
    QCoreApplication.translate("list_", '当前日期'): 'widget-time.ui',
    QCoreApplication.translate("list_", '活动倒计时'): 'widget-countdown.ui',
    QCoreApplication.translate("list_", '当前活动'): 'widget-current-activity.ui',
    QCoreApplication.translate("list_", '更多活动'): 'widget-next-activity.ui',
    QCoreApplication.translate("list_", '倒计日'): 'widget-countdown-day.ui',
    QCoreApplication.translate("list_", '天气'): 'widget-weather.ui'
}

widget_name = {
    'widget-time.ui': QCoreApplication.translate("list_", '当前日期'),
    'widget-countdown.ui': QCoreApplication.translate("list_", '活动倒计时'),
    'widget-current-activity.ui': QCoreApplication.translate("list_", '当前活动'),
    'widget-next-activity.ui': QCoreApplication.translate("list_", '更多活动'),
    'widget-countdown-day.ui': QCoreApplication.translate("list_", '倒计日'),
    'widget-weather.ui': QCoreApplication.translate("list_", '天气')
}

native_widget_name = [widget_name[i] for i in widget_name]

not_exist_themes = []

try:
    with open(base_directory / "config" / "schedule_db.json") as f:
        schedule_dbs = json.load(f).get('db', {})
except:
    logger.warning("读取数据库列表失败，重置为空。")
    schedule_dbs = {}

def validate_theme(folder: Path) -> Optional[ThemeInfo]:
    file_path = folder / 'theme.json'
    if not file_path.exists():
        return None
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return ThemeInfo(
                path=folder,
                config=ThemeConfig.model_validate_json(f.read())
            )
    except Exception as e:
        logger.error(f'验证主题配置文件发生错误：{e}')
        return None


def __collect_themes(it: Iterable[Tuple[str, ThemeInfo]]) -> Dict[str, ThemeInfo]:
    themes: Dict[str, ThemeInfo] = {}
    for name, info in it:
        if name in themes:
            logger.warning(f'主题 {name} - {themes[name].path} 已存在，{info.path} 将覆盖原有配置')
        themes[name] = info
    return themes


try:  # 加载课程/主题配置文件
    subject_info = json.load(open(f'{base_directory}/config/data/subject.json', 'r', encoding='utf-8'))
    subject_icon = subject_info['subject_icon']
    subject_abbreviation = subject_info['subject_abbreviation']
    __theme = __collect_themes(
        (dir.name, info)
        for root_dir in reversed(THEME_DIRS)
        for dir in root_dir.iterdir()
        if (info := validate_theme(dir)) is not None
    )
    theme_folder = list(folder.path.name for folder in __theme.values())
    theme_names = list(folder.config.name for folder in __theme.values())
except Exception as e:
    logger.error(f'加载课程/主题配置文件发生错误，使用默认配置：{e}')
    config_center.write_conf('General', 'theme', 'default')
    subject_icon = {
        QCoreApplication.translate("list_", '语文'): 'chinese',
        QCoreApplication.translate("list_", '数学'): 'math',
        QCoreApplication.translate("list_", '英语'): 'abc',
        QCoreApplication.translate("list_", '生物'): 'biology',
        QCoreApplication.translate("list_", '地理'): 'geography',
        QCoreApplication.translate("list_", '政治'): 'chinese',
        QCoreApplication.translate("list_", '历史'): 'history',
        QCoreApplication.translate("list_", '物理'): 'physics',
        QCoreApplication.translate("list_", '化学'): 'chemistry',
        QCoreApplication.translate("list_", '美术'): 'art',
        QCoreApplication.translate("list_", '音乐'): 'music',
        QCoreApplication.translate("list_", '体育'): 'pe',
        QCoreApplication.translate("list_", '信息技术'): 'it',
        QCoreApplication.translate("list_", '电脑'): 'it',
        QCoreApplication.translate("list_", '课程表未加载'): 'xmark',

        QCoreApplication.translate("list_", '班会'): 'meeting',
        QCoreApplication.translate("list_", '自习'): 'self_study',
        QCoreApplication.translate("list_", '课间'): 'break',
        QCoreApplication.translate("list_", '大课间'): 'pe',
        QCoreApplication.translate("list_", '放学'): 'after_school',
        QCoreApplication.translate("list_", '暂无课程'): 'break',
    }
    # 简称
    subject_abbreviation = {
        QCoreApplication.translate("list_", '历史'): '史'
    }

countdown_modes = [QCoreApplication.translate("list_", '轮播'), QCoreApplication.translate("list_", '多小组件')]


def get_widget_list() -> List[str]:
    rl = []
    for item, value in widget_conf.items():
        rl.append(item)
    return rl


def get_widget_names() -> List[str]:
    rl = []
    for item, value in widget_name.items():
        rl.append(value)
    return rl


def get_current_theme_num() -> Union[str, int]:
    for i in range(len(theme_folder)):
        if not os.path.exists(f'{base_directory}/config/schedule/{theme_folder[i]}.json'):
            return "default"
        if theme_folder[i] == config_center.read_conf('General', 'theme'):
            return i


def get_theme_ui_path(name: str) -> str:
    for i in range(len(theme_folder)):
        if theme_names[i] == name:
            return theme_folder[i]
    return 'default'


def get_subject_abbreviation(key: str) -> str:
    if key in subject_abbreviation:
        return subject_abbreviation[key]
    else:
        return key[:1]


# 学科图标
def get_subject_icon(key: str) -> str:
    if key in subject_icon:
        return f'{base_directory}/img/subject/{subject_icon[key]}.svg'
    else:
        return f'{base_directory}/img/subject/self_study.svg'


# 学科主题色
def subject_color(key: str) -> str:
    if key in subject:
        return f'{subject[key]}'
    else:
        return '(75, 170, 255'


def get_schedule_config() -> List[str]:
    schedule_config = []
    # 遍历目标目录下的所有文件
    for file_name in os.listdir(schedule_dir):
        # 找json
        if file_name.endswith('.json') and file_name != 'backup.json':
            # 将文件路径添加到列表
            schedule_config.append(file_name)
    return schedule_config


def return_default_schedule_number() -> int:
    total = 0
    for file_name in os.listdir(schedule_dir):
        # 找json
        if file_name.startswith('新课表 - '):
            total += 1
    return total


def create_new_profile(filename: str) -> None:
    copy(f'{base_directory}/config/default.json', f'{base_directory}/config/schedule/{filename}')


def import_schedule(filepath: str, filename: str) -> bool:  # 导入课表
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            check_data = json.load(file)
    except Exception as e:
        logger.error(f"加载数据时出错: {e}")
        return False

    try:
        checked_data = convert_schedule(check_data)
    except Exception as e:
        logger.error(f"转换数据时出错: {e}")
        return False
    # 保存文件
    try:
        print(checked_data)
        copy(filepath, f'{base_directory}/config/schedule/{filename}')
        save_data_to_json(checked_data, filename)
        config_center.write_conf('General', 'schedule', filename)
        return True
    except Exception as e:
        logger.error(f"保存数据时出错: {e}")
        return False


def convert_schedule(check_data: Dict[str, Any]) -> Dict[str, Any]:  # 转换课表
    # 校验课程表
    if check_data is None:
        logger.warning('此文件为空')
        raise ValueError('此文件为空')
    elif not check_data.get('timeline') and not check_data.get('schedule'):
        logger.warning('此文件不是课程表文件')
        raise ValueError('此文件不是课程表文件')
    # 转换为标准格式
    if not check_data.get('schedule_even'):
        logger.warning('此课程表格式不支持单双周')
        check_data['schedule_even'] = {str(i): [] for i in range(0, 6)}

    part_data = check_data.get('part')
    if part_data and len(part_data.get('0', [])) == 2:
        logger.warning('此课程表格式不支持休息段')
        for i in range(len(check_data.get('part'))):
            check_data['part'][str(i)].append('节点')

    if not check_data.get('part') or not check_data.get('part_name'):  # 兼容旧版本
        logger.warning('此课程表格式不支持节点')
        try:
            check_data['part'] = {  # 转换旧版本时间线为新版
                "0": check_data['timeline']['start_time_m']['part'], "1": check_data['timeline']['start_time_a']['part']
            }
            check_data['part_name'] = {"0": "上午", "1": "下午"}
            del check_data['timeline']['start_time_m']
            del check_data['timeline']['start_time_a']
            old_timeline = deepcopy(check_data['timeline'])
            # 转换为标准格式
            check_data['timeline']['default'] = {}
            for i in range(0, 6):
                check_data['timeline'][i] = {}

            for item_name, _ in old_timeline.items():
                if item_name[1] == 'a':
                    ma_to_num = 1
                else:
                    ma_to_num = 0
                new_name = item_name[0]+str(ma_to_num)+item_name[2]
                check_data['timeline']['default'][new_name] = check_data['timeline'][item_name]
                del check_data['timeline'][item_name]
        except Exception as e:
            logger.error(f"转换数据时出错: {e}")
            raise e
          
    return check_data


def export_schedule(filepath: str, filename: str) -> bool:  # 导出课表
    try:
        copy(f'{base_directory}/config/schedule/{filename}', filepath)
        return True
    except Exception as e:
        logger.error(f"导出文件时出错: {e}")
        return False


def get_widget_config() -> List[str]:
    try:
        if os.path.exists(f'{base_directory}/config/widget.json'):
            with open(f'{base_directory}/config/widget.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            with open(f'{base_directory}/config/widget.json', 'w', encoding='utf-8') as file:
                data = {'widgets': [
                    'widget-weather.ui', 'widget-countdown.ui', 'widget-current-activity.ui', 'widget-next-activity.ui'
                ]}
                json.dump(data, file, indent=4)
        return data['widgets']
    except Exception as e:
        logger.error(f'ReadWidgetConfigFAILD: {e}')
        return default_widgets


if __name__ == '__main__':
    print(theme_folder)
    print(theme_names)
    print('AL-1S')
    print(get_widget_list())

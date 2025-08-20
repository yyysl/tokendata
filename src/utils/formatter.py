"""
数值格式化工具
将大数字转换为易读的格式（B/M/K）
"""
from typing import Union

def format_number(value: Union[int, float], decimals: int = 2) -> str:
    """
    格式化数字为易读格式
    
    Args:
        value: 要格式化的数值
        decimals: 小数位数
        
    Returns:
        格式化后的字符串
    """
    try:
        if value is None or value == 0:
            return "0"
        
        abs_value = abs(value)
        
        # 十亿级别 (B)
        if abs_value >= 1_000_000_000:
            formatted = value / 1_000_000_000
            return f"{formatted:.{decimals}f}B"
        
        # 百万级别 (M)
        elif abs_value >= 1_000_000:
            formatted = value / 1_000_000
            return f"{formatted:.{decimals}f}M"
        
        # 千级别 (K)
        elif abs_value >= 1_000:
            formatted = value / 1_000
            return f"{formatted:.{decimals}f}K"
        
        # 小于1000的数字
        else:
            return f"{value:.{decimals}f}"
            
    except Exception:
        return str(value)

def format_currency(value: Union[int, float], decimals: int = 2) -> str:
    """
    格式化货币数值
    
    Args:
        value: 要格式化的数值
        decimals: 小数位数
        
    Returns:
        格式化后的货币字符串
    """
    try:
        if value is None or value == 0:
            return "$0"
        
        formatted = format_number(value, decimals)
        return f"${formatted}"
        
    except Exception:
        return f"${value}"

def format_percentage(value: Union[int, float], decimals: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        value: 要格式化的数值
        decimals: 小数位数
        
    Returns:
        格式化后的百分比字符串
    """
    try:
        if value is None:
            return "N/A"
        
        return f"{value:+.{decimals}f}%"
        
    except Exception:
        return f"{value}%"

def format_flow_value(value: Union[int, float], decimals: int = 2) -> str:
    """
    格式化资金流向值
    
    Args:
        value: 流向值（正值表示流入，负值表示流出）
        decimals: 小数位数
        
    Returns:
        格式化后的流向字符串
    """
    try:
        if value is None:
            return "N/A"
        
        if abs(value) < 0.01:  # 接近0的值显示为平衡
            return "0.00"
        
        return f"{value:+.{decimals}f}"
        
    except Exception:
        return f"{value}"

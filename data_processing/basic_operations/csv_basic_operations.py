#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据读取和基本操作示例
使用面向过程编程，适合初学者学习
"""

import pandas as pd
import os

def read_csv_file(file_path):
    """
    读取CSV文件
    参数: file_path - CSV文件路径
    返回: DataFrame对象
    """
    try:
        # 读取CSV文件，指定编码为utf-8
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"✅ 成功读取文件: {file_path}")
        print(f"📊 数据形状: {df.shape[0]}行 {df.shape[1]}列")
        return df
    except FileNotFoundError:
        print(f"❌ 文件未找到: {file_path}")
        return None
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return None

def display_basic_info(df, data_name="数据"):
    """
    显示数据的基本信息
    参数: df - DataFrame对象
         data_name - 数据名称
    """
    print(f"\n=== {data_name}基本信息 ===")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print(f"数据类型:\n{df.dtypes}")
    
    print(f"\n=== 前5行数据 ===")
    print(df.head())
    
    print(f"\n=== 后5行数据 ===")
    print(df.tail())

def display_statistics(df, data_name="数据"):
    """
    显示数值列的统计信息
    参数: df - DataFrame对象
         data_name - 数据名称
    """
    print(f"\n=== {data_name}统计信息 ===")
    # 只显示数值列的统计信息
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        print(df[numeric_columns].describe())
    else:
        print("没有数值列可以统计")

def check_missing_values(df, data_name="数据"):
    """
    检查缺失值
    参数: df - DataFrame对象
         data_name - 数据名称
    """
    print(f"\n=== {data_name}缺失值检查 ===")
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    missing_info = pd.DataFrame({
        '缺失数量': missing_count,
        '缺失百分比': missing_percent
    })
    
    print(missing_info)
    
    total_missing = missing_count.sum()
    if total_missing == 0:
        print("✅ 没有发现缺失值")
    else:
        print(f"⚠️ 总共发现 {total_missing} 个缺失值")

def save_to_csv(df, output_path, data_name="处理后的数据"):
    """
    保存DataFrame到CSV文件
    参数: df - DataFrame对象
         output_path - 输出文件路径
         data_name - 数据名称
    """
    try:
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ {data_name}已保存到: {output_path}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")

def main():
    """
    主函数 - 演示基本的CSV数据操作
    """
    print("🚀 开始CSV数据处理示例")
    
    # 设置文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_data_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    
    employees_file = os.path.join(sample_data_dir, "employees.csv")
    products_file = os.path.join(sample_data_dir, "products.csv")
    
    # 读取员工数据
    print("\n" + "="*50)
    print("📋 处理员工数据")
    print("="*50)
    
    employees_df = read_csv_file(employees_file)
    if employees_df is not None:
        display_basic_info(employees_df, "员工")
        display_statistics(employees_df, "员工")
        check_missing_values(employees_df, "员工")
    
    # 读取商品数据
    print("\n" + "="*50)
    print("🛍️ 处理商品数据")
    print("="*50)
    
    products_df = read_csv_file(products_file)
    if products_df is not None:
        display_basic_info(products_df, "商品")
        display_statistics(products_df, "商品")
        check_missing_values(products_df, "商品")
    
    print("\n🎉 CSV数据处理示例完成！")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据筛选和排序示例
使用面向过程编程，演示常用的数据筛选操作
"""

import pandas as pd
import os

def load_data(file_path):
    """
    加载CSV数据
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"✅ 数据加载成功: {df.shape[0]}行 {df.shape[1]}列")
        return df
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return None

def filter_by_condition(df, column, condition, value):
    """
    根据条件筛选数据
    参数: df - DataFrame对象
         column - 列名
         condition - 条件 ('>', '<', '>=', '<=', '==', '!=')
         value - 比较值
    """
    print(f"\n🔍 筛选条件: {column} {condition} {value}")
    
    if condition == '>':
        filtered_df = df[df[column] > value]
    elif condition == '<':
        filtered_df = df[df[column] < value]
    elif condition == '>=':
        filtered_df = df[df[column] >= value]
    elif condition == '<=':
        filtered_df = df[df[column] <= value]
    elif condition == '==':
        filtered_df = df[df[column] == value]
    elif condition == '!=':
        filtered_df = df[df[column] != value]
    else:
        print("❌ 不支持的条件")
        return df
    
    print(f"📊 筛选结果: {filtered_df.shape[0]}行")
    return filtered_df

def filter_by_multiple_conditions(df, conditions):
    """
    根据多个条件筛选数据
    参数: df - DataFrame对象
         conditions - 条件列表，每个条件是(column, operator, value)的元组
    """
    print(f"\n🔍 多条件筛选:")
    filtered_df = df.copy()
    
    for column, operator, value in conditions:
        print(f"   - {column} {operator} {value}")
        if operator == '>':
            filtered_df = filtered_df[filtered_df[column] > value]
        elif operator == '<':
            filtered_df = filtered_df[filtered_df[column] < value]
        elif operator == '>=':
            filtered_df = filtered_df[filtered_df[column] >= value]
        elif operator == '<=':
            filtered_df = filtered_df[filtered_df[column] <= value]
        elif operator == '==':
            filtered_df = filtered_df[filtered_df[column] == value]
        elif operator == '!=':
            filtered_df = filtered_df[filtered_df[column] != value]
    
    print(f"📊 最终筛选结果: {filtered_df.shape[0]}行")
    return filtered_df

def sort_data(df, column, ascending=True):
    """
    对数据进行排序
    参数: df - DataFrame对象
         column - 排序列名
         ascending - True为升序，False为降序
    """
    order = "升序" if ascending else "降序"
    print(f"\n📈 按 {column} 列进行{order}排序")
    
    sorted_df = df.sort_values(by=column, ascending=ascending)
    print(f"✅ 排序完成")
    return sorted_df

def sort_by_multiple_columns(df, columns, ascending_list=None):
    """
    按多列排序
    参数: df - DataFrame对象
         columns - 排序列名列表
         ascending_list - 每列的排序方向列表
    """
    if ascending_list is None:
        ascending_list = [True] * len(columns)
    
    print(f"\n📈 多列排序:")
    for i, col in enumerate(columns):
        order = "升序" if ascending_list[i] else "降序"
        print(f"   - {col}: {order}")
    
    sorted_df = df.sort_values(by=columns, ascending=ascending_list)
    print(f"✅ 多列排序完成")
    return sorted_df

def get_top_n(df, column, n=5, ascending=False):
    """
    获取前N名数据
    参数: df - DataFrame对象
         column - 排序列名
         n - 获取前几名
         ascending - False为获取最大的N个，True为获取最小的N个
    """
    direction = "最小" if ascending else "最大"
    print(f"\n🏆 获取 {column} 列{direction}的前{n}名:")
    
    top_df = df.nlargest(n, column) if not ascending else df.nsmallest(n, column)
    print(top_df)
    return top_df

def filter_by_text(df, column, text, exact_match=False):
    """
    根据文本内容筛选
    参数: df - DataFrame对象
         column - 列名
         text - 搜索文本
         exact_match - True为精确匹配，False为包含匹配
    """
    match_type = "精确匹配" if exact_match else "包含匹配"
    print(f"\n🔍 文本筛选 ({match_type}): {column} 包含 '{text}'")
    
    if exact_match:
        filtered_df = df[df[column] == text]
    else:
        filtered_df = df[df[column].str.contains(text, na=False)]
    
    print(f"📊 筛选结果: {filtered_df.shape[0]}行")
    return filtered_df

def main():
    """
    主函数 - 演示数据筛选和排序操作
    """
    print("🚀 开始CSV数据筛选和排序示例")
    
    # 设置文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_data_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    
    employees_file = os.path.join(sample_data_dir, "employees.csv")
    products_file = os.path.join(sample_data_dir, "products.csv")
    
    # 处理员工数据
    print("\n" + "="*50)
    print("👥 员工数据筛选和排序")
    print("="*50)
    
    employees_df = load_data(employees_file)
    if employees_df is not None:
        print("\n📋 原始员工数据:")
        print(employees_df)
        
        # 筛选工资大于7000的员工
        high_salary = filter_by_condition(employees_df, '工资', '>', 7000)
        print("\n💰 工资大于7000的员工:")
        print(high_salary)
        
        # 筛选技术部员工
        tech_dept = filter_by_text(employees_df, '部门', '技术部', exact_match=True)
        print("\n💻 技术部员工:")
        print(tech_dept)
        
        # 多条件筛选：技术部且工资大于7500
        tech_high_salary = filter_by_multiple_conditions(
            employees_df, 
            [('部门', '==', '技术部'), ('工资', '>', 7500)]
        )
        print("\n🎯 技术部且工资大于7500的员工:")
        print(tech_high_salary)
        
        # 按工资降序排序
        sorted_by_salary = sort_data(employees_df, '工资', ascending=False)
        print("\n📊 按工资降序排序:")
        print(sorted_by_salary)
        
        # 获取工资最高的前3名
        top_salary = get_top_n(employees_df, '工资', n=3)
    
    # 处理商品数据
    print("\n" + "="*50)
    print("🛍️ 商品数据筛选和排序")
    print("="*50)
    
    products_df = load_data(products_file)
    if products_df is not None:
        print("\n📋 原始商品数据:")
        print(products_df)
        
        # 筛选价格小于10的商品
        cheap_products = filter_by_condition(products_df, '价格', '<', 10)
        print("\n💰 价格小于10的商品:")
        print(cheap_products)
        
        # 筛选水果类商品
        fruits = filter_by_text(products_df, '类别', '水果', exact_match=True)
        print("\n🍎 水果类商品:")
        print(fruits)
        
        # 按销售量降序排序
        sorted_by_sales = sort_data(products_df, '销售量', ascending=False)
        print("\n📈 按销售量降序排序:")
        print(sorted_by_sales)
        
        # 多列排序：先按类别，再按价格
        multi_sorted = sort_by_multiple_columns(
            products_df, 
            ['类别', '价格'], 
            [True, False]  # 类别升序，价格降序
        )
        print("\n🔄 按类别升序、价格降序排序:")
        print(multi_sorted)
        
        # 获取销售量最高的前3名商品
        top_sales = get_top_n(products_df, '销售量', n=3)
    
    print("\n🎉 数据筛选和排序示例完成！")

if __name__ == "__main__":
    main()
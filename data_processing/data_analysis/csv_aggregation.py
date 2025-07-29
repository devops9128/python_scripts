#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据聚合和汇总示例
使用面向过程编程，演示数据聚合、分组汇总等操作
"""

import pandas as pd
import numpy as np
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

def create_extended_sample_data():
    """
    创建扩展的示例数据用于聚合分析
    """
    print("🔧 创建扩展示例数据...")
    
    # 销售数据
    sales_data = {
        '日期': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',
                '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10',
                '2024-02-01', '2024-02-02', '2024-02-03', '2024-02-04', '2024-02-05'],
        '销售员': ['张三', '李四', '王五', '张三', '李四', '王五', '张三', '李四', '王五', '张三',
                 '李四', '王五', '张三', '李四', '王五'],
        '产品': ['苹果', '香蕉', '苹果', '橙子', '苹果', '香蕉', '橙子', '苹果', '橙子', '香蕉',
               '苹果', '橙子', '香蕉', '苹果', '橙子'],
        '数量': [10, 15, 8, 12, 20, 18, 6, 14, 9, 16, 11, 13, 17, 19, 7],
        '单价': [5.5, 3.2, 5.5, 4.8, 5.5, 3.2, 4.8, 5.5, 4.8, 3.2, 5.5, 4.8, 3.2, 5.5, 4.8],
        '地区': ['北京', '上海', '广州', '北京', '上海', '广州', '北京', '上海', '广州', '北京',
               '上海', '广州', '北京', '上海', '广州']
    }
    
    df = pd.DataFrame(sales_data)
    df['销售额'] = df['数量'] * df['单价']
    df['日期'] = pd.to_datetime(df['日期'])
    
    return df

def basic_aggregation(df, data_name="数据"):
    """
    基础聚合操作
    """
    print(f"\n📊 {data_name}基础聚合分析")
    print("-" * 40)
    
    # 总体统计
    print("总体统计:")
    print(f"  总销售额: {df['销售额'].sum():.2f}")
    print(f"  平均销售额: {df['销售额'].mean():.2f}")
    print(f"  最大单笔销售: {df['销售额'].max():.2f}")
    print(f"  最小单笔销售: {df['销售额'].min():.2f}")
    print(f"  总销售数量: {df['数量'].sum()}")
    print(f"  平均销售数量: {df['数量'].mean():.2f}")

def group_by_single_column(df, group_column, agg_column, data_name="数据"):
    """
    按单列分组聚合
    """
    print(f"\n🔍 {data_name}按{group_column}分组聚合")
    print("-" * 40)
    
    # 基础分组统计
    grouped = df.groupby(group_column)[agg_column].agg(['sum', 'mean', 'count', 'max', 'min'])
    print(f"按{group_column}分组的{agg_column}统计:")
    print(grouped)
    
    # 排序显示
    print(f"\n按{agg_column}总和排序:")
    sorted_groups = grouped.sort_values('sum', ascending=False)
    print(sorted_groups)

def group_by_multiple_columns(df, group_columns, agg_column, data_name="数据"):
    """
    按多列分组聚合
    """
    print(f"\n🔍 {data_name}按{group_columns}多列分组聚合")
    print("-" * 50)
    
    # 多列分组
    grouped = df.groupby(group_columns)[agg_column].agg(['sum', 'mean', 'count'])
    print(f"按{group_columns}分组的{agg_column}统计:")
    print(grouped)
    
    # 重置索引以便更好地查看
    grouped_reset = grouped.reset_index()
    print(f"\n重置索引后的结果:")
    print(grouped_reset)

def custom_aggregation(df, data_name="数据"):
    """
    自定义聚合函数
    """
    print(f"\n🛠️ {data_name}自定义聚合分析")
    print("-" * 40)
    
    # 自定义聚合函数
    def sales_summary(series):
        return pd.Series({
            '总销售额': series.sum(),
            '平均销售额': series.mean(),
            '销售次数': series.count(),
            '最大销售': series.max(),
            '最小销售': series.min(),
            '销售范围': series.max() - series.min(),
            '标准差': series.std()
        })
    
    # 按销售员分组应用自定义函数
    custom_agg = df.groupby('销售员')['销售额'].apply(sales_summary)
    print("销售员销售情况详细分析:")
    print(custom_agg)

def pivot_table_analysis(df, data_name="数据"):
    """
    数据透视表分析
    """
    print(f"\n📋 {data_name}数据透视表分析")
    print("-" * 40)
    
    # 创建数据透视表：销售员 vs 产品
    pivot1 = pd.pivot_table(df, 
                           values='销售额', 
                           index='销售员', 
                           columns='产品', 
                           aggfunc='sum', 
                           fill_value=0)
    print("销售员 vs 产品销售额透视表:")
    print(pivot1)
    
    # 添加总计行和列
    pivot1_with_totals = pivot1.copy()
    pivot1_with_totals['总计'] = pivot1_with_totals.sum(axis=1)
    pivot1_with_totals.loc['总计'] = pivot1_with_totals.sum()
    print(f"\n带总计的透视表:")
    print(pivot1_with_totals)
    
    # 创建数据透视表：地区 vs 产品
    pivot2 = pd.pivot_table(df, 
                           values=['销售额', '数量'], 
                           index='地区', 
                           columns='产品', 
                           aggfunc={'销售额': 'sum', '数量': 'sum'}, 
                           fill_value=0)
    print(f"\n地区 vs 产品多指标透视表:")
    print(pivot2)

def time_based_aggregation(df, data_name="数据"):
    """
    基于时间的聚合分析
    """
    print(f"\n📅 {data_name}时间序列聚合分析")
    print("-" * 40)
    
    # 确保日期列是datetime类型
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 按日期聚合
    daily_sales = df.groupby('日期')['销售额'].sum()
    print("每日销售额:")
    print(daily_sales)
    
    # 按月聚合
    df['月份'] = df['日期'].dt.to_period('M')
    monthly_sales = df.groupby('月份')['销售额'].agg(['sum', 'mean', 'count'])
    print(f"\n每月销售统计:")
    print(monthly_sales)
    
    # 按星期几聚合
    df['星期几'] = df['日期'].dt.day_name()
    weekday_sales = df.groupby('星期几')['销售额'].sum()
    print(f"\n按星期几销售统计:")
    print(weekday_sales)

def rolling_aggregation(df, data_name="数据"):
    """
    滚动窗口聚合
    """
    print(f"\n🔄 {data_name}滚动窗口聚合分析")
    print("-" * 40)
    
    # 按日期排序
    df_sorted = df.sort_values('日期')
    
    # 按日期聚合每日销售额
    daily_sales = df_sorted.groupby('日期')['销售额'].sum().reset_index()
    
    # 计算3日移动平均
    daily_sales['3日移动平均'] = daily_sales['销售额'].rolling(window=3).mean()
    
    # 计算累计销售额
    daily_sales['累计销售额'] = daily_sales['销售额'].cumsum()
    
    print("每日销售额及移动平均:")
    print(daily_sales)

def percentage_analysis(df, data_name="数据"):
    """
    百分比分析
    """
    print(f"\n📊 {data_name}百分比分析")
    print("-" * 40)
    
    # 销售员销售额占比
    salesperson_sales = df.groupby('销售员')['销售额'].sum()
    total_sales = salesperson_sales.sum()
    salesperson_percentage = (salesperson_sales / total_sales * 100).round(2)
    
    print("销售员销售额占比:")
    for person, percentage in salesperson_percentage.items():
        print(f"  {person}: {salesperson_sales[person]:.2f} ({percentage}%)")
    
    # 产品销售额占比
    product_sales = df.groupby('产品')['销售额'].sum()
    product_percentage = (product_sales / total_sales * 100).round(2)
    
    print(f"\n产品销售额占比:")
    for product, percentage in product_percentage.items():
        print(f"  {product}: {product_sales[product]:.2f} ({percentage}%)")
    
    # 地区销售额占比
    region_sales = df.groupby('地区')['销售额'].sum()
    region_percentage = (region_sales / total_sales * 100).round(2)
    
    print(f"\n地区销售额占比:")
    for region, percentage in region_percentage.items():
        print(f"  {region}: {region_sales[region]:.2f} ({percentage}%)")

def ranking_analysis(df, data_name="数据"):
    """
    排名分析
    """
    print(f"\n🏆 {data_name}排名分析")
    print("-" * 40)
    
    # 销售员排名
    salesperson_ranking = df.groupby('销售员')['销售额'].sum().sort_values(ascending=False)
    print("销售员销售额排名:")
    for rank, (person, sales) in enumerate(salesperson_ranking.items(), 1):
        print(f"  第{rank}名: {person} - {sales:.2f}")
    
    # 产品销售量排名
    product_quantity_ranking = df.groupby('产品')['数量'].sum().sort_values(ascending=False)
    print(f"\n产品销售量排名:")
    for rank, (product, quantity) in enumerate(product_quantity_ranking.items(), 1):
        print(f"  第{rank}名: {product} - {quantity}件")
    
    # 地区销售额排名
    region_ranking = df.groupby('地区')['销售额'].sum().sort_values(ascending=False)
    print(f"\n地区销售额排名:")
    for rank, (region, sales) in enumerate(region_ranking.items(), 1):
        print(f"  第{rank}名: {region} - {sales:.2f}")

def save_aggregated_results(df, output_dir):
    """
    保存聚合结果
    """
    print(f"\n💾 保存聚合分析结果")
    print("-" * 40)
    
    try:
        # 销售员汇总
        salesperson_summary = df.groupby('销售员').agg({
            '销售额': ['sum', 'mean', 'count'],
            '数量': ['sum', 'mean']
        }).round(2)
        salesperson_file = os.path.join(output_dir, "销售员汇总.csv")
        salesperson_summary.to_csv(salesperson_file, encoding='utf-8')
        print(f"✅ 销售员汇总已保存: {salesperson_file}")
        
        # 产品汇总
        product_summary = df.groupby('产品').agg({
            '销售额': ['sum', 'mean', 'count'],
            '数量': ['sum', 'mean'],
            '单价': 'mean'
        }).round(2)
        product_file = os.path.join(output_dir, "产品汇总.csv")
        product_summary.to_csv(product_file, encoding='utf-8')
        print(f"✅ 产品汇总已保存: {product_file}")
        
        # 地区汇总
        region_summary = df.groupby('地区').agg({
            '销售额': ['sum', 'mean', 'count'],
            '数量': ['sum', 'mean']
        }).round(2)
        region_file = os.path.join(output_dir, "地区汇总.csv")
        region_summary.to_csv(region_file, encoding='utf-8')
        print(f"✅ 地区汇总已保存: {region_file}")
        
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")

def main():
    """
    主函数 - 演示数据聚合和汇总分析
    """
    print("🚀 开始CSV数据聚合和汇总示例")
    
    # 创建扩展示例数据
    sales_df = create_extended_sample_data()
    
    print("\n" + "="*60)
    print("📊 销售数据聚合和汇总分析")
    print("="*60)
    
    print("\n原始销售数据:")
    print(sales_df.head(10))
    
    # 各种聚合分析
    basic_aggregation(sales_df, "销售")
    group_by_single_column(sales_df, '销售员', '销售额', "销售")
    group_by_single_column(sales_df, '产品', '数量', "销售")
    group_by_multiple_columns(sales_df, ['销售员', '产品'], '销售额', "销售")
    custom_aggregation(sales_df, "销售")
    pivot_table_analysis(sales_df, "销售")
    time_based_aggregation(sales_df, "销售")
    rolling_aggregation(sales_df, "销售")
    percentage_analysis(sales_df, "销售")
    ranking_analysis(sales_df, "销售")
    
    # 保存结果
    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_aggregated_results(sales_df, current_dir)
    
    print("\n🎉 数据聚合和汇总示例完成！")
    print("\n📊 分析内容总结:")
    print("1. ✅ 基础聚合分析")
    print("2. ✅ 单列分组聚合")
    print("3. ✅ 多列分组聚合")
    print("4. ✅ 自定义聚合函数")
    print("5. ✅ 数据透视表分析")
    print("6. ✅ 时间序列聚合")
    print("7. ✅ 滚动窗口聚合")
    print("8. ✅ 百分比分析")
    print("9. ✅ 排名分析")
    print("10. ✅ 结果保存")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据统计分析示例
使用面向过程编程，演示常见的数据统计分析操作
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

def basic_statistics(df, data_name="数据"):
    """
    基础统计分析
    """
    print(f"\n📊 {data_name}基础统计分析")
    print("-" * 40)
    
    # 数值列统计
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        print("数值列统计信息:")
        stats = df[numeric_columns].describe()
        print(stats)
        
        # 额外统计信息
        print(f"\n详细统计:")
        for col in numeric_columns:
            data = df[col]
            print(f"\n{col}列:")
            print(f"  总数: {data.count()}")
            print(f"  均值: {data.mean():.2f}")
            print(f"  中位数: {data.median():.2f}")
            print(f"  众数: {data.mode().iloc[0] if len(data.mode()) > 0 else '无'}")
            print(f"  标准差: {data.std():.2f}")
            print(f"  方差: {data.var():.2f}")
            print(f"  最小值: {data.min()}")
            print(f"  最大值: {data.max()}")
            print(f"  范围: {data.max() - data.min()}")

def categorical_analysis(df, data_name="数据"):
    """
    分类数据分析
    """
    print(f"\n📈 {data_name}分类数据分析")
    print("-" * 40)
    
    # 文本列分析
    text_columns = df.select_dtypes(include=['object']).columns
    
    for col in text_columns:
        print(f"\n{col}列分析:")
        value_counts = df[col].value_counts()
        print(f"  唯一值数量: {df[col].nunique()}")
        print(f"  频次统计:")
        for value, count in value_counts.items():
            percentage = (count / len(df)) * 100
            print(f"    {value}: {count}次 ({percentage:.1f}%)")

def group_analysis(df, group_column, target_column, data_name="数据"):
    """
    分组分析
    """
    print(f"\n🔍 {data_name}分组分析: 按{group_column}分组分析{target_column}")
    print("-" * 50)
    
    # 按组统计
    grouped = df.groupby(group_column)[target_column]
    
    print("分组统计结果:")
    group_stats = grouped.agg(['count', 'mean', 'median', 'std', 'min', 'max'])
    print(group_stats)
    
    # 详细分组信息
    print(f"\n详细分组信息:")
    for group_name, group_data in df.groupby(group_column):
        target_data = group_data[target_column]
        print(f"\n{group_column} = {group_name}:")
        print(f"  人数: {len(group_data)}")
        print(f"  {target_column}均值: {target_data.mean():.2f}")
        print(f"  {target_column}中位数: {target_data.median():.2f}")
        print(f"  {target_column}最大值: {target_data.max()}")
        print(f"  {target_column}最小值: {target_data.min()}")

def correlation_analysis(df, data_name="数据"):
    """
    相关性分析
    """
    print(f"\n🔗 {data_name}相关性分析")
    print("-" * 40)
    
    # 只分析数值列
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) < 2:
        print("数值列少于2个，无法进行相关性分析")
        return
    
    # 计算相关系数矩阵
    correlation_matrix = df[numeric_columns].corr()
    print("相关系数矩阵:")
    print(correlation_matrix)
    
    # 找出强相关关系
    print(f"\n强相关关系 (|相关系数| > 0.7):")
    for i in range(len(numeric_columns)):
        for j in range(i+1, len(numeric_columns)):
            col1 = numeric_columns[i]
            col2 = numeric_columns[j]
            corr_value = correlation_matrix.loc[col1, col2]
            if abs(corr_value) > 0.7:
                relationship = "正相关" if corr_value > 0 else "负相关"
                print(f"  {col1} 与 {col2}: {corr_value:.3f} ({relationship})")

def percentile_analysis(df, column, data_name="数据"):
    """
    百分位数分析
    """
    print(f"\n📏 {data_name}{column}列百分位数分析")
    print("-" * 40)
    
    data = df[column]
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    
    print("百分位数分布:")
    for p in percentiles:
        value = np.percentile(data, p)
        print(f"  {p}%分位数: {value:.2f}")
    
    # 分析数据分布
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    print(f"\n分布特征:")
    print(f"  四分位距(IQR): {iqr:.2f}")
    print(f"  下四分位数(Q1): {q1:.2f}")
    print(f"  上四分位数(Q3): {q3:.2f}")

def outlier_detection(df, column, data_name="数据"):
    """
    异常值检测
    """
    print(f"\n🎯 {data_name}{column}列异常值检测")
    print("-" * 40)
    
    data = df[column]
    
    # 使用IQR方法检测异常值
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    
    print(f"IQR方法异常值检测:")
    print(f"  正常范围: {lower_bound:.2f} - {upper_bound:.2f}")
    print(f"  异常值数量: {len(outliers)}")
    
    if len(outliers) > 0:
        print(f"  异常值列表: {outliers.tolist()}")
    
    # 使用Z-score方法检测异常值
    z_scores = np.abs((data - data.mean()) / data.std())
    z_outliers = data[z_scores > 3]
    
    print(f"\nZ-score方法异常值检测 (|Z| > 3):")
    print(f"  异常值数量: {len(z_outliers)}")
    if len(z_outliers) > 0:
        print(f"  异常值列表: {z_outliers.tolist()}")

def trend_analysis(df, date_column, value_column, data_name="数据"):
    """
    趋势分析（如果有日期列）
    """
    print(f"\n📈 {data_name}趋势分析")
    print("-" * 40)
    
    try:
        # 转换日期列
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        # 按日期排序
        df_sorted = df_copy.sort_values(date_column)
        
        # 计算变化趋势
        values = df_sorted[value_column].values
        if len(values) > 1:
            # 计算总体趋势
            first_value = values[0]
            last_value = values[-1]
            total_change = last_value - first_value
            change_percentage = (total_change / first_value) * 100
            
            print(f"趋势分析结果:")
            print(f"  起始值: {first_value}")
            print(f"  结束值: {last_value}")
            print(f"  总变化: {total_change:.2f}")
            print(f"  变化百分比: {change_percentage:.2f}%")
            
            # 判断趋势方向
            if change_percentage > 5:
                trend = "上升趋势"
            elif change_percentage < -5:
                trend = "下降趋势"
            else:
                trend = "相对稳定"
            
            print(f"  趋势判断: {trend}")
            
    except Exception as e:
        print(f"无法进行趋势分析: {e}")

def generate_summary_report(df, data_name="数据"):
    """
    生成数据分析摘要报告
    """
    print(f"\n📋 {data_name}分析摘要报告")
    print("=" * 50)
    
    # 基本信息
    print(f"数据概况:")
    print(f"  总行数: {len(df)}")
    print(f"  总列数: {len(df.columns)}")
    print(f"  数值列数: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"  文本列数: {len(df.select_dtypes(include=['object']).columns)}")
    
    # 数据质量
    missing_count = df.isnull().sum().sum()
    duplicate_count = df.duplicated().sum()
    
    print(f"\n数据质量:")
    print(f"  缺失值总数: {missing_count}")
    print(f"  重复行数: {duplicate_count}")
    print(f"  数据完整性: {((len(df) * len(df.columns) - missing_count) / (len(df) * len(df.columns))) * 100:.1f}%")
    
    # 关键统计
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        print(f"\n关键统计指标:")
        for col in numeric_columns:
            data = df[col]
            print(f"  {col}: 均值={data.mean():.2f}, 中位数={data.median():.2f}, 标准差={data.std():.2f}")

def main():
    """
    主函数 - 演示数据统计分析
    """
    print("🚀 开始CSV数据统计分析示例")
    
    # 设置文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_data_dir = os.path.join(os.path.dirname(current_dir), "sample_data")
    
    employees_file = os.path.join(sample_data_dir, "employees.csv")
    products_file = os.path.join(sample_data_dir, "products.csv")
    
    # 分析员工数据
    print("\n" + "="*60)
    print("👥 员工数据统计分析")
    print("="*60)
    
    employees_df = load_data(employees_file)
    if employees_df is not None:
        basic_statistics(employees_df, "员工")
        categorical_analysis(employees_df, "员工")
        group_analysis(employees_df, '部门', '工资', "员工")
        percentile_analysis(employees_df, '工资', "员工")
        outlier_detection(employees_df, '工资', "员工")
        outlier_detection(employees_df, '年龄', "员工")
        trend_analysis(employees_df, '入职日期', '工资', "员工")
        generate_summary_report(employees_df, "员工")
    
    # 分析商品数据
    print("\n" + "="*60)
    print("🛍️ 商品数据统计分析")
    print("="*60)
    
    products_df = load_data(products_file)
    if products_df is not None:
        basic_statistics(products_df, "商品")
        categorical_analysis(products_df, "商品")
        group_analysis(products_df, '类别', '价格', "商品")
        group_analysis(products_df, '类别', '销售量', "商品")
        correlation_analysis(products_df, "商品")
        percentile_analysis(products_df, '价格', "商品")
        outlier_detection(products_df, '价格', "商品")
        generate_summary_report(products_df, "商品")
    
    print("\n🎉 数据统计分析示例完成！")
    print("\n📊 分析内容总结:")
    print("1. ✅ 基础统计分析")
    print("2. ✅ 分类数据分析")
    print("3. ✅ 分组分析")
    print("4. ✅ 相关性分析")
    print("5. ✅ 百分位数分析")
    print("6. ✅ 异常值检测")
    print("7. ✅ 趋势分析")
    print("8. ✅ 摘要报告生成")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV数据清洗示例
使用面向过程编程，演示常见的数据清洗操作
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

def create_sample_dirty_data():
    """
    创建包含脏数据的示例数据集
    """
    print("🔧 创建包含脏数据的示例数据集...")
    
    data = {
        '姓名': ['张三', '李四', '', '王五', '赵六', '钱七', '孙八', None, '周九', '吴十'],
        '年龄': [28, 32, 25, -5, 35, 150, 29, 31, 27, 33],
        '部门': ['技术部', '销售部', '技术部', '人事部', '销售部', '技术部', '市场部', '人事部', '技术部', '销售部'],
        '工资': [8000, 6500, 7500, 7000, None, 8500, 6200, 7200, 7800, 6900],
        '邮箱': ['zhang@company.com', 'li@company', 'wang@company.com', '', 'zhao@company.com', 
                'qian@company.com', 'sun@company.com', 'zhou@company.com', 'wu@company.com', 'wu@company.com']
    }
    
    df = pd.DataFrame(data)
    return df

def check_data_quality(df, data_name="数据"):
    """
    检查数据质量
    """
    print(f"\n🔍 {data_name}质量检查:")
    print(f"数据形状: {df.shape}")
    
    # 检查缺失值
    missing_count = df.isnull().sum()
    print(f"\n缺失值统计:")
    for col, count in missing_count.items():
        if count > 0:
            print(f"  {col}: {count}个缺失值")
    
    # 检查空字符串
    empty_strings = (df == '').sum()
    print(f"\n空字符串统计:")
    for col, count in empty_strings.items():
        if count > 0:
            print(f"  {col}: {count}个空字符串")
    
    # 检查重复行
    duplicate_count = df.duplicated().sum()
    print(f"\n重复行: {duplicate_count}行")
    
    # 检查数值列的异常值
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        print(f"\n数值列统计:")
        print(df[numeric_columns].describe())

def clean_missing_values(df, strategy='drop'):
    """
    处理缺失值
    参数: df - DataFrame对象
         strategy - 处理策略: 'drop', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value'
    """
    print(f"\n🧹 处理缺失值 (策略: {strategy})")
    
    if strategy == 'drop':
        # 删除包含缺失值的行
        cleaned_df = df.dropna()
        print(f"删除缺失值后: {cleaned_df.shape[0]}行")
        
    elif strategy == 'fill_mean':
        # 用均值填充数值列的缺失值
        cleaned_df = df.copy()
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            mean_value = df[col].mean()
            cleaned_df[col].fillna(mean_value, inplace=True)
            print(f"  {col}列用均值{mean_value:.2f}填充")
        
    elif strategy == 'fill_median':
        # 用中位数填充数值列的缺失值
        cleaned_df = df.copy()
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            median_value = df[col].median()
            cleaned_df[col].fillna(median_value, inplace=True)
            print(f"  {col}列用中位数{median_value:.2f}填充")
        
    elif strategy == 'fill_mode':
        # 用众数填充
        cleaned_df = df.copy()
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else '未知'
                cleaned_df[col].fillna(mode_value, inplace=True)
                print(f"  {col}列用众数'{mode_value}'填充")
    
    else:
        cleaned_df = df.copy()
    
    return cleaned_df

def clean_empty_strings(df, fill_value='未知'):
    """
    处理空字符串
    """
    print(f"\n🧹 处理空字符串 (填充值: '{fill_value}')")
    
    cleaned_df = df.copy()
    for col in df.columns:
        if df[col].dtype == 'object':  # 只处理文本列
            empty_count = (df[col] == '').sum()
            if empty_count > 0:
                cleaned_df[col] = cleaned_df[col].replace('', fill_value)
                print(f"  {col}列: {empty_count}个空字符串已填充")
    
    return cleaned_df

def remove_duplicates(df):
    """
    删除重复行
    """
    print(f"\n🧹 删除重复行")
    
    original_count = len(df)
    cleaned_df = df.drop_duplicates()
    removed_count = original_count - len(cleaned_df)
    
    print(f"删除了{removed_count}行重复数据")
    print(f"清洗后: {len(cleaned_df)}行")
    
    return cleaned_df

def clean_outliers(df, column, method='iqr'):
    """
    处理异常值
    参数: df - DataFrame对象
         column - 列名
         method - 处理方法: 'iqr', 'zscore', 'range'
    """
    print(f"\n🧹 处理{column}列的异常值 (方法: {method})")
    
    cleaned_df = df.copy()
    
    if method == 'iqr':
        # 使用四分位数方法
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        print(f"  检测到{len(outliers)}个异常值")
        print(f"  正常范围: {lower_bound:.2f} - {upper_bound:.2f}")
        
        # 将异常值替换为边界值
        cleaned_df[column] = cleaned_df[column].clip(lower_bound, upper_bound)
        
    elif method == 'range':
        # 使用合理范围（针对年龄）
        if column == '年龄':
            lower_bound = 18
            upper_bound = 65
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            print(f"  检测到{len(outliers)}个异常值")
            print(f"  合理范围: {lower_bound} - {upper_bound}")
            
            # 将异常值替换为边界值
            cleaned_df[column] = cleaned_df[column].clip(lower_bound, upper_bound)
    
    return cleaned_df

def validate_email(df, email_column):
    """
    验证邮箱格式
    """
    print(f"\n🧹 验证{email_column}列的邮箱格式")
    
    cleaned_df = df.copy()
    
    # 简单的邮箱格式验证
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # 检查邮箱格式
    invalid_emails = ~cleaned_df[email_column].str.match(email_pattern, na=False)
    invalid_count = invalid_emails.sum()
    
    print(f"  检测到{invalid_count}个无效邮箱")
    
    if invalid_count > 0:
        print("  无效邮箱列表:")
        invalid_email_list = cleaned_df[invalid_emails][email_column].tolist()
        for email in invalid_email_list:
            print(f"    - {email}")
        
        # 将无效邮箱标记为待修正
        cleaned_df.loc[invalid_emails, email_column] = '待修正'
    
    return cleaned_df

def save_cleaned_data(df, output_path):
    """
    保存清洗后的数据
    """
    try:
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ 清洗后的数据已保存到: {output_path}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")

def main():
    """
    主函数 - 演示数据清洗操作
    """
    print("🚀 开始CSV数据清洗示例")
    
    # 创建包含脏数据的示例
    dirty_df = create_sample_dirty_data()
    
    print("\n" + "="*50)
    print("🗂️ 原始脏数据")
    print("="*50)
    print(dirty_df)
    
    # 检查数据质量
    check_data_quality(dirty_df, "原始")
    
    # 开始清洗过程
    print("\n" + "="*50)
    print("🧹 开始数据清洗过程")
    print("="*50)
    
    # 步骤1: 处理空字符串
    step1_df = clean_empty_strings(dirty_df, '未知')
    
    # 步骤2: 处理缺失值（用众数填充）
    step2_df = clean_missing_values(step1_df, 'fill_mode')
    
    # 步骤3: 处理年龄异常值
    step3_df = clean_outliers(step2_df, '年龄', 'range')
    
    # 步骤4: 验证邮箱格式
    step4_df = validate_email(step3_df, '邮箱')
    
    # 步骤5: 删除重复行
    final_df = remove_duplicates(step4_df)
    
    print("\n" + "="*50)
    print("✨ 清洗后的数据")
    print("="*50)
    print(final_df)
    
    # 检查清洗后的数据质量
    check_data_quality(final_df, "清洗后")
    
    # 保存清洗后的数据
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "cleaned_data.csv")
    save_cleaned_data(final_df, output_path)
    
    print("\n🎉 数据清洗示例完成！")
    print("\n📋 清洗步骤总结:")
    print("1. ✅ 处理空字符串")
    print("2. ✅ 处理缺失值")
    print("3. ✅ 处理年龄异常值")
    print("4. ✅ 验证邮箱格式")
    print("5. ✅ 删除重复行")

if __name__ == "__main__":
    main()
# 基础操作

本目录包含CSV数据处理的基础操作代码，适合初学者学习pandas的基本用法。

## 📋 脚本列表

### 🎯 学习顺序推荐

1. **csv_basic_operations.py** ⭐ - CSV基础读取和操作
2. **csv_filter_sort.py** - 数据筛选和排序
3. **csv_data_cleaning.py** - 数据清洗

## 🚀 快速开始

### 基础操作学习
```bash
python csv_basic_operations.py
```

### 筛选和排序
```bash
python csv_filter_sort.py
```

### 数据清洗
```bash
python csv_data_cleaning.py
```

## 📚 学习内容

### csv_basic_operations.py
- ✅ CSV文件读取
- ✅ 数据基本信息查看
- ✅ 数据预览（头部/尾部）
- ✅ 统计信息显示
- ✅ 缺失值检查
- ✅ 数据保存

**学习重点**: 
- `pd.read_csv()` 读取文件
- `df.head()`, `df.tail()` 数据预览
- `df.describe()` 统计信息
- `df.isnull()` 缺失值检查

### csv_filter_sort.py
- ✅ 单条件筛选
- ✅ 多条件筛选
- ✅ 文本匹配筛选
- ✅ 单列排序
- ✅ 多列排序
- ✅ 获取前N名数据

**学习重点**:
- `df[df['列名'] > 值]` 条件筛选
- `df.sort_values()` 数据排序
- `df.nlargest()`, `df.nsmallest()` 获取极值
- 逻辑运算符的使用

### csv_data_cleaning.py
- ✅ 缺失值处理
- ✅ 空字符串处理
- ✅ 重复数据删除
- ✅ 异常值检测和处理
- ✅ 数据格式验证
- ✅ 数据质量检查

**学习重点**:
- `df.dropna()` 删除缺失值
- `df.fillna()` 填充缺失值
- `df.drop_duplicates()` 删除重复
- 异常值检测方法（IQR、Z-score）

## 🎯 使用场景

### 数据探索阶段
使用 `csv_basic_operations.py` 来：
- 快速了解数据结构
- 检查数据质量
- 获取基本统计信息

### 数据筛选阶段
使用 `csv_filter_sort.py` 来：
- 筛选符合条件的数据
- 对数据进行排序
- 找出关键数据

### 数据清洗阶段
使用 `csv_data_cleaning.py` 来：
- 处理数据质量问题
- 清理异常和错误数据
- 为后续分析准备干净数据

## 📊 输出文件

运行脚本后可能生成的文件：
- **cleaned_data.csv** - 清洗后的数据（由csv_data_cleaning.py生成）

## 💡 学习建议

1. **按顺序学习**: 从基础操作开始
2. **动手实践**: 运行每个脚本，观察输出
3. **修改参数**: 尝试修改筛选条件和排序方式
4. **使用自己的数据**: 替换示例数据文件进行测试

## 🔧 常见问题

### 文件路径问题
确保示例数据文件在正确位置：`../sample_data/`

### 编码问题
如果遇到中文乱码，检查CSV文件编码是否为UTF-8

### 依赖问题
确保已安装pandas：`pip install pandas`

## 📞 支持

遇到问题请查看主目录的README文档或检查代码注释。
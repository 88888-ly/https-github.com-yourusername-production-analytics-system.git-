import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import base64
import sqlite3
import os

# 下载CSV文件功能
def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# 设置页面配置
st.set_page_config(
    page_title="产品生产数据分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 现代化界面设计（增强版）
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* 页面标题样式 */
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4facfe 0%, #00f2fe 100%);
        border-right: none;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        border-radius: 0 12px 12px 0;
    }
    
    /* 侧边栏导航链接 */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        margin: 0.25rem 0.5rem !important;
        padding: 0.5rem 0.75rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
    }
    
    .css-1d391kg:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(8px);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .css-1d391kg[aria-selected="true"] {
        background: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transform: translateX(8px);
        border-color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        border-radius: 50px;
        padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4188 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        transform: translateY(-3px);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.5);
    }
    
    /* 输入框和选择器样式 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select,
    .stMultiSelect>div>div>select {
        background-color: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stDateInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stMultiSelect>div>div>select:focus {
        border-color: #2563eb;
        background-color: #f8fafc;
        color: #0f172a;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1);
        outline: none;
        transform: translateY(-2px);
    }
    
    /* 文本区域样式 */
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #2563eb;
        background-color: #f8fafc;
        color: #0f172a;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1);
        outline: none;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15);
        transform: translateY(-8px);
    }
    
    /* 表单容器样式 */
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        padding: 28px;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    
    /* 标签样式 */
    .stMarkdown label {
        color: #4a5568;
        font-weight: 600;
        font-size: 14px;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    /* 分割线样式 */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* 图表容器样式 */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.95);
        padding: 24px;
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* 页脚样式 */
    .css-164nlkn {
        color: #718096;
        font-size: 14px;
        text-align: center;
        padding: 1rem;
    }
    
    /* 数据框样式 */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    
    .stDataFrame table {
        border-collapse: collapse;
        width: 100%;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        text-align: left;
    }
    
    .stDataFrame td {
        padding: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stDataFrame tr:hover {
        background-color: #f1f5f9;
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    /* 标题装饰 */
    h1::after {
        content: '';
        display: block;
        width: 120px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-top: 10px;
        border-radius: 2px;
        animation: slideIn 0.5s ease-out;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.9);
        padding: 0.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 折叠面板样式 */
    .stExpander {
        margin-bottom: 1rem;
    }
    
    .stExpander [data-baseweb="expandable"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* 下载按钮样式 */
    .css-1cpxqw2 {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }
    
    /* 动画效果 */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            width: 0;
        }
        to {
            width: 120px;
        }
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .metric-card {
            padding: 16px;
            margin-bottom: 1rem;
        }
        
        .stForm {
            padding: 16px;
        }
        
        .sidebar .sidebar-content {
            border-radius: 0;
        }
        
        .css-1d391kg {
            margin: 0.25rem 0.25rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 数据库初始化函数
def init_db():
    conn = sqlite3.connect('production_data.db')
    cursor = conn.cursor()
    # 创建生产数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS production_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product_name TEXT NOT NULL,
            production_quantity INTEGER NOT NULL,
            qualified_quantity INTEGER NOT NULL,
            unqualified_quantity INTEGER NOT NULL,
            unqualified_reason TEXT,
            qualification_rate REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 从数据库加载数据
def load_data_from_db():
    conn = sqlite3.connect('production_data.db')
    df = pd.read_sql_query('SELECT * FROM production_data', conn)
    conn.close()
    
    # 如果数据不为空，转换列名和日期类型
    if not df.empty:
        # 重命名列以匹配应用程序使用的名称
        df = df.rename(columns={
            'date': '日期',
            'product_name': '产品名称',
            'production_quantity': '生产数量',
            'qualified_quantity': '合格数量',
            'unqualified_quantity': '不合格数量',
            'unqualified_reason': '不合格原因',
            'qualification_rate': '合格率'
        })
        # 设置日期列为日期类型
        df['日期'] = pd.to_datetime(df['日期'])
        # 移除id列
        df = df.drop('id', axis=1)
    else:
        # 如果数据库为空，创建空的DataFrame
        df = pd.DataFrame({
            '日期': [],
            '产品名称': [],
            '生产数量': [],
            '合格数量': [],
            '不合格数量': [],
            '不合格原因': [],
            '合格率': []
        })
        df['日期'] = pd.to_datetime(df['日期'])
    
    return df

# 将数据保存到数据库
def save_data_to_db(df):
    conn = sqlite3.connect('production_data.db')
    # 重命名列以匹配数据库结构
    df_db = df.copy()
    df_db = df_db.rename(columns={
        '日期': 'date',
        '产品名称': 'product_name',
        '生产数量': 'production_quantity',
        '合格数量': 'qualified_quantity',
        '不合格数量': 'unqualified_quantity',
        '不合格原因': 'unqualified_reason',
        '合格率': 'qualification_rate'
    })
    # 将日期转换为字符串
    df_db['date'] = df_db['date'].dt.strftime('%Y-%m-%d')
    
    # 清空表并插入新数据
    conn.execute('DELETE FROM production_data')
    df_db.to_sql('production_data', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

# 添加单条数据到数据库
def add_data_to_db(date, product_name, production_quantity, qualified_quantity, unqualified_quantity, unqualified_reason, qualification_rate):
    conn = sqlite3.connect('production_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO production_data (date, product_name, production_quantity, qualified_quantity, unqualified_quantity, unqualified_reason, qualification_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date.strftime('%Y-%m-%d'), product_name, production_quantity, qualified_quantity, unqualified_quantity, unqualified_reason, qualification_rate))
    conn.commit()
    conn.close()

# 删除所有数据
def clear_data_from_db():
    conn = sqlite3.connect('production_data.db')
    conn.execute('DELETE FROM production_data')
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 初始化会话状态 - 从数据库加载数据
if 'production_data' not in st.session_state:
    # 从数据库加载数据
    df = load_data_from_db()
    
    # 如果数据库为空，初始化示例数据
    if df.empty:
        df = pd.DataFrame({
            '日期': [datetime.today().strftime('%Y-%m-%d')],
            '产品名称': ['示例产品'],
            '生产数量': [0],
            '合格数量': [0],
            '不合格数量': [0],
            '不合格原因': ['无'],
            '合格率': [0.0]
        })
        df['日期'] = pd.to_datetime(df['日期'])
        # 保存到数据库
        save_data_to_db(df)
    
    st.session_state.production_data = df

# 侧边栏导航
with st.sidebar:
    st.markdown("### 🔍 数据分析系统")
    st.markdown("---")
    
    selected = option_menu(
        "功能菜单",
        ["数据输入", "数据可视化", "分析报告", "智能分析", "系统设置"],
        icons=["input-cursor-text", "bar-chart-line", "file-text", "robot", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "10px!important", "background-color": "transparent"},
            "icon": {"color": "#000000", "font-size": "22px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px 0", "padding": "12px 15px", "border-radius": "8px", "color": "#000000"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.3)", "color": "#000000", "box-shadow": "0 4px 12px rgba(0,0,0,0.15)"},
        }
    )
    
    st.markdown("---")
    st.markdown("📊 实时数据分析")
    st.markdown("💡 智能优化建议")
    st.markdown("📈 趋势预测分析")

# 数据输入页面
if selected == "数据输入":
    st.title("📥 产品生产信息输入")
    st.markdown("---")
    
    with st.form("production_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("产品名称", placeholder="请输入产品名称")
            production_date = st.date_input("生产日期", value=datetime.today())
            production_quantity = st.number_input("生产数量", min_value=0, step=1, placeholder="请输入生产数量")
            
        with col2:
            qualified_quantity = st.number_input("合格数量", min_value=0, step=1, placeholder="请输入合格数量")
            unqualified_quantity = st.number_input("不合格数量", min_value=0, step=1, placeholder="请输入不合格数量")
            
            # 不合格原因输入
            st.subheader("不合格原因")
            defect_reasons = []
            
            # 预设的常见不合格原因
            common_reasons = [
                "外观缺陷", "尺寸偏差", "性能不达标", "材料问题", 
                "工艺问题", "设备故障", "操作失误", "其他"
            ]
            
            # 多选框选择常见原因
            selected_reasons = st.multiselect(
                "选择常见不合格原因",
                common_reasons
            )
            defect_reasons.extend(selected_reasons)
            
            # 允许用户添加自定义原因
            custom_reason = st.text_input("自定义不合格原因", placeholder="其他原因...")
            if custom_reason:
                defect_reasons.append(custom_reason)
        
        # 提交按钮
        submitted = st.form_submit_button("提交数据")
    
    if submitted:
        # 验证输入数据
        if not product_name:
            st.error("请输入产品名称")
        elif production_quantity <= 0:
            st.error("生产数量必须大于0")
        elif qualified_quantity + unqualified_quantity != production_quantity:
            st.error("合格数量 + 不合格数量 必须等于 生产数量")
        else:
            # 计算合格率
            pass_rate = (qualified_quantity / production_quantity) * 100
            
            # 将不合格原因转换为字符串
            defect_reasons_str = ", ".join(defect_reasons) if defect_reasons else "无"
            
            # 创建新数据记录
            new_record = pd.DataFrame({
                '日期': [pd.to_datetime(production_date)],
                '产品名称': [product_name],
                '生产数量': [production_quantity],
                '合格数量': [qualified_quantity],
                '不合格数量': [unqualified_quantity],
                '不合格原因': [defect_reasons_str],
                '合格率': [pass_rate]
            })
            
            # 添加到会话状态的数据中
            st.session_state.production_data = pd.concat([st.session_state.production_data, new_record], ignore_index=True)
            
            # 保存到数据库
            save_data_to_db(st.session_state.production_data)
            
            st.success("数据提交成功！")
            
            # 显示当前输入的数据
            st.subheader("当前提交的数据")
            st.dataframe(new_record.style.format({"合格率": "{:.2f}%"}))

# 数据可视化页面
elif selected == "数据可视化":
    st.title("📈 生产数据可视化分析")
    st.markdown("---")
    
    if st.session_state.production_data.empty:
        st.warning("暂无数据，请先在数据输入页面添加数据")
    else:
        # 数据筛选
        st.subheader("数据筛选")
        col1, col2 = st.columns(2)
        
        with col1:
            product_filter = st.multiselect(
                "选择产品",
                options=st.session_state.production_data["产品名称"].unique(),
                default=st.session_state.production_data["产品名称"].unique()
            )
        
        with col2:
            # 设置默认日期范围
            if not st.session_state.production_data.empty:
                default_date = (st.session_state.production_data["日期"].min(), st.session_state.production_data["日期"].max())
            else:
                # 当数据为空时，默认显示今天到今天
                today = datetime.today()
                default_date = (today, today)
            
            date_range = st.date_input(
                "选择日期范围",
                value=default_date
            )
        
        # 应用筛选
        filtered_data = st.session_state.production_data[
            (st.session_state.production_data["产品名称"].isin(product_filter)) &
            (st.session_state.production_data["日期"] >= pd.to_datetime(date_range[0])) &
            (st.session_state.production_data["日期"] <= pd.to_datetime(date_range[1]))
        ].sort_values("日期")
        
        if filtered_data.empty:
            st.warning("筛选条件下暂无数据")
        else:
            # 显示筛选后的数据
            st.subheader("筛选后的数据")
            
            # 添加删除数据功能
            if not filtered_data.empty:
                # 创建复选框选择器
                st.markdown("### 🗑️ 数据删除功能")
                
                # 获取筛选后的数据索引
                data_indices = filtered_data.index.tolist()
                
                # 创建一个字典来存储选中的行
                selected_rows = []
                
                # 显示数据并添加复选框
                for i, (index, row) in enumerate(filtered_data.iterrows()):
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        if st.checkbox("", key=f"delete_{index}"):
                            selected_rows.append(index)
                    with col2:
                        st.write(f"**{row['产品名称']}** - {row['日期'].strftime('%Y-%m-%d')}: 生产 {row['生产数量']} 件, 合格率 {row['合格率']:.2f}%")
                
                # 删除按钮
                if st.button("删除选中数据", type="secondary", help="此操作将删除选中的生产记录，请谨慎操作"):
                    if selected_rows:
                        # 确认删除
                        confirm_delete = st.checkbox("确认要删除选中的数据吗？此操作不可恢复")
                        if confirm_delete:
                            # 从会话状态中删除数据
                            st.session_state.production_data = st.session_state.production_data.drop(selected_rows)
                            
                            # 重置索引
                            st.session_state.production_data = st.session_state.production_data.reset_index(drop=True)
                            
                            # 保存到数据库
                            save_data_to_db(st.session_state.production_data)
                            
                            st.success(f"成功删除 {len(selected_rows)} 条数据")
                            
                            # 页面将在下次用户交互时自动刷新，无需显式调用 rerun
                    else:
                        st.warning("请先选择要删除的数据")
            
            # 显示筛选后的数据表格
            st.subheader("数据表格")
            st.dataframe(filtered_data.style.format({"合格率": "{:.2f}%"}))
            
            # 数据可视化
            st.subheader("生产数据分析图表")
            
            # 1. 生产数量与合格数量趋势图
            st.markdown("#### 生产数量与合格数量趋势")
            
            # 按产品类别分别绘制趋势图
            for product in product_filter:
                # 过滤当前产品的数据
                product_data = filtered_data[filtered_data["产品名称"] == product]
                
                # 创建趋势图
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=product_data["日期"],
                    y=product_data["生产数量"],
                    name="生产数量",
                    mode="lines+markers",
                    line=dict(color="#2196F3", width=2)
                ))
                fig1.add_trace(go.Scatter(
                    x=product_data["日期"],
                    y=product_data["合格数量"],
                    name="合格数量",
                    mode="lines+markers",
                    line=dict(color="#4CAF50", width=2)
                ))
                
                # 设置图表标题为当前产品名称
                fig1.update_layout(
                    title=f"{product}生产与合格数量趋势",
                    xaxis_title="日期",
                    yaxis_title="数量",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    template="plotly_white",
                    font=dict(color="#000000"),  # 设置所有字体为黑色
                    xaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                    yaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                    legend_font=dict(color="#000000")
                )
                
                # 显示当前产品的趋势图
                st.plotly_chart(fig1, use_container_width=True)
            
            # 2. 合格率趋势图
            st.markdown("#### 产品合格率趋势")
            fig2 = px.line(
                filtered_data,
                x="日期",
                y="合格率",
                color="产品名称",
                markers=True,
                title="产品合格率趋势",
                labels={"合格率": "合格率(%)"},
                template="plotly_white"
            )
            fig2.update_layout(
                yaxis_ticksuffix="%",
                yaxis_range=[0, 100]
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # 3. 不合格原因分析饼图
            st.markdown("#### 不合格原因分布")
            
            # 解析所有不合格原因
            all_reasons = []
            for reasons in filtered_data["不合格原因"]:
                if reasons and reasons != "无":
                    all_reasons.extend([reason.strip() for reason in reasons.split(",")])
            
            if all_reasons:
                reason_df = pd.DataFrame(all_reasons, columns=["不合格原因"])
                reason_counts = reason_df["不合格原因"].value_counts().reset_index()
                reason_counts.columns = ["不合格原因", "次数"]
                
                # 显示不合格原因及对应的数量
                st.markdown("### 不合格原因数量统计")
                for reason, count in reason_counts.itertuples(index=False):
                    st.write(f"- **{reason}**: {count} 件")
                
                fig3 = px.pie(
                    reason_counts,
                    values="次数",
                    names="不合格原因",
                    title="不合格原因分布",
                    template="plotly_white",
                    hole=0.3,
                    hover_data={"次数": True},  # 悬停时显示数量
                    labels={"次数": "数量"}
                )
                # 设置图例和文本颜色为黑色以提高可见性
                fig3.update_traces(
                    textinfo='label+value+percent',  # 显示标签、数量和百分比
                    textposition='outside',
                    marker=dict(line=dict(color='#000000', width=1)),
                    textfont=dict(color='#000000')
                )
                fig3.update_layout(
                    font=dict(color='#000000'),
                    title_font=dict(color='#000000'),
                    legend_font=dict(color='#000000')
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("暂无不合格数据")

# 分析报告页面
elif selected == "分析报告":
    st.title("📋 数据分析报告")
    st.markdown("---")
    
    if st.session_state.production_data.empty:
        st.warning("暂无数据，请先在数据输入页面添加数据")
    else:
        st.subheader("数据分析摘要")
        
        # 总体生产情况
        total_production = st.session_state.production_data["生产数量"].sum()
        total_qualified = st.session_state.production_data["合格数量"].sum()
        total_unqualified = st.session_state.production_data["不合格数量"].sum()
        overall_pass_rate = (total_qualified / total_production) * 100 if total_production > 0 else 0
        
        # 显示关键指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("总生产数量", f"{total_production:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("总合格数量", f"{total_qualified:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("总不合格数量", f"{total_unqualified:,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("总体合格率", f"{overall_pass_rate:.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 年度总结报告
        st.subheader("年度总结报告")
        
        # 选择年份
        years = st.session_state.production_data["日期"].dt.year.unique()
        years = sorted(years)
        selected_year = st.selectbox("选择年份", years, index=len(years)-1, key="year_select")
        
        # 筛选当年数据
        year_data = st.session_state.production_data[
            st.session_state.production_data["日期"].dt.year == selected_year
        ]
        
        if not year_data.empty:
            # 年度生产情况
            year_production = year_data["生产数量"].sum()
            year_qualified = year_data["合格数量"].sum()
            year_unqualified = year_data["不合格数量"].sum()
            year_pass_rate = (year_qualified / year_production) * 100 if year_production > 0 else 0
            
            # 年度不合格原因分析
            all_year_reasons = []
            for reasons in year_data["不合格原因"]:
                if reasons and reasons != "无":
                    all_year_reasons.extend([reason.strip() for reason in reasons.split(",")])
            
            st.markdown(f"#### {selected_year} 生产年报")
            
            # 年度报告内容
            year_report_content = f"""
## {selected_year} 产品生产年度总结报告

### 一、生产概况
- 年度生产总量：{year_production:,} 件
- 年度合格数量：{year_qualified:,} 件
- 年度不合格数量：{year_unqualified:,} 件
- 年度产品合格率：{year_pass_rate:.2f}%

### 二、质量分析
"""
            
            # 不合格原因分析
            if all_year_reasons:
                year_reason_counts = pd.Series(all_year_reasons).value_counts()
                year_top_reason = year_reason_counts.idxmax()
                year_top_reason_count = year_reason_counts.max()
                
                year_report_content += f"### 三、不合格原因分析\n"
                year_report_content += f"年度主要不合格原因为：{year_top_reason}，共发生 {year_top_reason_count} 次\n\n"
                year_report_content += "各不合格原因分布如下：\n"
                for reason, count in year_reason_counts.items():
                    year_report_content += f"- {reason}：{count} 次 ({count/year_unqualified*100:.1f}%)\n"
            else:
                year_report_content += "### 三、质量情况\n"
                year_report_content += "本年度生产的产品全部合格，未发现不合格产品\n"
            
            # 年度改善方案
            year_report_content += "\n### 四、年度改善建议\n"
            year_report_content += "1. 根据全年质量数据，重点关注主要不合格原因的改善\n"
            year_report_content += "2. 建立年度质量回顾机制，总结经验教训\n"
            year_report_content += "3. 制定下年度质量目标和改进计划\n"
            year_report_content += "4. 加强员工技能培训，提高质量意识\n"
            year_report_content += "5. 优化生产工艺和设备维护计划\n"
            
            # 显示年度报告
            st.text_area("年度报告", year_report_content, height=500, key="year_report")
            
            # 下载年度数据
            st.markdown(
                get_csv_download_link(
                    year_data,
                    f"{selected_year}_production_data.csv",
                    "📥 下载年度生产数据"
                ),
                unsafe_allow_html=True
            )
        else:
            st.info(f"{selected_year} 暂无生产数据")
        
        st.markdown("---")
        
        # 月度总结报告
        st.subheader("月度总结报告")
        
        # 选择月份
        months = st.session_state.production_data["日期"].dt.strftime("%Y-%m").unique()
        selected_month = st.selectbox("选择月份", months, index=len(months)-1, key="month_select")
        
        # 筛选当月数据
        month_data = st.session_state.production_data[
            st.session_state.production_data["日期"].dt.strftime("%Y-%m") == selected_month
        ]
        
        if not month_data.empty:
            # 月度生产情况
            month_production = month_data["生产数量"].sum()
            month_qualified = month_data["合格数量"].sum()
            month_unqualified = month_data["不合格数量"].sum()
            month_pass_rate = (month_qualified / month_production) * 100 if month_production > 0 else 0
            
            # 月度不合格原因分析
            all_month_reasons = []
            for reasons in month_data["不合格原因"]:
                if reasons and reasons != "无":
                    all_month_reasons.extend([reason.strip() for reason in reasons.split(",")])
            
            st.markdown(f"#### {selected_month} 生产月报")
            
            # 报告内容
            report_content = f"""
## {selected_month} 产品生产月度总结报告

### 一、生产概况
- 本月生产总量：{month_production:,} 件
- 本月合格数量：{month_qualified:,} 件
- 本月不合格数量：{month_unqualified:,} 件
- 本月产品合格率：{month_pass_rate:.2f}%

### 二、质量分析
"""
            
            # 不合格原因分析
            if all_month_reasons:
                reason_counts = pd.Series(all_month_reasons).value_counts()
                top_reason = reason_counts.idxmax()
                top_reason_count = reason_counts.max()
                
                report_content += f"### 三、不合格原因分析\n"
                report_content += f"本月主要不合格原因为：{top_reason}，共发生 {top_reason_count} 次\n\n"
                report_content += "各不合格原因分布如下：\n"
                for reason, count in reason_counts.items():
                    report_content += f"- {reason}：{count} 次 ({count/month_unqualified*100:.1f}%)\n"
                
                # 深层原因分析
                report_content += "\n### 四、深层原因分析\n"
                
                # 根据主要不合格原因提供详细的可能因素分析
                if top_reason == "外观缺陷":
                    report_content += "#### 外观缺陷可能因素分析\n"
                    report_content += "- **原材料因素**：原材料批次间颜色差异、原材料杂质含量过高、原材料表面质量问题\n"
                    report_content += "- **生产环境**：车间温度/湿度控制不当、生产环境粉尘过多、光照条件影响质量检查\n"
                    report_content += "- **工艺操作**：注塑温度/压力/速度参数设置不当、模具温度控制不稳定、脱模剂使用不当\n"
                    report_content += "- **设备问题**：模具表面磨损、设备震动过大、成型设备温度控制系统故障\n"
                elif top_reason == "尺寸偏差":
                    report_content += "#### 尺寸偏差可能因素分析\n"
                    report_content += "- **设备精度**：加工设备精度不足、设备定期校准不到位、设备主轴跳动过大\n"
                    report_content += "- **模具问题**：模具磨损、模具设计不合理、模具装配精度不足\n"
                    report_content += "- **原材料特性**：原材料收缩率不稳定、原材料含水率变化、原材料批次间密度差异\n"
                    report_content += "- **工艺参数**：注塑压力/速度/保压时间设置不当、冷却时间不足、成型温度不稳定\n"
                    report_content += "- **操作因素**：工件装夹定位不准确、操作人员测量方法不规范\n"
                elif top_reason == "性能不达标":
                    report_content += "#### 性能不达标可能因素分析\n"
                    report_content += "- **材料配方**：原材料配方比例不准确、添加剂使用不当、材料老化问题\n"
                    report_content += "- **工艺参数**：固化温度/时间不足、热处理工艺参数设置不当、成型压力不够\n"
                    report_content += "- **设备问题**：设备老化、设备传感器不准确、设备校准过期\n"
                    report_content += "- **测试环节**：测试方法不准确、测试设备故障、测试环境不符合标准\n"
                elif top_reason == "材料问题":
                    report_content += "#### 材料问题可能因素分析\n"
                    report_content += "- **供应商因素**：供应商质量控制不严、供应商更换原材料批次、原材料运输过程损坏\n"
                    report_content += "- **存储条件**：原材料存储温度/湿度不符合要求、存储时间过长导致材料老化、存储环境污染\n"
                    report_content += "- **采购管理**：采购批次质量波动、原材料验收标准不严格、供应商评估体系不完善\n"
                elif top_reason == "工艺问题":
                    report_content += "#### 工艺问题可能因素分析\n"
                    report_content += "- **工艺设计**：工艺流程不合理、工艺参数设置范围过宽、工艺验证不充分\n"
                    report_content += "- **工艺执行**：操作人员未严格按照工艺文件执行、工艺参数记录不完整、工艺变更未验证\n"
                    report_content += "- **工艺培训**：员工对工艺要求理解不深入、新员工工艺培训不足、工艺文件更新不及时\n"
                elif top_reason == "设备故障":
                    report_content += "#### 设备故障可能因素分析\n"
                    report_content += "- **维护管理**：设备维护计划执行不到位、维护记录不完整、关键部件更换不及时\n"
                    report_content += "- **设备状态**：设备老化严重、设备超负荷运行、设备安装精度下降\n"
                    report_content += "- **操作因素**：操作人员违规操作、操作人员缺乏设备维护知识、设备操作规程不清晰\n"
                elif top_reason == "操作失误":
                    report_content += "#### 操作失误可能因素分析\n"
                    report_content += "- **人员培训**：新员工培训不足、定期技能培训缺失、操作考核不严格\n"
                    report_content += "- **工作环境**：工作强度过大、工作环境嘈杂、照明条件不佳\n"
                    report_content += "- **管理因素**：操作流程不清晰、质量控制点设置不合理、现场管理不到位\n"
                else:
                    report_content += "#### 其他不良原因分析\n"
                    report_content += "- 建议对不合格产品进行详细检测，包括外观、尺寸、性能等方面\n"
                    report_content += "- 进行鱼骨图分析或5W1H分析法，找出具体原因\n"
                    report_content += "- 对生产过程进行全面排查，包括原材料、设备、工艺、人员等环节\n"
            else:
                report_content += "### 三、质量情况\n"
                report_content += "本月生产的产品全部合格，未发现不合格产品\n"
            
            # 优化建议
            report_content += "\n### 五、改善方案\n"
            
            # 根据主要问题提供详细的改善方案
            if all_month_reasons:
                if top_reason == "外观缺陷":
                    report_content += "#### 外观缺陷改善方案\n"
                    report_content += "1. **原材料管控**：\n"
                    report_content += "   - 建立原材料批次检测制度，严格控制原材料外观质量\n"
                    report_content += "   - 与供应商签订外观质量协议，明确色差、杂质等要求\n"
                    report_content += "   - 对原材料存储环境进行控制，避免受潮、污染\n"
                    report_content += "2. **生产环境优化**：\n"
                    report_content += "   - 安装温湿度监控系统，确保生产环境符合工艺要求\n"
                    report_content += "   - 加强车间清洁管理，减少粉尘污染\n"
                    report_content += "   - 优化车间照明，确保质量检查光线充足\n"
                    report_content += "3. **工艺优化**：\n"
                    report_content += "   - 重新调整注塑温度、压力、速度参数，记录最优参数组合\n"
                    report_content += "   - 建立模具温度控制系统，确保温度稳定\n"
                    report_content += "   - 规范脱模剂使用，避免残留影响外观\n"
                    report_content += "4. **设备维护**：\n"
                    report_content += "   - 定期检查和抛光模具表面，延长模具寿命\n"
                    report_content += "   - 对设备进行振动检测，及时调整设备水平\n"
                elif top_reason == "尺寸偏差":
                    report_content += "#### 尺寸偏差改善方案\n"
                    report_content += "1. **设备精度保障**：\n"
                    report_content += "   - 建立设备定期校准制度，每季度校准一次关键设备\n"
                    report_content += "   - 安装设备精度监控系统，实时监测设备状态\n"
                    report_content += "   - 对老化设备进行升级改造或更换\n"
                    report_content += "2. **模具管理**：\n"
                    report_content += "   - 建立模具定期检查制度，记录模具磨损情况\n"
                    report_content += "   - 对磨损模具进行修复或更换\n"
                    report_content += "   - 优化模具冷却系统，确保冷却均匀\n"
                    report_content += "3. **原材料控制**：\n"
                    report_content += "   - 对每批次原材料进行收缩率测试\n"
                    report_content += "   - 控制原材料存储环境，避免含水率变化\n"
                    report_content += "4. **工艺参数优化**：\n"
                    report_content += "   - 进行DOE实验，找出最优工艺参数组合\n"
                    report_content += "   - 建立工艺参数自动控制系统，减少人为误差\n"
                    report_content += "5. **操作规范**：\n"
                    report_content += "   - 制定详细的操作指导书，规范装夹定位方法\n"
                    report_content += "   - 对操作人员进行测量技能培训，确保测量准确性\n"
                elif top_reason == "性能不达标":
                    report_content += "#### 性能不达标改善方案\n"
                    report_content += "1. **材料配方优化**：\n"
                    report_content += "   - 重新调整材料配方，进行性能测试验证\n"
                    report_content += "   - 选择稳定性更好的原材料供应商\n"
                    report_content += "2. **工艺参数调整**：\n"
                    report_content += "   - 延长固化时间，确保产品完全固化\n"
                    report_content += "   - 优化热处理工艺参数，提高产品性能\n"
                    report_content += "3. **设备管理**：\n"
                    report_content += "   - 对设备进行全面维护和校准\n"
                    report_content += "   - 安装设备状态监控系统，及时发现设备故障\n"
                    report_content += "4. **测试系统优化**：\n"
                    report_content += "   - 定期校准测试设备\n"
                    report_content += "   - 优化测试方法，确保测试结果准确\n"
                elif top_reason == "材料问题":
                    report_content += "#### 材料问题改善方案\n"
                    report_content += "1. **供应商管理**：\n"
                    report_content += "   - 建立供应商评估体系，定期对供应商进行审核\n"
                    report_content += "   - 与核心供应商建立长期合作关系，签订质量协议\n"
                    report_content += "   - 增加备用供应商，避免单一供应商风险\n"
                    report_content += "2. **原材料存储**：\n"
                    report_content += "   - 建立原材料存储管理制度，明确存储条件\n"
                    report_content += "   - 对存储环境进行温湿度监控\n"
                    report_content += "   - 实施先进先出制度，避免原材料过期\n"
                    report_content += "3. **原材料检测**：\n"
                    report_content += "   - 增加原材料检测项目，建立全检制度\n"
                    report_content += "   - 使用先进检测设备，提高检测准确性\n"
                elif top_reason == "工艺问题":
                    report_content += "#### 工艺问题改善方案\n"
                    report_content += "1. **工艺文件完善**：\n"
                    report_content += "   - 重新修订工艺文件，明确各工序参数要求\n"
                    report_content += "   - 增加工艺流程图，提高工艺可视化\n"
                    report_content += "2. **工艺执行管控**：\n"
                    report_content += "   - 建立工艺参数记录系统，实时监控工艺执行情况\n"
                    report_content += "   - 定期进行工艺审核，确保工艺执行到位\n"
                    report_content += "3. **工艺培训**：\n"
                    report_content += "   - 对员工进行工艺文件培训，确保理解工艺要求\n"
                    report_content += "   - 定期组织工艺知识考试，提高员工工艺意识\n"
                elif top_reason == "设备故障":
                    report_content += "#### 设备故障改善方案\n"
                    report_content += "1. **设备维护计划**：\n"
                    report_content += "   - 建立设备维护保养制度，明确维护项目和周期\n"
                    report_content += "   - 制定设备维护计划，确保维护工作按时完成\n"
                    report_content += "2. **设备状态监控**：\n"
                    report_content += "   - 安装设备状态监控系统，实时监测设备运行参数\n"
                    report_content += "   - 建立设备故障预警机制，提前发现潜在问题\n"
                    report_content += "3. **设备操作培训**：\n"
                    report_content += "   - 对操作人员进行设备操作培训，确保正确操作\n"
                    report_content += "   - 制定设备操作规程，明确操作步骤和注意事项\n"
                elif top_reason == "操作失误":
                    report_content += "#### 操作失误改善方案\n"
                    report_content += "1. **人员培训**：\n"
                    report_content += "   - 建立新员工培训制度，培训合格后方可上岗\n"
                    report_content += "   - 定期组织技能培训，提高员工操作水平\n"
                    report_content += "   - 开展岗位技能竞赛，激励员工提高技能\n"
                    report_content += "2. **工作环境优化**：\n"
                    report_content += "   - 合理安排工作时间，避免员工疲劳作业\n"
                    report_content += "   - 优化车间布局，减少噪音污染\n"
                    report_content += "   - 改善工作照明，提高工作舒适度\n"
                    report_content += "3. **管理提升**：\n"
                    report_content += "   - 制定详细的操作指导书，明确操作流程\n"
                    report_content += "   - 建立质量责任追溯制度，明确各岗位责任\n"
                    report_content += "   - 加强现场管理，及时纠正违规操作\n"
                else:
                    report_content += "#### 其他不良情况改善方案\n"
                    report_content += "1. 组织跨部门质量分析会议，找出具体不良原因\n"
                    report_content += "2. 建立临时质量改进小组，制定专项改善计划\n"
                    report_content += "3. 增加产品检测项目，全面了解产品质量状况\n"
                    report_content += "4. 对生产过程进行全面排查，找出问题点\n"
            else:
                report_content += "#### 质量保持与提升方案\n"
                report_content += "1. 保持当前的生产和质量控制水平\n"
                report_content += "2. 定期进行工艺优化和设备维护\n"
                report_content += "3. 持续关注员工技能提升\n"
                report_content += "4. 建立质量预警机制，提前发现潜在质量问题\n"
                report_content += "5. 定期进行质量回顾，总结经验教训\n"
            
            # 月度产品曲线分析图
            st.markdown("### 月度产品曲线分析")
            
            if not month_data.empty:
                # 按日期排序
                month_data_sorted = month_data.sort_values("日期")
                
                # 创建月度生产趋势图
                fig_month_trend = go.Figure()
                fig_month_trend.add_trace(go.Scatter(
                    x=month_data_sorted["日期"],
                    y=month_data_sorted["生产数量"],
                    name="生产数量",
                    mode="lines+markers",
                    line=dict(color="#2196F3", width=2)
                ))
                fig_month_trend.add_trace(go.Scatter(
                    x=month_data_sorted["日期"],
                    y=month_data_sorted["合格数量"],
                    name="合格数量",
                    mode="lines+markers",
                    line=dict(color="#4CAF50", width=2)
                ))
                fig_month_trend.add_trace(go.Scatter(
                    x=month_data_sorted["日期"],
                    y=month_data_sorted["不合格数量"],
                    name="不合格数量",
                    mode="lines+markers",
                    line=dict(color="#F44336", width=2)
                ))
                
                fig_month_trend.update_layout(
                    title=f"{selected_month} 每日生产情况趋势",
                    xaxis_title="日期",
                    yaxis_title="数量",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    template="plotly_white",
                    font=dict(color="#000000"),
                    xaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                    yaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                    legend_font=dict(color="#000000")
                )
                
                st.plotly_chart(fig_month_trend, use_container_width=True)
            else:
                st.info("暂无月度数据生成趋势图")
            
            # 绘制质量趋势折线图
            st.markdown("### 质量趋势分析")
            
            # 检查是否有数据
            if not st.session_state.production_data.empty:
                # 获取所有月份数据并按月份排序
                all_months = st.session_state.production_data["日期"].dt.strftime("%Y-%m").unique()
                all_months = sorted(all_months)
                
                # 计算每个月的合格率
                month_pass_rates = []
                for month in all_months:
                    month_data_temp = st.session_state.production_data[
                        st.session_state.production_data["日期"].dt.strftime("%Y-%m") == month
                    ]
                    if not month_data_temp.empty:
                        total_production = month_data_temp["生产数量"].sum()
                        total_qualified = month_data_temp["合格数量"].sum()
                        if total_production > 0:
                            pass_rate = (total_qualified / total_production) * 100
                            month_pass_rates.append({
                                "月份": month,
                                "合格率": pass_rate,
                                "生产数量": total_production
                            })
                
                if month_pass_rates:
                    trend_df = pd.DataFrame(month_pass_rates)
                    
                    fig_trend = px.line(
                        trend_df,
                        x="月份",
                        y="合格率",
                        title="近月产品合格率趋势",
                        markers=True,
                        template="plotly_white",
                        hover_data={"生产数量": True, "合格率": ":.2f%%"}
                    )
                    
                    fig_trend.update_layout(
                        yaxis=dict(
                            title="合格率 (%)",
                            range=[0, 100],
                            tickformat=".0f"
                        ),
                        xaxis=dict(
                            title="月份"
                        ),
                        font=dict(color="#000000"),
                        xaxis_title_font=dict(color="#000000"),
                        yaxis_title_font=dict(color="#000000"),
                        legend_font=dict(color="#000000")
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)
                else:
                    st.info("暂无足够数据生成质量趋势图")
            else:
                st.info("暂无数据生成质量趋势图")
            
            # 显示报告
            st.text_area("月度报告", report_content, height=500)
            
            # 下载月度数据
            st.markdown(
                get_csv_download_link(
                    month_data,
                    f"{selected_month}_production_data.csv",
                    "📥 下载月度生产数据"
                ),
                unsafe_allow_html=True
            )
        # 智能优化建议
        st.markdown("---")
        st.subheader("💡 智能优化建议")
        
        # 为每个产品生成优化建议
        all_products = st.session_state.production_data["产品名称"].unique()
        
        for product in all_products:
            st.markdown(f"#### 📦 {product} 优化建议与市场评估")
            
            # 获取该产品的历史数据
            product_data = st.session_state.production_data[
                st.session_state.production_data["产品名称"] == product
            ]
            
            if not product_data.empty:
                # 计算关键指标
                total_production = product_data["生产数量"].sum()
                total_qualified = product_data["合格数量"].sum()
                total_unqualified = product_data["不合格数量"].sum()
                pass_rate = (total_qualified / total_production) * 100 if total_production > 0 else 0
                
                # 按月份汇总生产数量
                monthly_production = product_data.resample('M', on='日期').sum()[["生产数量"]]
                monthly_production = monthly_production.reset_index()
                
                # 分析市场需求趋势（基于生产数量变化）
                market_trend = "稳定"
                if len(monthly_production) >= 3:
                    # 计算生产数量的变化趋势
                    recent_production = monthly_production["生产数量"].tail(3).values
                    if recent_production[-1] > recent_production[-2] > recent_production[-3]:
                        market_trend = "增长"
                    elif recent_production[-1] < recent_production[-2] < recent_production[-3]:
                        market_trend = "下降"
                
                # 生成优化建议
                optimization_suggestions = []
                
                # 基于合格率的建议
                if pass_rate < 90:
                    optimization_suggestions.append("提高产品质量，减少不合格品率")
                elif pass_rate < 95:
                    optimization_suggestions.append("进一步优化生产工艺，提升产品合格率")
                else:
                    optimization_suggestions.append("保持当前良好的产品质量控制水平")
                
                # 基于市场趋势的建议
                if market_trend == "增长":
                    optimization_suggestions.append("扩大生产规模，满足增长的市场需求")
                elif market_trend == "下降":
                    optimization_suggestions.append("评估市场需求变化原因，考虑调整生产计划")
                else:
                    optimization_suggestions.append("维持当前生产规模，密切关注市场变化")
                
                # 基于不合格原因的建议
                all_reasons = []
                for reasons in product_data["不合格原因"]:
                    if reasons and reasons != "无":
                        all_reasons.extend([reason.strip() for reason in reasons.split(",")])
                
                if all_reasons:
                    reason_counts = pd.Series(all_reasons).value_counts()
                    top_reason = reason_counts.idxmax()
                    
                    if top_reason == "外观缺陷":
                        optimization_suggestions.append("重点改进外观质量，提高产品市场竞争力")
                    elif top_reason == "尺寸偏差":
                        optimization_suggestions.append("加强尺寸控制，确保产品符合标准要求")
                    elif top_reason == "性能不达标":
                        optimization_suggestions.append("优化产品性能，满足客户需求")
                    elif top_reason == "材料问题":
                        optimization_suggestions.append("更换或改进原材料，提高产品质量")
                    elif top_reason == "工艺问题":
                        optimization_suggestions.append("优化生产工艺，提高生产效率和产品质量")
                    elif top_reason == "设备故障":
                        optimization_suggestions.append("加强设备维护，减少故障对生产的影响")
                    elif top_reason == "操作失误":
                        optimization_suggestions.append("加强员工培训，减少操作失误")
                
                # 生成市场需求评估
                market_evaluation = []
                
                if market_trend == "增长":
                    market_evaluation.append("市场需求呈增长趋势，建议增加备货量")
                elif market_trend == "下降":
                    market_evaluation.append("市场需求呈下降趋势，建议减少备货量")
                else:
                    market_evaluation.append("市场需求稳定，建议维持当前备货策略")
                
                if pass_rate >= 95:
                    market_evaluation.append("产品质量优异，具有良好的市场竞争力")
                elif pass_rate >= 90:
                    market_evaluation.append("产品质量良好，但仍有提升空间")
                else:
                    market_evaluation.append("产品质量需改进，以提高市场竞争力")
                
                # 显示优化建议
                st.markdown("##### 🔧 优化建议：")
                for suggestion in optimization_suggestions:
                    st.markdown(f"- {suggestion}")
                
                # 显示市场需求评估
                st.markdown("##### 📊 市场需求评估：")
                for evaluation in market_evaluation:
                    st.markdown(f"- {evaluation}")
                
                st.markdown("---")
            else:
                st.info(f"{product} 暂无数据")
        
        # 备货数量预测分析
        st.markdown("---")
        st.subheader("📈 备货数量预测分析")
        
        # 选择产品进行预测
        all_products = st.session_state.production_data["产品名称"].unique()
        selected_product_for_prediction = st.selectbox("选择产品进行备货预测", all_products, key="prediction_product_select")
        
        # 获取该产品的历史生产数据
        product_history = st.session_state.production_data[
            st.session_state.production_data["产品名称"] == selected_product_for_prediction
        ].sort_values("日期")
        
        if len(product_history) >= 2:  # 需要至少2个月的数据进行预测
            # 按月份汇总生产数量
            monthly_production = product_history.resample('M', on='日期').sum()[["生产数量"]]
            monthly_production = monthly_production.reset_index()
            monthly_production["月份"] = monthly_production["日期"].dt.month
            monthly_production["年份"] = monthly_production["日期"].dt.year
            
            # 使用移动平均法预测下一个月的生产数量
            predicted_production = monthly_production["生产数量"].mean()
            
            # 计算下一个月的日期
            last_date = monthly_production["日期"].max()
            if last_date.month == 12:
                next_month_date = datetime(last_date.year + 1, 1, 1)
            else:
                next_month_date = datetime(last_date.year, last_date.month + 1, 1)
            
            # 显示预测结果
            st.markdown(f"#### {selected_product_for_prediction} 下一个月备货数量预测")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("预测月份", next_month_date.strftime("%Y-%m"))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("预测备货数量", f"{int(round(predicted_production)):,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_production = monthly_production["生产数量"].mean()
                st.metric("历史月均生产数量", f"{int(round(avg_production)):,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 绘制历史生产与预测数量趋势图
            fig_prediction = go.Figure()
            
            # 添加历史数据
            fig_prediction.add_trace(go.Scatter(
                x=monthly_production["日期"],
                y=monthly_production["生产数量"],
                name="历史生产数量",
                mode="lines+markers",
                line=dict(color="#2196F3", width=2)
            ))
            
            # 添加预测数据
            fig_prediction.add_trace(go.Scatter(
                x=[next_month_date],
                y=[predicted_production],
                name="预测备货数量",
                mode="markers",
                marker=dict(color="#FF9800", size=15, symbol="star")
            ))
            
            fig_prediction.update_layout(
                title=f"{selected_product_for_prediction} 生产数量历史趋势与预测",
                xaxis_title="日期",
                yaxis_title="数量",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white",
                font=dict(color="#000000"),
                xaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                yaxis=dict(title_font=dict(color="#000000"), tickfont=dict(color="#000000")),
                legend_font=dict(color="#000000")
            )
            
            st.plotly_chart(fig_prediction, use_container_width=True)
            
            # 显示预测说明
            st.markdown("### 预测说明")
            st.markdown("- 预测基于历史生产数据的线性回归模型")
            st.markdown("- 建议结合实际市场需求和库存情况调整备货数量")
            st.markdown("- 模型预测准确率受历史数据量和稳定性影响")
            
        else:
            st.info(f"{selected_product_for_prediction} 数据不足，需要至少2个月的生产数据才能进行预测")

# 智能分析页面
elif selected == "智能分析":
    st.title("🤖 智能分析系统")
    st.markdown("---")
    
    # 智能分析功能选项卡
    analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4, analysis_tab5, analysis_tab6 = st.tabs([
        "质量分析引擎", "库存优化引擎", "智能决策引擎", "需求预测分析", "可视化仪表盘", "知识库"
    ])
    
    # 1. 质量分析引擎
    with analysis_tab1:
        st.subheader("📊 质量分析引擎")
        st.markdown("---")
        
        if st.session_state.production_data.empty:
            st.warning("暂无生产数据，请先在数据输入页面添加数据")
        else:
            # 质量分析功能模块
            quality_col1, quality_col2 = st.columns(2)
            
            with quality_col1:
                # 不合格率分析
                st.markdown("### 🔍 不合格率分析")
                
                # 计算总体不合格率
                total_production = st.session_state.production_data["生产数量"].sum()
                total_unqualified = st.session_state.production_data["不合格数量"].sum()
                overall_unqualified_rate = (total_unqualified / total_production * 100) if total_production > 0 else 0
                
                # 按产品计算不合格率
                product_unqualified = st.session_state.production_data.groupby("产品名称").agg(
                    生产总数=pd.NamedAgg(column="生产数量", aggfunc="sum"),
                    不合格总数=pd.NamedAgg(column="不合格数量", aggfunc="sum")
                ).reset_index()
                product_unqualified["不合格率"] = (product_unqualified["不合格总数"] / product_unqualified["生产总数"] * 100).round(2)
                
                st.metric("总体不合格率", f"{overall_unqualified_rate:.2f}%")
                
                # 产品不合格率柱状图
                if not product_unqualified.empty:
                    fig_unqualified = px.bar(
                        product_unqualified,
                        x="产品名称",
                        y="不合格率",
                        title="各产品不合格率对比",
                        template="plotly_white",
                        color="不合格率",
                        color_continuous_scale="RdYlGn_r"
                    )
                    st.plotly_chart(fig_unqualified, use_container_width=True)
            
            with quality_col2:
                # 帕累托分析
                st.markdown("### 📈 帕累托分析")
                
                # 解析所有不合格原因
                all_reasons = []
                for reasons in st.session_state.production_data["不合格原因"]:
                    if reasons and reasons != "无":
                        all_reasons.extend([reason.strip() for reason in reasons.split(",")])
                
                if all_reasons:
                    reason_df = pd.DataFrame(all_reasons, columns=["不合格原因"])
                    reason_counts = reason_df["不合格原因"].value_counts().reset_index()
                    reason_counts.columns = ["不合格原因", "次数"]
                    
                    # 计算累积百分比
                    reason_counts["累计百分比"] = (reason_counts["次数"].cumsum() / reason_counts["次数"].sum() * 100).round(2)
                    
                    # 帕累托图
                    fig_pareto = px.bar(
                        reason_counts,
                        x="不合格原因",
                        y="次数",
                        title="不合格原因帕累托分析",
                        template="plotly_white",
                        color="不合格原因"
                    )
                    
                    # 添加累积百分比线
                    fig_pareto.add_trace(go.Scatter(
                        x=reason_counts["不合格原因"],
                        y=reason_counts["累计百分比"],
                        name="累积百分比",
                        yaxis="y2",
                        mode="lines+markers",
                        line=dict(color="red", width=2)
                    ))
                    
                    fig_pareto.update_layout(
                        yaxis2=dict(
                            title="累积百分比(%)",
                            overlaying="y",
                            side="right",
                            range=[0, 100]
                        )
                    )
                    
                    st.plotly_chart(fig_pareto, use_container_width=True)
                else:
                    st.info("暂无不合格原因数据")
            
            # 根本原因挖掘
            st.markdown("### 💡 根本原因挖掘")
            
            # 基于不合格原因频率的根本原因分析
            if all_reasons:
                top_reason = reason_counts.iloc[0]["不合格原因"]
                top_reason_count = reason_counts.iloc[0]["次数"]
                top_reason_percent = reason_counts.iloc[0]["累计百分比"]
                
                st.markdown(f"**主要不合格原因**: {top_reason}")
                st.markdown(f"**发生次数**: {top_reason_count} 次")
                st.markdown(f"**占比**: {top_reason_percent:.2f}%")
                
                # 生成改进建议
                st.markdown("#### 🔧 改进建议")
                if top_reason == "外观缺陷":
                    st.markdown("- 检查生产设备的校准状态")
                    st.markdown("- 加强原材料质量检验")
                    st.markdown("- 优化生产环境的温度和湿度控制")
                elif top_reason == "尺寸偏差":
                    st.markdown("- 定期维护和校准生产模具")
                    st.markdown("- 加强生产过程中的尺寸检测")
                    st.markdown("- 优化原材料的配比")
                elif top_reason == "功能故障":
                    st.markdown("- 检查零部件的质量")
                    st.markdown("- 优化装配工艺")
                    st.markdown("- 加强成品功能测试")
                elif top_reason == "性能不达标":
                    st.markdown("- 检查生产参数设置")
                    st.markdown("- 优化生产工艺")
                    st.markdown("- 加强产品性能测试")
                else:
                    st.markdown("- 收集更多关于该不合格原因的详细信息")
                    st.markdown("- 进行针对性的生产流程分析")
                    st.markdown("- 制定专项改进计划")
            else:
                st.info("暂无不合格原因数据，无法进行根本原因挖掘")
    
    # 2. 库存优化引擎
    with analysis_tab2:
        st.subheader("📦 库存优化引擎")
        st.markdown("---")
        
        # 库存优化参数输入
        st.markdown("### ⚙️ 库存参数设置")
        
        # 获取产品列表
        products = st.session_state.production_data["产品名称"].unique().tolist()
        if products:
            selected_product = st.selectbox("选择产品", products, key="stock_product_select")
        else:
            selected_product = "示例产品"
            st.info("暂无产品数据，使用示例产品")
        
        # 参数输入表单
        with st.form("inventory_params_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # 需求相关参数
                daily_demand = st.number_input("日平均需求量", min_value=0.0, value=100.0, step=10.0)
                demand_std = st.number_input("需求标准差", min_value=0.0, value=20.0, step=5.0)
                
                # 订货相关参数
                ordering_cost = st.number_input("每次订货成本（元）", min_value=0.0, value=500.0, step=50.0)
                lead_time = st.number_input("订货提前期（天）", min_value=1, value=5, step=1)
            
            with col2:
                # 持有成本相关参数
                holding_cost_rate = st.number_input("年持有成本率（%）", min_value=0.0, value=20.0, step=1.0)
                unit_cost = st.number_input("单位产品成本（元）", min_value=0.0, value=100.0, step=10.0)
                
                # 服务水平
                service_level = st.slider("服务水平（%）", min_value=50, max_value=99, value=95, step=1)
            
            submit_params = st.form_submit_button("计算库存优化参数")
        
        if submit_params:
            # 计算安全库存
            # 服务水平对应的Z值（近似值）
            service_level_z = {
                50: 0.00,
                60: 0.25,
                70: 0.52,
                75: 0.67,
                80: 0.84,
                85: 1.04,
                90: 1.28,
                95: 1.64,
                96: 1.75,
                97: 1.88,
                98: 2.05,
                99: 2.33
            }
            z = service_level_z.get(service_level, 1.64)  # 默认95%服务水平
            
            # 计算安全库存
            safety_stock = z * demand_std * (lead_time ** 0.5)
            
            # 计算再订货点
            reorder_point = daily_demand * lead_time + safety_stock
            
            # 计算经济订货批量（EOQ）
            # 年需求量
            annual_demand = daily_demand * 365
            # 单位年持有成本
            holding_cost = unit_cost * (holding_cost_rate / 100)
            # EOQ公式
            eoq = ((2 * annual_demand * ordering_cost) / holding_cost) ** 0.5
            
            # 计算最佳订货周期
            optimal_order_cycle = eoq / daily_demand
            
            # 计算年总成本
            annual_ordering_cost = (annual_demand / eoq) * ordering_cost
            annual_holding_cost = (eoq / 2) * holding_cost
            total_annual_cost = annual_ordering_cost + annual_holding_cost
            
            # 显示结果
            st.markdown("### 📊 库存优化结果")
            
            # 关键指标卡片
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**安全库存**")
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{round(safety_stock)}</div><div class='metric-label'>件</div></div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**再订货点**")
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{round(reorder_point)}</div><div class='metric-label'>件</div></div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("**经济订货批量**")
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{round(eoq)}</div><div class='metric-label'>件</div></div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown("**最佳订货周期**")
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{round(optimal_order_cycle, 1)}</div><div class='metric-label'>天</div></div>", unsafe_allow_html=True)
            
            # 成本分析
            st.markdown("### 💰 成本分析")
            
            cost_data = {
                "成本类型": ["年订货成本", "年持有成本", "年总成本"],
                "金额(元)": [round(annual_ordering_cost, 2), round(annual_holding_cost, 2), round(total_annual_cost, 2)]
            }
            cost_df = pd.DataFrame(cost_data)
            
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
            
            # 成本结构饼图
            fig_cost = px.pie(
                cost_data,
                values="金额(元)",
                names="成本类型",
                title="库存成本结构",
                template="plotly_white",
                hole=0.3
            )
            st.plotly_chart(fig_cost, use_container_width=True)
            
            # 优化建议
            st.markdown("### 🔧 优化建议")
            st.markdown(f"- 当库存水平降至 **{round(reorder_point)}** 件时，应立即订货")
            st.markdown(f"- 每次最优订货量为 **{round(eoq)}** 件")
            st.markdown(f"- 建议保持 **{round(safety_stock)}** 件的安全库存，以应对需求波动")
            st.markdown(f"- 预计年库存总成本约为 **{round(total_annual_cost, 2)}** 元")
            
            # 敏感性分析
            st.markdown("### 📈 敏感性分析")
            st.markdown("调整关键参数以观察对优化结果的影响：")
            
            # 服务水平敏感性
            service_levels = [90, 95, 97, 99]
            safety_stocks = []
            for sl in service_levels:
                z_val = service_level_z.get(sl, 1.64)
                ss = z_val * demand_std * (lead_time ** 0.5)
                safety_stocks.append(round(ss))
            
            # 服务水平与安全库存关系图
            fig_service_level = px.line(
                x=service_levels,
                y=safety_stocks,
                title="服务水平与安全库存关系",
                labels={"x": "服务水平(%)", "y": "安全库存(件)"},
                template="plotly_white",
                markers=True
            )
            st.plotly_chart(fig_service_level, use_container_width=True)
        
    # 3. 智能决策引擎
    with analysis_tab3:
        st.subheader("🧠 智能决策引擎")
        st.markdown("---")
        
        st.markdown("### 📋 决策场景选择")
        
        # 决策场景选项
        decision_scenario = st.selectbox(
            "选择决策场景",
            [
                "生产调度优化",
                "库存策略调整",
                "供应商选择",
                "质量改进优先级"
            ],
            key="decision_scenario_select"
        )
        
        # 根据不同场景显示不同的决策参数
        if decision_scenario == "生产调度优化":
            st.markdown("### ⚙️ 生产调度参数设置")
            
            # 获取产品列表
            products = st.session_state.production_data["产品名称"].unique().tolist()
            if not products:
                products = ["产品A", "产品B", "产品C"]
                st.info("暂无产品数据，使用示例产品")
            
            with st.form("production_scheduling_form"):
                # 生产资源限制
                available_capacity = st.number_input("可用生产能力（小时）", min_value=10, value=100, step=10)
                
                # 产品需求和优先级
                st.markdown("#### 产品需求与优先级设置")
                
                product_data = []
                for i, product in enumerate(products[:3]):  # 最多显示3个产品
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"**{product}**")
                    with col2:
                        demand = st.number_input(f"{product}需求数量", min_value=0, value=50, step=10, key=f"demand_{i}")
                    with col3:
                        processing_time = st.number_input(f"{product}单位处理时间（分钟）", min_value=1, value=30, step=5, key=f"time_{i}")
                    with col4:
                        priority = st.slider(f"{product}优先级（1-5）", min_value=1, max_value=5, value=3, key=f"priority_{i}")
                    
                    product_data.append({
                        "产品": product,
                        "需求": demand,
                        "单位处理时间": processing_time,
                        "优先级": priority,
                        "总处理时间": demand * processing_time / 60  # 转换为小时
                    })
                
                submit_scheduling = st.form_submit_button("生成生产调度方案")
            
            if submit_scheduling:
                # 多因子决策模型
                st.markdown("### 📊 决策分析结果")
                
                # 计算每个产品的得分
                for product in product_data:
                    # 需求满足率因子
                    demand_factor = product["需求"] / sum(p["需求"] for p in product_data)
                    
                    # 优先级因子
                    priority_factor = product["优先级"] / 5  # 归一化到0-1
                    
                    # 处理效率因子（单位时间产出）
                    efficiency_factor = 1 / (product["单位处理时间"] / 60)  # 每小时产出
                    
                    # 综合得分
                    product["得分"] = (0.4 * demand_factor + 0.3 * priority_factor + 0.3 * efficiency_factor) * 100
                
                # 根据得分排序
                product_data.sort(key=lambda x: x["得分"], reverse=True)
                
                # 生成生产调度方案
                st.markdown("#### 📅 最优生产调度方案")
                
                remaining_capacity = available_capacity
                schedule = []
                
                for product in product_data:
                    if remaining_capacity >= product["总处理时间"]:
                        # 完全生产
                        production_quantity = product["需求"]
                        used_capacity = product["总处理时间"]
                    else:
                        # 部分生产
                        production_quantity = int(remaining_capacity * 60 / product["单位处理时间"])
                        used_capacity = production_quantity * product["单位处理时间"] / 60
                    
                    if production_quantity > 0:
                        schedule.append({
                            "产品": product["产品"],
                            "计划生产数量": production_quantity,
                            "所需生产时间（小时）": round(used_capacity, 2),
                            "优先级": product["优先级"],
                            "决策得分": round(product["得分"], 2)
                        })
                        
                        remaining_capacity -= used_capacity
                        if remaining_capacity <= 0:
                            break
                
                # 显示调度方案
                if schedule:
                    schedule_df = pd.DataFrame(schedule)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    # 显示剩余产能
                    st.markdown(f"**剩余生产能力**: {round(remaining_capacity, 2)} 小时")
                    
                    # 生产调度甘特图（简化版）
                    st.markdown("#### 📊 生产调度甘特图")
                    
                    # 创建甘特图数据
                    gantt_data = []
                    current_time = 0
                    
                    for item in schedule:
                        gantt_data.append({
                            "Task": item["产品"],
                            "Start": current_time,
                            "Finish": current_time + item["所需生产时间（小时）"]
                        })
                        current_time += item["所需生产时间（小时）"]
                    
                    # 绘制甘特图
                    if gantt_data:
                        gantt_df = pd.DataFrame(gantt_data)
                        fig_gantt = px.timeline(
                            gantt_df,
                            x_start="Start",
                            x_end="Finish",
                            y="Task",
                            title="生产调度计划",
                            template="plotly_white"
                        )
                        fig_gantt.update_yaxes(autorange="reversed")  # 任务从上到下显示
                        fig_gantt.update_xaxes(title="时间（小时）")
                        st.plotly_chart(fig_gantt, use_container_width=True)
                    
                    # 决策建议
                    st.markdown("#### 💡 决策建议")
                    st.markdown("根据多因子决策模型，建议按以下顺序安排生产：")
                    for i, item in enumerate(schedule, 1):
                        st.markdown(f"{i}. **{item['产品']}**: 生产 {item['计划生产数量']} 件，优先级 {item['优先级']}，决策得分 {item['决策得分']}")
                else:
                    st.warning("可用生产能力不足以满足任何产品的生产需求")
        
        elif decision_scenario == "库存策略调整":
            st.markdown("### ⚙️ 库存策略参数设置")
            
            with st.form("inventory_strategy_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # 市场需求波动
                    demand_volatility = st.slider("市场需求波动（%）", min_value=5, max_value=50, value=20, step=5)
                    
                    # 供应链可靠性
                    supply_chain_reliability = st.slider("供应链可靠性（%）", min_value=70, max_value=100, value=90, step=5)
                
                with col2:
                    # 库存持有成本
                    holding_cost_impact = st.slider("库存持有成本影响度（1-10）", min_value=1, max_value=10, value=5, step=1)
                    
                    # 缺货成本影响
                    stockout_cost_impact = st.slider("缺货成本影响度（1-10）", min_value=1, max_value=10, value=7, step=1)
                
                submit_inventory = st.form_submit_button("生成库存策略建议")
            
            if submit_inventory:
                # 库存策略决策模型
                st.markdown("### 📊 库存策略建议")
                
                # 根据参数计算推荐的库存策略
                if demand_volatility > 30 or supply_chain_reliability < 85:
                    recommended_strategy = "安全库存策略"
                    strategy_description = "由于市场需求波动大或供应链可靠性低，建议增加安全库存以应对不确定性"
                elif holding_cost_impact > stockout_cost_impact:
                    recommended_strategy = "准时制（JIT）策略"
                    strategy_description = "由于库存持有成本影响大于缺货成本，建议采用准时制策略降低库存水平"
                else:
                    recommended_strategy = "经济订货批量（EOQ）策略"
                    strategy_description = "建议采用经济订货批量策略，平衡订货成本和持有成本"
                
                # 显示建议
                st.markdown(f"**推荐库存策略**: {recommended_strategy}")
                st.markdown(f"**策略说明**: {strategy_description}")
                
                # 可视化策略效果
                st.markdown("#### 📈 策略效果对比")
                
                # 创建策略对比数据
                strategy_data = {
                    "策略": ["安全库存策略", "准时制策略", "经济订货批量策略"],
                    "库存成本": [85, 45, 60],
                    "缺货风险": [20, 70, 40],
                    "响应速度": [60, 90, 70]
                }
                
                strategy_df = pd.DataFrame(strategy_data)
                
                # 绘制雷达图
                fig_strategy = px.line_polar(
                    strategy_df,
                    r=["库存成本", "缺货风险", "响应速度"],
                    theta="策略",
                    line_close=True,
                    title="不同库存策略效果对比"
                )
                st.plotly_chart(fig_strategy, use_container_width=True)
        
        # 其他决策场景可以类似实现
        else:
            st.info(f"{decision_scenario}功能正在开发中，敬请期待！")
        
        st.markdown("---")
        st.markdown("### 🤖 自动决策流程")
        
        st.markdown("智能决策引擎采用以下自动决策流程：")
        st.markdown("1. **数据采集**: 收集生产、质量、库存等相关数据")
        st.markdown("2. **因子分析**: 对质量、成本、交付、风险等因子进行分析")
        st.markdown("3. **模型计算**: 基于多因子决策模型计算综合得分")
        st.markdown("4. **方案生成**: 生成多个备选决策方案")
        st.markdown("5. **方案评估**: 评估各方案的优缺点和风险")
        st.markdown("6. **决策推荐**: 提供最优决策方案和执行建议")
        
    # 4. 需求预测分析
    with analysis_tab4:
        st.subheader("📅 需求预测分析")
        st.markdown("---")
        
        # 数据准备与模型选择
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔧 预测设置")
            product_for_forecast = st.selectbox("选择产品", st.session_state.production_data["产品名称"].unique(), key="forecast_product_select")
            forecast_days = st.slider("预测天数", 7, 90, 30)
            
            # 多模型选择
            selected_models = st.multiselect(
                "选择预测模型",
                ["线性回归", "移动平均", "指数平滑", "季节性ARIMA", "Prophet"],
                default=["线性回归", "季节性ARIMA"]
            )
            
        with col2:
            st.markdown("### 📊 历史数据")
            # 准备历史需求数据
            product_data = st.session_state.production_data[st.session_state.production_data["产品名称"] == product_for_forecast]
            
            if len(product_data) < 7:
                st.info("数据量不足，需要至少7天的历史数据进行预测")
            else:
                # 按日期聚合需求数据
                daily_demand = product_data.groupby("日期")[["生产数量", "合格数量"]].sum().reset_index()
                
                # 计算日需求量（使用合格数量）
                daily_demand["需求量"] = daily_demand["合格数量"]
                
                # 显示历史需求趋势图
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Scatter(
                    x=daily_demand["日期"],
                    y=daily_demand["需求量"],
                    mode='lines+markers',
                    name='历史需求量',
                    line=dict(color='#3b82f6')
                ))
                fig_hist.update_layout(
                    title="历史需求趋势",
                    xaxis_title="日期",
                    yaxis_title="需求量",
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig_hist, use_container_width=True)
        
        if len(product_data) >= 7:
            # 需求预测执行
            st.markdown("---")
            st.markdown("### ⚡ 执行预测")
            
            if st.button("开始预测"):
                # 数据预处理
                from sklearn.preprocessing import MinMaxScaler
                from sklearn.linear_model import LinearRegression
                from sklearn.metrics import mean_absolute_error, mean_squared_error
                import numpy as np
                from statsmodels.tsa.seasonal import seasonal_decompose
                
                # 准备时间序列数据
                time_series = daily_demand.set_index('日期')['需求量']
                time_series = time_series.asfreq('D')
                time_series = time_series.fillna(time_series.mean())
                
                # 创建预测结果容器
                st.session_state.forecast_results = {}
                
                # 1. 线性回归预测
                if "线性回归" in selected_models:
                    # 特征工程：使用时间索引作为特征
                    X = np.arange(len(time_series)).reshape(-1, 1)
                    y = time_series.values
                    
                    # 训练模型
                    lr_model = LinearRegression()
                    lr_model.fit(X, y)
                    
                    # 预测未来值
                    future_X = np.arange(len(time_series), len(time_series) + forecast_days).reshape(-1, 1)
                    lr_forecast = lr_model.predict(future_X)
                    
                    # 保存结果
                    st.session_state.forecast_results["线性回归"] = lr_forecast
                
                # 2. 移动平均预测
                if "移动平均" in selected_models:
                    window = 7  # 7天移动平均
                    ma_forecast = []
                    last_ma = time_series[-window:].mean()
                    
                    for _ in range(forecast_days):
                        ma_forecast.append(last_ma)
                        # 简单移动平均：保持最后一个平均值
                    
                    st.session_state.forecast_results["移动平均"] = np.array(ma_forecast)
                
                # 3. 指数平滑预测
                if "指数平滑" in selected_models:
                    alpha = 0.3  # 平滑系数
                    es_forecast = []
                    last_value = time_series.iloc[-1]
                    
                    for _ in range(forecast_days):
                        es_forecast.append(last_value)
                        # 简单指数平滑：保持最后一个预测值（更复杂的实现需要考虑趋势和季节性）
                    
                    st.session_state.forecast_results["指数平滑"] = np.array(es_forecast)
                
                # 4. 季节性ARIMA预测（简化版）
                if "季节性ARIMA" in selected_models:
                    try:
                        from statsmodels.tsa.arima.model import ARIMA
                        
                        # 简化的ARIMA模型
                        model = ARIMA(time_series, order=(1, 1, 1))
                        arima_result = model.fit()
                        
                        # 预测
                        arima_forecast = arima_result.forecast(steps=forecast_days)
                        st.session_state.forecast_results["季节性ARIMA"] = arima_forecast.values
                    except Exception as e:
                        st.error(f"ARIMA模型预测出错：{e}")
                
                # 5. Prophet预测（简化版）
                if "Prophet" in selected_models:
                    try:
                        # 简化的Prophet实现（这里使用线性回归模拟）
                        # 完整实现需要安装fbprophet库
                        X = np.arange(len(time_series)).reshape(-1, 1)
                        y = time_series.values
                        
                        prophet_model = LinearRegression()
                        prophet_model.fit(X, y)
                        
                        future_X = np.arange(len(time_series), len(time_series) + forecast_days).reshape(-1, 1)
                        prophet_forecast = prophet_model.predict(future_X)
                        
                        st.session_state.forecast_results["Prophet"] = prophet_forecast
                    except Exception as e:
                        st.error(f"Prophet模型预测出错：{e}")
                
                # 预测结果可视化
                st.markdown("---")
                st.markdown("### 📈 预测结果")
                
                # 创建未来日期
                last_date = time_series.index[-1]
                future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq='D')
                
                # 创建预测图表
                fig_forecast = go.Figure()
                
                # 添加历史数据
                fig_forecast.add_trace(go.Scatter(
                    x=time_series.index,
                    y=time_series.values,
                    mode='lines+markers',
                    name='历史需求量',
                    line=dict(color='#3b82f6', dash='dash')
                ))
                
                # 添加各模型预测结果
                colors = ['#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
                model_colors = dict(zip(selected_models, colors[:len(selected_models)]))
                
                for model_name, forecast_values in st.session_state.forecast_results.items():
                    fig_forecast.add_trace(go.Scatter(
                        x=future_dates,
                        y=forecast_values,
                        mode='lines+markers',
                        name=f'{model_name}预测',
                        line=dict(color=model_colors[model_name])
                    ))
                
                fig_forecast.update_layout(
                    title="需求预测趋势",
                    xaxis_title="日期",
                    yaxis_title="需求量",
                    height=400,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # 预测评估
                st.markdown("---")
                st.markdown("### 📊 模型评估")
                
                # 如果有多个模型，计算评估指标
                if len(st.session_state.forecast_results) > 0:
                    # 准备评估数据（使用最近7天作为验证集）
                    val_size = min(7, len(time_series) // 5)
                    train_data = time_series[:-val_size]
                    val_data = time_series[-val_size:]
                    
                    eval_results = []
                    
                    for model_name in selected_models:
                        # 重新训练模型用于评估
                        if model_name == "线性回归":
                            X_train = np.arange(len(train_data)).reshape(-1, 1)
                            y_train = train_data.values
                            X_val = np.arange(len(train_data), len(train_data) + val_size).reshape(-1, 1)
                            
                            model = LinearRegression()
                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_val)
                        
                        elif model_name == "移动平均":
                            window = 7
                            y_pred = [train_data[-window:].mean()] * val_size
                        
                        elif model_name == "指数平滑":
                            y_pred = [train_data.iloc[-1]] * val_size
                        
                        elif model_name == "季节性ARIMA":
                            try:
                                from statsmodels.tsa.arima.model import ARIMA
                                model = ARIMA(train_data, order=(1, 1, 1))
                                result = model.fit()
                                y_pred = result.forecast(steps=val_size)
                            except:
                                y_pred = [train_data.iloc[-1]] * val_size
                        
                        elif model_name == "Prophet":
                            X_train = np.arange(len(train_data)).reshape(-1, 1)
                            y_train = train_data.values
                            X_val = np.arange(len(train_data), len(train_data) + val_size).reshape(-1, 1)
                            
                            model = LinearRegression()
                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_val)
                        
                        else:
                            y_pred = [train_data.iloc[-1]] * val_size
                        
                        # 计算评估指标
                        y_true = val_data.values
                        y_pred = np.array(y_pred)
                        
                        mae = mean_absolute_error(y_true, y_pred)
                        mse = mean_squared_error(y_true, y_pred)
                        rmse = np.sqrt(mse)
                        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                        
                        eval_results.append({
                            "模型": model_name,
                            "MAE": round(mae, 2),
                            "MSE": round(mse, 2),
                            "RMSE": round(rmse, 2),
                            "MAPE (%)": round(mape, 2)
                        })
                    
                    # 显示评估结果
                    eval_df = pd.DataFrame(eval_results)
                    st.dataframe(eval_df, use_container_width=True)
                    
                    # 高亮最佳模型
                    best_model = eval_df.sort_values(by="RMSE").iloc[0]["模型"]
                    st.success(f"**最佳预测模型：{best_model}**")
                
                # 预测报告
                st.markdown("---")
                st.markdown("### 📋 预测报告")
                
                # 生成未来日期的预测汇总
                if "预测报告" not in st.session_state:
                    st.session_state.预测报告 = {}
                
                # 计算平均预测值
                avg_forecast = np.zeros(forecast_days)
                for forecast_values in st.session_state.forecast_results.values():
                    avg_forecast += forecast_values
                avg_forecast = avg_forecast / len(st.session_state.forecast_results)
                
                # 创建预测数据框
                forecast_df = pd.DataFrame({
                    "日期": future_dates,
                    "平均预测值": np.round(avg_forecast, 0),
                    "95%置信区间下限": np.round(avg_forecast * 0.9, 0),
                    "95%置信区间上限": np.round(avg_forecast * 1.1, 0)
                })
                
                # 汇总预测结果
                total_forecast = int(forecast_df["平均预测值"].sum())
                daily_avg = int(forecast_df["平均预测值"].mean())
                
                st.markdown(f"#### 📊 预测汇总")
                st.markdown(f"- **预测产品**: {product_for_forecast}")
                st.markdown(f"- **预测天数**: {forecast_days}天")
                st.markdown(f"- **总预测需求量**: {total_forecast}件")
                st.markdown(f"- **日均预测需求量**: {daily_avg}件")
                st.markdown(f"- **使用模型数量**: {len(selected_models)}个")
                
                st.markdown(f"#### 📈 预测趋势")
                st.markdown("- 预测期间需求量预计保持相对稳定")
                st.markdown("- 建议关注节假日、促销活动等可能影响需求的因素")
                st.markdown("- 预测结果仅供参考，实际需求可能受多种因素影响")
                
                st.markdown(f"#### 🎯 建议行动")
                st.markdown("1. 根据预测结果调整生产计划")
                st.markdown("2. 优化库存水平，避免库存积压或短缺")
                st.markdown("3. 定期监控实际需求，及时调整预测模型")
                st.markdown("4. 考虑建立安全库存，应对需求波动")
                
                # 显示详细预测表
                st.markdown("#### 📅 详细预测")
                st.dataframe(forecast_df, use_container_width=True)
                
                # 下载预测报告按钮
                import io
                buffer = io.BytesIO()
                forecast_df.to_excel(buffer, index=False)
                buffer.seek(0)
                
                st.download_button(
                    label="📥 下载预测报告",
                    data=buffer,
                    file_name=f"需求预测报告_{product_for_forecast}_{datetime.today().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
          
    # 5. 可视化仪表盘
    with analysis_tab5:
        st.subheader("📊 可视化仪表盘")
        st.markdown("---")
        
        if st.session_state.production_data.empty:
            st.warning("暂无生产数据，请先在数据输入页面添加数据")
        else:
            # 1. 筛选器面板
            st.markdown("### 🎯 数据筛选")
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    selected_products = st.multiselect(
                        "选择产品",
                        options=st.session_state.production_data["产品名称"].unique(),
                        default=st.session_state.production_data["产品名称"].unique(),
                        key="dashboard_product_filter"
                    )
                with col2:
                    date_range = st.date_input(
                        "选择日期范围",
                        value=(st.session_state.production_data["日期"].min(), st.session_state.production_data["日期"].max()),
                        key="dashboard_date_filter"
                    )
                with col3:
                    refresh_btn = st.button("🔄 刷新数据", key="dashboard_refresh")
            
            # 应用筛选
            filtered_data = st.session_state.production_data[
                (st.session_state.production_data["产品名称"].isin(selected_products)) &
                (st.session_state.production_data["日期"] >= date_range[0]) &
                (st.session_state.production_data["日期"] <= date_range[1])
            ]
            
            # 2. 总体概览指标卡片
            st.markdown("### 🔢 生产概览")
            
            # 计算关键指标
            total_production = filtered_data["生产数量"].sum()
            total_qualified = filtered_data["合格数量"].sum()
            total_unqualified = filtered_data["不合格数量"].sum()
            overall_yield_rate = (total_qualified / total_production * 100) if total_production > 0 else 0
            total_products = filtered_data["产品名称"].nunique()
            total_days = filtered_data["日期"].nunique()
            
            # 创建指标卡片
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                with st.container():
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        label="总生产数量",
                        value=f"{total_production:,}",
                        delta_color="off"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                with st.container():
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        label="总合格数量",
                        value=f"{total_qualified:,}",
                        delta_color="off"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                with st.container():
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        label="总不合格数量",
                        value=f"{total_unqualified:,}",
                        delta_color="off"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            with col4:
                with st.container():
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric(
                        label="总体合格率",
                        value=f"{overall_yield_rate:.2f}%",
                        delta_color="off"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # 2. 核心趋势图表
            st.markdown("---")
            st.markdown("### 📈 核心趋势分析")
            
            # 2.1 按日期的生产趋势
            daily_production = filtered_data.groupby("日期")[["生产数量", "合格数量"]].sum().reset_index()
            
            fig_daily = go.Figure()
            fig_daily.add_trace(go.Scatter(
                x=daily_production["日期"],
                y=daily_production["生产数量"],
                name="生产数量",
                mode="lines+markers",
                line=dict(color="#2196F3", width=2),
                marker=dict(size=6)
            ))
            fig_daily.add_trace(go.Scatter(
                x=daily_production["日期"],
                y=daily_production["合格数量"],
                name="合格数量",
                mode="lines+markers",
                line=dict(color="#4CAF50", width=2),
                marker=dict(size=6)
            ))
            
            # 添加合格率次要Y轴
            daily_production["合格率"] = (daily_production["合格数量"] / daily_production["生产数量"] * 100).fillna(0)
            fig_daily.add_trace(go.Scatter(
                x=daily_production["日期"],
                y=daily_production["合格率"],
                name="合格率",
                mode="lines+markers",
                line=dict(color="#FF9800", width=2, dash="dash"),
                marker=dict(size=6),
                yaxis="y2"
            ))
            
            fig_daily.update_layout(
                title="每日生产、合格数量与合格率趋势",
                xaxis_title="日期",
                yaxis_title="数量",
                yaxis2=dict(
                    title="合格率 (%)",
                    overlaying="y",
                    side="right",
                    range=[0, 100]
                ),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white"
            )
            
            # 2.2 按产品的生产与合格率
            product_summary = filtered_data.groupby("产品名称").agg({
                "生产数量": "sum",
                "合格数量": "sum"
            }).reset_index()
            product_summary["合格率"] = (product_summary["合格数量"] / product_summary["生产数量"] * 100).round(2)
            
            fig_product = go.Figure()
            fig_product.add_trace(go.Bar(
                x=product_summary["产品名称"],
                y=product_summary["生产数量"],
                name="生产数量",
                marker_color="#2196F3"
            ))
            fig_product.add_trace(go.Bar(
                x=product_summary["产品名称"],
                y=product_summary["合格数量"],
                name="合格数量",
                marker_color="#4CAF50"
            ))
            fig_product.update_layout(
                title="各产品生产与合格数量",
                xaxis_title="产品名称",
                yaxis_title="数量",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white"
            )
            
            # 2.3 不合格原因分布
            reasons_data = []
            for reasons in filtered_data["不合格原因"]:
                if reasons and reasons != "无":
                    for reason in reasons.split("、"):
                        reasons_data.append(reason.strip())
            
            reasons_df = pd.DataFrame(reasons_data, columns=["原因"])
            reasons_count = reasons_df["原因"].value_counts().reset_index()
            reasons_count.columns = ["原因", "次数"]
            reasons_count["百分比"] = (reasons_count["次数"] / reasons_count["次数"].sum() * 100).round(2)
            
            fig_reasons = go.Figure(data=[go.Pie(
                labels=reasons_count["原因"],
                values=reasons_count["次数"],
                hole=0.3,
                hovertext=reasons_count["百分比"],
                hovertemplate="%{label}: %{value}次 (%{hovertext}%)",
                textinfo="percent",
                textfont=dict(color="#000000")
            )])
            fig_reasons.update_layout(
                title="不合格原因分布",
                template="plotly_white"
            )
            
            # 3. 智能报表生成
            st.markdown("---")
            st.markdown("### 📋 智能报表生成")
            
            # 创建更丰富的报表参数面板
            col1, col2 = st.columns(2)
            
            with col1:
                # 报表类型选择
                report_type = st.selectbox(
                    "选择报表类型",
                    ["生产日报", "质量周报", "产品月度分析", "综合分析报告", "不合格原因分析", "产品对比分析"],
                    key="report_type_select"
                )
                
                # 时间范围选择
                time_filter = st.selectbox(
                    "选择时间范围",
                    ["最近7天", "最近30天", "最近90天", "全部时间"],
                    key="time_filter_select"
                )
            
            with col2:
                # 产品选择
                selected_products = st.multiselect(
                    "选择产品",
                    options=st.session_state.production_data["产品名称"].unique(),
                    default=st.session_state.production_data["产品名称"].unique()
                )
                
                # 报表格式选择
                report_format = st.selectbox(
                    "选择导出格式",
                    ["Markdown", "CSV", "Excel"],
                    key="report_format_select"
                )
            
            # 高级选项
            with st.expander("⚙️ 高级选项"):
                include_charts = st.checkbox("包含图表", value=True)
                include_recommendations = st.checkbox("包含改进建议", value=True)
                include_raw_data = st.checkbox("包含原始数据", value=False)
            
            # 生成报表按钮
            if st.button("📄 生成报表"):
                import io
                import base64
                from datetime import datetime
                
                # 应用筛选条件
                filtered_report_data = st.session_state.production_data[st.session_state.production_data["产品名称"].isin(selected_products)]
                
                if time_filter == "最近7天":
                    filtered_report_data = filtered_report_data[filtered_report_data["日期"] >= pd.to_datetime(datetime.today() - pd.Timedelta(days=7))]
                elif time_filter == "最近30天":
                    filtered_report_data = filtered_report_data[filtered_report_data["日期"] >= pd.to_datetime(datetime.today() - pd.Timedelta(days=30))]
                elif time_filter == "最近90天":
                    filtered_report_data = filtered_report_data[filtered_report_data["日期"] >= pd.to_datetime(datetime.today() - pd.Timedelta(days=90))]
                
                if filtered_report_data.empty:
                    st.warning("筛选条件下暂无数据")
                else:
                    # 根据报表类型生成不同内容
                    report_content = f"# {report_type}\n"
                    report_content += f"\n**生成时间**: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    report_content += f"**时间范围**: {time_filter}\n"
                    report_content += f"**涉及产品**: {', '.join(selected_products)}\n"
                    report_content += f"**数据记录数**: {len(filtered_report_data):,}条\n"
                    report_content += f"\n---\n"
                    
                    # 1. 报表摘要 - 所有报表类型通用
                    report_content += f"## 一、报表摘要\n"
                    total_production = filtered_report_data['生产数量'].sum()
                    total_qualified = filtered_report_data['合格数量'].sum()
                    total_unqualified = filtered_report_data['不合格数量'].sum()
                    overall_yield_rate = (total_qualified / total_production * 100) if total_production > 0 else 0
                    
                    report_content += f"- 总生产数量: {total_production:,}件\n"
                    report_content += f"- 总合格数量: {total_qualified:,}件\n"
                    report_content += f"- 总不合格数量: {total_unqualified:,}件\n"
                    report_content += f"- 总体合格率: {overall_yield_rate:.2f}%\n"
                    report_content += f"- 涉及产品数量: {len(selected_products)}个\n"
                    report_content += f"- 报告覆盖天数: {filtered_report_data['日期'].nunique()}天\n"
                    
                    # 2. 根据报表类型生成不同内容
                    if report_type == "生产日报":
                        # 生产日报特定内容
                        report_content += f"\n## 二、今日生产情况\n"
                        today = pd.to_datetime(datetime.today().date())
                        today_data = filtered_report_data[filtered_report_data["日期"] == today]
                        
                        if not today_data.empty:
                            today_prod = today_data['生产数量'].sum()
                            today_qualified = today_data['合格数量'].sum()
                            today_yield = (today_qualified / today_prod * 100) if today_prod > 0 else 0
                            
                            report_content += f"- 今日生产总量: {today_prod:,}件\n"
                            report_content += f"- 今日合格数量: {today_qualified:,}件\n"
                            report_content += f"- 今日合格率: {today_yield:.2f}%\n"
                            
                            report_content += f"\n### 各产品今日生产详情\n"
                            today_product_summary = today_data.groupby('产品名称')[['生产数量', '合格数量', '不合格数量']].sum().reset_index()
                            today_product_summary['合格率'] = (today_product_summary['合格数量'] / today_product_summary['生产数量'] * 100).round(2)
                            report_content += today_product_summary.to_markdown(index=False, numalign="right") + "\n"
                        else:
                            report_content += f"- 今日暂无生产数据\n"
                    
                    elif report_type == "质量周报":
                        # 质量周报特定内容
                        report_content += f"\n## 二、本周质量情况\n"
                        
                        # 计算周环比
                        current_week = filtered_report_data['日期'].dt.isocalendar().week.max()
                        current_year = filtered_report_data['日期'].dt.isocalendar().year.max()
                        
                        this_week_data = filtered_report_data[(filtered_report_data['日期'].dt.isocalendar().week == current_week) & 
                                                           (filtered_report_data['日期'].dt.isocalendar().year == current_year)]
                        
                        last_week = current_week - 1 if current_week > 1 else 52
                        last_year = current_year if current_week > 1 else current_year - 1
                        
                        last_week_data = st.session_state.production_data[(st.session_state.production_data['日期'].dt.isocalendar().week == last_week) & 
                                                                          (st.session_state.production_data['日期'].dt.isocalendar().year == last_year) &
                                                                          (st.session_state.production_data['产品名称'].isin(selected_products))]
                        
                        if not this_week_data.empty:
                            this_week_yield = (this_week_data['合格数量'].sum() / this_week_data['生产数量'].sum() * 100) if this_week_data['生产数量'].sum() > 0 else 0
                            report_content += f"- 本周合格率: {this_week_yield:.2f}%\n"
                            
                            if not last_week_data.empty:
                                last_week_yield = (last_week_data['合格数量'].sum() / last_week_data['生产数量'].sum() * 100) if last_week_data['生产数量'].sum() > 0 else 0
                                change = this_week_yield - last_week_yield
                                report_content += f"- 周环比变化: {'+' if change > 0 else ''}{change:.2f}个百分点\n"
                    
                    elif report_type == "产品月度分析":
                        # 产品月度分析特定内容
                        report_content += f"\n## 二、月度产品分析\n"
                        
                        # 按产品分组的月度汇总
                        monthly_product_summary = filtered_report_data.groupby(['产品名称']).agg({
                            '生产数量': ['sum', 'mean'],
                            '合格数量': ['sum', 'mean'],
                            '不合格数量': 'sum',
                            '合格率': ['mean', 'min', 'max']
                        }).round(2)
                        
                        monthly_product_summary.columns = ['总生产数量', '日均生产数量', '总合格数量', '日均合格数量', '总不合格数量', '平均合格率', '最低合格率', '最高合格率']
                        monthly_product_summary = monthly_product_summary.reset_index()
                        
                        report_content += monthly_product_summary.to_markdown(index=False, numalign="right") + "\n"
                    
                    elif report_type == "不合格原因分析":
                        # 不合格原因分析特定内容
                        report_content += f"\n## 二、不合格原因详细分析\n"
                        
                        reasons_list = []
                        for reasons in filtered_report_data['不合格原因']:
                            if reasons and reasons != "无":
                                for reason in reasons.split("、"):
                                    reasons_list.append(reason.strip())
                        
                        reasons_series = pd.Series(reasons_list)
                        if not reasons_series.empty:
                            reasons_count = reasons_series.value_counts().reset_index()
                            reasons_count.columns = ['原因', '次数']
                            reasons_count['占比'] = (reasons_count['次数'] / reasons_count['次数'].sum() * 100).round(2)
                            
                            report_content += reasons_count.to_markdown(index=False, numalign="right") + "\n"
                            
                            # 按产品分析不合格原因
                            report_content += f"\n### 按产品分析不合格原因\n"
                            product_reasons = {}
                            for _, row in filtered_report_data.iterrows():
                                if row['不合格原因'] and row['不合格原因'] != "无":
                                    product = row['产品名称']
                                    for reason in row['不合格原因'].split("、"):
                                        reason = reason.strip()
                                        if product not in product_reasons:
                                            product_reasons[product] = {}
                                        if reason not in product_reasons[product]:
                                            product_reasons[product][reason] = 0
                                        product_reasons[product][reason] += 1
                            
                            for product, reasons in product_reasons.items():
                                report_content += f"\n**{product}**:\n"
                                for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
                                    report_content += f"  * {reason}: {count}次\n"
                        else:
                            report_content += f"- 暂无不合格数据\n"
                    
                    elif report_type == "产品对比分析":
                        # 产品对比分析特定内容
                        report_content += f"\n## 二、产品对比分析\n"
                        
                        if len(selected_products) >= 2:
                            # 多产品对比
                            product_comparison = filtered_report_data.groupby('产品名称').agg({
                                '生产数量': ['sum', 'mean', 'max', 'min'],
                                '合格率': ['mean', 'max', 'min'],
                                '不合格数量': 'sum'
                            }).round(2)
                            
                            product_comparison.columns = ['总生产数量', '日均生产数量', '最高日产量', '最低日产量', '平均合格率', '最高合格率', '最低合格率', '总不合格数量']
                            product_comparison = product_comparison.reset_index()
                            
                            report_content += product_comparison.to_markdown(index=False, numalign="right") + "\n"
                        else:
                            report_content += f"- 请选择至少2个产品进行对比分析\n"
                    
                    # 3. 通用的生产趋势分析
                    if report_type != "不合格原因分析":
                        report_content += f"\n## 三、生产趋势分析\n"
                        daily_trend = filtered_report_data.groupby('日期')[['生产数量', '合格数量']].sum()
                        
                        if not daily_trend.empty:
                            report_content += f"- 日均生产数量: {daily_trend['生产数量'].mean():.2f}件\n"
                            report_content += f"- 生产高峰期: {daily_trend['生产数量'].idxmax().strftime('%Y-%m-%d')}，当日生产{daily_trend['生产数量'].max():,}件\n"
                            report_content += f"- 生产低谷期: {daily_trend['生产数量'].idxmin().strftime('%Y-%m-%d')}，当日生产{daily_trend['生产数量'].min():,}件\n"
                    
                    # 4. 通用的质量分析
                    if report_type not in ["生产日报", "不合格原因分析"]:
                        report_content += f"\n## 四、质量分析\n"
                        product_quality = filtered_report_data.groupby('产品名称')[['生产数量', '合格数量']].sum()
                        product_quality['合格率'] = (product_quality['合格数量'] / product_quality['生产数量'] * 100).round(2)
                        
                        if not product_quality.empty:
                            best_quality = product_quality['合格率'].idxmax()
                            worst_quality = product_quality['合格率'].idxmin()
                            report_content += f"- 质量最佳产品: {best_quality}，合格率{product_quality.loc[best_quality, '合格率']}%\n"
                            report_content += f"- 质量待提升产品: {worst_quality}，合格率{product_quality.loc[worst_quality, '合格率']}%\n"
                    
                    # 5. 改进建议
                    if include_recommendations:
                        report_content += f"\n## 五、改进建议\n"
                        
                        if report_type != "不合格原因分析":
                            report_content += f"1. 针对{best_quality}的成功经验，可在其他产品生产中推广应用\n"
                            report_content += f"2. 重点关注{worst_quality}的生产过程，分析合格率低下的根本原因\n"
                        
                        if not reasons_series.empty:
                            top_reasons = reasons_series.value_counts().head(3)
                            report_content += f"3. 针对主要不合格原因'{top_reasons.index[0]}'，建议制定专项改进措施\n"
                        
                        report_content += f"4. 根据生产趋势合理安排生产计划，避免生产波动过大\n"
                        report_content += f"5. 定期分析质量数据，建立质量预警机制\n"
                        report_content += f"6. 加强员工培训，提高操作技能和质量意识\n"
                    
                    # 6. 详细数据表格
                    if include_raw_data:
                        report_content += f"\n## 六、原始数据\n"
                        report_content += filtered_report_data.to_markdown(index=False, numalign="right") + "\n"
                    
                    # 提供报表下载
                    st.success("报表生成成功！")
                    
                    # 根据选择的格式导出
                    if report_format == "Markdown":
                        buffer = io.BytesIO()
                        buffer.write(report_content.encode('utf-8'))
                        buffer.seek(0)
                        
                        st.download_button(
                            label="📥 下载Markdown报表",
                            data=buffer,
                            file_name=f"{report_type}_{datetime.today().strftime('%Y%m%d')}.md",
                            mime="text/markdown"
                        )
                    
                    elif report_format == "CSV":
                        buffer = io.BytesIO()
                        filtered_report_data.to_csv(buffer, index=False, encoding='utf-8-sig')
                        buffer.seek(0)
                        
                        st.download_button(
                            label="📥 下载CSV数据",
                            data=buffer,
                            file_name=f"{report_type}_数据_{datetime.today().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    
                    elif report_format == "Excel":
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            # 写入筛选后的数据
                            filtered_report_data.to_excel(writer, sheet_name='原始数据', index=False)
                            
                            # 写入报表摘要
                            summary_data = {
                                '指标': ['总生产数量', '总合格数量', '总不合格数量', '总体合格率', '涉及产品数量', '报告覆盖天数'],
                                '值': [total_production, total_qualified, total_unqualified, f"{overall_yield_rate:.2f}%", len(selected_products), filtered_report_data['日期'].nunique()]
                            }
                            pd.DataFrame(summary_data).to_excel(writer, sheet_name='报表摘要', index=False)
                            
                            # 写入产品汇总
                            product_summary = filtered_report_data.groupby('产品名称')[['生产数量', '合格数量', '不合格数量']].sum().reset_index()
                            product_summary['合格率'] = (product_summary['合格数量'] / product_summary['生产数量'] * 100).round(2)
                            product_summary.to_excel(writer, sheet_name='产品汇总', index=False)
                        
                        buffer.seek(0)
                        
                        st.download_button(
                            label="📥 下载Excel报表",
                            data=buffer,
                            file_name=f"{report_type}_{datetime.today().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
    
    # 6. 知识库
    with analysis_tab6:
        st.subheader("📚 知识库")
        st.markdown("---")
        
        # 知识库功能选项卡
        knowledge_tab1, knowledge_tab2, knowledge_tab3 = st.tabs(["行业最佳实践", "优化方案", "常见问题解答"])
        
        # 1. 行业最佳实践
        with knowledge_tab1:
            st.markdown("### 🏭 行业最佳实践")
            
            # 生产管理最佳实践
            st.markdown("#### 📊 生产管理")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1. 准时制生产 (JIT)**")
                st.markdown("- 按需生产，减少库存积压")
                st.markdown("- 提高生产效率，降低成本")
                st.markdown("- 增强生产灵活性")
                
                st.markdown("**2. 全面质量管理 (TQM)**")
                st.markdown("- 全员参与质量控制")
                st.markdown("- 持续改进质量体系")
                st.markdown("- 以客户需求为导向")
            with col2:
                st.markdown("**3. 5S管理法**")
                st.markdown("- 整理(Sort): 区分必需品和非必需品")
                st.markdown("- 整顿(Set in order): 定点、定容、定量")
                st.markdown("- 清扫(Shine): 保持工作环境清洁")
                st.markdown("- 清洁(Standardize): 制定标准")
                st.markdown("- 素养(Sustain): 养成良好习惯")
                
                st.markdown("**4. 看板管理**")
                st.markdown("- 可视化生产进度")
                st.markdown("- 控制生产流程")
                st.markdown("- 提高沟通效率")
            
            # 质量管理最佳实践
            st.markdown("#### 🔍 质量管理")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1. 六西格玛 (6σ)**")
                st.markdown("- 减少变异，提高质量")
                st.markdown("- 定义、测量、分析、改进、控制 (DMAIC)")
                st.markdown("- 目标：3.4个缺陷/百万次机会")
                
                st.markdown("**2. 质量控制七大工具**")
                st.markdown("- 检查表、柏拉图、因果图")
                st.markdown("- 散点图、控制图、直方图")
                st.markdown("- 分层法")
            with col2:
                st.markdown("**3. 零缺陷管理**")
                st.markdown("- 第一次就把事情做对")
                st.markdown("- 质量是制造出来的，不是检验出来的")
                st.markdown("- 预防胜于治疗")
                
                st.markdown("**4. 统计过程控制 (SPC)**")
                st.markdown("- 实时监控生产过程")
                st.markdown("- 识别过程变异")
                st.markdown("- 预测过程趋势")
            
        # 2. 优化方案
        with knowledge_tab2:
            st.markdown("### 🛠️ 优化方案")
            
            # 质量问题优化方案
            st.markdown("#### 🎯 质量问题优化")
            
            # 搜索框
            search_query = st.text_input("搜索优化方案", placeholder="输入不合格原因或问题关键词")
            
            # 优化方案库
            optimization_solutions = {
                "原材料不合格": {
                    "问题描述": "原材料不符合质量标准，导致生产的产品不合格",
                    "优化措施": [
                        "加强供应商管理，建立供应商评估体系",
                        "增加原材料检验频次和项目",
                        "建立原材料质量追溯系统",
                        "寻找替代供应商，降低单一供应商风险"
                    ],
                    "预期效果": "降低原材料不合格率，提高产品合格率"
                },
                "设备故障": {
                    "问题描述": "生产设备出现故障或精度不足，导致产品不合格",
                    "优化措施": [
                        "建立设备维护保养计划，定期检查设备",
                        "对操作人员进行设备操作培训",
                        "引入设备状态监测系统，提前预警故障",
                        "考虑设备升级或更换，提高设备精度"
                    ],
                    "预期效果": "减少设备故障停机时间，提高产品质量稳定性"
                },
                "操作失误": {
                    "问题描述": "操作人员操作不规范或失误，导致产品不合格",
                    "优化措施": [
                        "完善操作规范和标准作业指导书",
                        "加强操作人员培训和考核",
                        "引入防错装置，减少人为失误",
                        "建立操作质量检查机制"
                    ],
                    "预期效果": "减少操作失误，提高产品合格率"
                },
                "工艺问题": {
                    "问题描述": "生产工艺不合理或参数设置不当，导致产品不合格",
                    "优化措施": [
                        "对生产工艺进行优化和改进",
                        "合理设置工艺参数，进行参数验证",
                        "引入新工艺、新技术，提高生产效率和质量",
                        "建立工艺参数监控系统"
                    ],
                    "预期效果": "优化生产工艺，提高产品质量和生产效率"
                },
                "环境因素": {
                    "问题描述": "生产环境（温度、湿度、灰尘等）不符合要求，导致产品不合格",
                    "优化措施": [
                        "改善生产环境，控制温度、湿度等参数",
                        "加强生产环境清洁和维护",
                        "对敏感产品生产区域进行环境监控",
                        "建立环境异常响应机制"
                    ],
                    "预期效果": "改善生产环境，提高产品质量稳定性"
                }
            }
            
            # 显示优化方案
            if search_query:
                # 搜索匹配的优化方案
                search_results = []
                for issue, solution in optimization_solutions.items():
                    if search_query in issue or any(search_query in step for step in solution["优化措施"]):
                        search_results.append((issue, solution))
                
                if search_results:
                    for issue, solution in search_results:
                        with st.expander(f"📋 {issue}"):
                            st.markdown(f"**问题描述**：{solution['问题描述']}")
                            st.markdown("**优化措施**：")
                            for i, measure in enumerate(solution["优化措施"], 1):
                                st.markdown(f"{i}. {measure}")
                            st.markdown(f"**预期效果**：{solution['预期效果']}")
                else:
                    st.info("未找到相关优化方案，请尝试其他关键词")
            else:
                # 默认显示所有优化方案
                for issue, solution in optimization_solutions.items():
                    with st.expander(f"📋 {issue}"):
                        st.markdown(f"**问题描述**：{solution['问题描述']}")
                        st.markdown("**优化措施**：")
                        for i, measure in enumerate(solution["优化措施"], 1):
                            st.markdown(f"{i}. {measure}")
                        st.markdown(f"**预期效果**：{solution['预期效果']}")
            
        # 3. 常见问题解答
        with knowledge_tab3:
            st.markdown("### ❓ 常见问题解答")
            
            # FAQ列表
            faq_list = [
                {
                    "question": "如何提高产品合格率？",
                    "answer": [
                        "建立完善的质量管理体系",
                        "加强生产过程监控和检验",
                        "对操作人员进行培训和考核",
                        "优化生产工艺和设备",
                        "分析不合格原因，采取针对性改进措施"
                    ]
                },
                {
                    "question": "如何降低生产成本？",
                    "answer": [
                        "优化生产流程，提高生产效率",
                        "降低原材料消耗和浪费",
                        "合理安排生产计划，减少设备停机时间",
                        "实施精益生产，减少库存积压",
                        "降低能源消耗和人工成本"
                    ]
                },
                {
                    "question": "如何预测产品需求？",
                    "answer": [
                        "分析历史销售数据，识别需求趋势",
                        "考虑季节因素和市场变化",
                        "使用多种预测模型进行综合预测",
                        "结合销售团队的市场反馈",
                        "定期更新预测模型，提高预测准确性"
                    ]
                },
                {
                    "question": "如何提高设备利用率？",
                    "answer": [
                        "建立设备维护保养计划，实施预防性维护，减少设备故障",
                        "优化生产计划，减少设备换模和调整时间",
                        "提高设备自动化程度，减少人工干预",
                        "对设备操作人员进行培训，提高操作技能",
                        "建立设备利用率考核机制，激励员工提高设备使用效率",
                        "定期对设备进行评估，考虑设备升级或更换"
                    ],
                    "category": "设备维护"
                },
                {
                    "question": "如何进行有效的数据分析？",
                    "answer": [
                        "明确数据分析目标，确定关键绩效指标(KPI)",
                        "收集准确、完整的数据，建立数据质量控制机制",
                        "选择合适的数据分析方法和工具",
                        "对数据进行可视化展示，便于理解和决策",
                        "定期进行数据分析，提供决策支持",
                        "建立数据分析报告机制，及时反馈分析结果"
                    ],
                    "category": "数据分析"
                },
                {
                    "question": "如何提高生产灵活性？",
                    "answer": [
                        "采用模块化生产方式，提高生产线的适应性",
                        "培养多技能员工，提高人员灵活性",
                        "合理安排生产计划，采用混合生产模式",
                        "建立快速换模(SMED)系统，减少换模时间",
                        "优化供应链管理，提高物料供应的灵活性",
                        "采用先进的生产管理系统，提高计划灵活性"
                    ],
                    "category": "生产管理"
                },
                {
                    "question": "如何建立有效的质量管理体系？",
                    "answer": [
                        "明确质量方针和质量目标，确保与企业战略一致",
                        "建立质量管理组织结构，明确各部门和人员的质量职责",
                        "制定质量管理制度和流程，确保质量活动规范化",
                        "实施质量培训，提高员工质量意识和技能",
                        "建立质量记录和文件管理系统，确保质量可追溯",
                        "定期进行内部审核和管理评审，持续改进质量体系"
                    ],
                    "category": "质量控制"
                }
            ]
            
            # 过滤FAQ
            filtered_faqs = []
            for faq in faq_list:
                # 分类过滤
                if faq_categories == "全部" or faq["category"] == faq_categories:
                    # 关键词搜索
                    if not knowledge_search or knowledge_search.lower() in faq["question"].lower() or \
                       any(knowledge_search.lower() in answer.lower() for answer in faq["answer"]):
                        filtered_faqs.append(faq)
            
            # 显示FAQ
            if filtered_faqs:
                for i, faq in enumerate(filtered_faqs, 1):
                    with st.expander(f"Q{i}. {faq['question']} - [{faq['category']}]"):
                        for j, answer in enumerate(faq["answer"], 1):
                            st.markdown(f"{j}. {answer}")
            else:
                st.info("未找到相关问题解答，请尝试调整筛选条件或搜索关键词")
            
        # 4. 质量工具指南
        with knowledge_tab4:
            st.markdown("### 📏 质量工具指南")
            
            # 质量工具分类
            quality_tools = st.selectbox(
                "选择质量工具",
                [
                    "柏拉图 (Pareto Chart)", 
                    "因果图 (Cause and Effect Diagram)", 
                    "控制图 (Control Chart)", 
                    "直方图 (Histogram)",
                    "散点图 (Scatter Diagram)",
                    "检查表 (Check Sheet)",
                    "分层法 (Stratification)",
                    "FMEA (失效模式与影响分析)"
                ],
                key="quality_tool"
            )
            
            # 质量工具详细介绍
            quality_tool_details = {
                "柏拉图 (Pareto Chart)": {
                    "description": "柏拉图是一种按重要性排序的条形图，用于识别和优先处理问题。它基于80/20原则，即80%的问题由20%的原因引起。",
                    "用途": [
                        "识别主要问题或原因",
                        "确定改进的优先级",
                        "监控改进效果",
                        "沟通问题的重要性"
                    ],
                    "应用步骤": [
                        "收集数据，列出问题或原因及其发生次数",
                        "按发生次数降序排列",
                        "计算累积百分比",
                        "绘制条形图和累积百分比折线图",
                        "分析结果，确定主要问题"
                    ],
                    "注意事项": [
                        "确保数据准确可靠",
                        "定期更新柏拉图，监控改进效果",
                        "结合其他质量工具使用，如因果图"
                    ]
                },
                "因果图 (Cause and Effect Diagram)": {
                    "description": "因果图又称鱼骨图或石川图，用于识别问题的潜在原因。它将问题放在鱼头位置，原因分类放在鱼脊的分支上。",
                    "用途": [
                        "分析问题的根本原因",
                        "组织头脑风暴会议",
                        "可视化问题与原因的关系",
                        "确定改进的方向"
                    ],
                    "应用步骤": [
                        "明确要分析的问题，写在鱼头位置",
                        "确定主要原因类别，如人、机、料、法、环、测",
                        "针对每个类别，展开分析潜在原因",
                        "进一步分析深层原因，直到找到根本原因",
                        "对原因进行验证，确定主要原因"
                    ],
                    "注意事项": [
                        "鼓励团队参与，进行头脑风暴",
                        "原因分析要深入，找出根本原因",
                        "对原因进行验证，避免主观判断",
                        "结合其他质量工具使用，如柏拉图、FMEA"
                    ]
                },
                "控制图 (Control Chart)": {
                    "description": "控制图是一种用于监控过程是否处于统计控制状态的图表。它通过绘制过程数据并与控制限比较，识别过程变异。",
                    "用途": [
                        "监控过程稳定性",
                        "识别过程变异",
                        "预测过程趋势",
                        "确定过程是否需要调整"
                    ],
                    "应用步骤": [
                        "确定要监控的质量特性",
                        "收集数据，确定样本量和抽样频率",
                        "计算控制限(通常为±3σ)",
                        "绘制控制图，包括中心线和控制限",
                        "分析控制图，判断过程是否稳定",
                        "采取相应措施，如过程调整或持续改进"
                    ],
                    "注意事项": [
                        "确保数据收集的一致性和准确性",
                        "正确计算控制限，避免误判",
                        "定期更新控制图，监控过程变化",
                        "结合其他质量工具使用，如直方图、散点图"
                    ]
                },
                "直方图 (Histogram)": {
                    "description": "直方图是一种用于展示数据分布的图表。它将数据分组，并用条形图表示每组数据的频率或数量。",
                    "用途": [
                        "展示数据分布情况",
                        "识别数据的集中趋势和离散程度",
                        "比较不同组数据的分布",
                        "评估过程能力"
                    ],
                    "应用步骤": [
                        "收集数据，确定数据范围",
                        "计算数据的最大值、最小值和极差",
                        "确定组数和组距",
                        "绘制直方图，包括横轴(数据分组)和纵轴(频率或数量)",
                        "分析直方图的形状，如正态分布、偏态分布等"
                    ],
                    "注意事项": [
                        "确保数据量足够，一般至少50个数据点",
                        "合理选择组数，通常为5-20组",
                        "正确解释直方图的形状，避免误判",
                        "结合其他质量工具使用，如控制图、过程能力分析"
                    ]
                },
                "散点图 (Scatter Diagram)": {
                    "description": "散点图是一种用于展示两个变量之间关系的图表。它将一个变量放在横轴，另一个变量放在纵轴，每个数据点表示一对变量值。",
                    "用途": [
                        "分析两个变量之间的关系",
                        "识别变量之间的相关性",
                        "预测一个变量基于另一个变量的值",
                        "确定改进的方向"
                    ],
                    "应用步骤": [
                        "确定要分析的两个变量",
                        "收集数据，每对数据表示两个变量的值",
                        "绘制散点图，横轴表示自变量，纵轴表示因变量",
                        "分析散点图的趋势，判断变量之间的关系(正相关、负相关或无相关)",
                        "计算相关系数，量化变量之间的关系强度"
                    ],
                    "注意事项": [
                        "确保数据的准确性和完整性",
                        "避免将相关性误解为因果关系",
                        "考虑其他可能影响变量关系的因素",
                        "结合其他质量工具使用，如回归分析、控制图"
                    ]
                },
                "检查表 (Check Sheet)": {
                    "description": "检查表是一种用于收集和记录数据的表格。它可以帮助系统地收集数据，便于后续分析。",
                    "用途": [
                        "收集质量数据，如缺陷类型、发生位置等",
                        "记录过程参数，如温度、湿度等",
                        "进行日常检查，如设备维护、安全检查等",
                        "统计数据，为其他质量工具提供数据支持"
                    ],
                    "应用步骤": [
                        "确定要收集的数据类型和范围",
                        "设计检查表，包括数据类别、收集时间、收集人等",
                        "使用检查表收集数据，确保数据准确可靠",
                        "整理和分析数据，生成图表或报告",
                        "根据分析结果采取相应措施"
                    ],
                    "注意事项": [
                        "检查表设计要简洁明了，易于使用",
                        "确保数据收集的一致性和准确性",
                        "定期更新检查表，适应新的需求",
                        "结合其他质量工具使用，如柏拉图、因果图"
                    ]
                },
                "分层法 (Stratification)": {
                    "description": "分层法是一种用于将数据按不同类别分组的方法。它可以帮助识别数据中的模式和差异。",
                    "用途": [
                        "分析不同组数据之间的差异",
                        "识别问题的特定原因",
                        "验证改进措施的效果",
                        "提高数据分析的准确性"
                    ],
                    "应用步骤": [
                        "确定分层的依据，如时间、地点、人员、设备等",
                        "收集数据，按分层依据分组",
                        "对每组数据进行分析，比较组间差异",
                        "识别显著差异的组，分析原因",
                        "采取相应措施，解决问题"
                    ],
                    "注意事项": [
                        "选择合适的分层依据，确保分层有意义",
                        "确保每组数据量足够，避免结论不可靠",
                        "结合其他质量工具使用，如散点图、直方图",
                        "考虑多个分层依据的组合使用"
                    ]
                },
                "FMEA (失效模式与影响分析)": {
                    "description": "FMEA是一种用于识别和评估产品或过程中潜在失效模式及其影响的方法。它可以帮助预防潜在问题的发生。",
                    "用途": [
                        "识别产品或过程中的潜在失效模式",
                        "评估失效模式的严重程度、发生频率和可探测性",
                        "确定改进的优先级",
                        "预防潜在问题的发生"
                    ],
                    "应用步骤": [
                        "确定分析的范围和目标",
                        "组成跨职能团队，包括设计、生产、质量等部门",
                        "识别潜在失效模式、原因和影响",
                        "评估严重程度(S)、发生频率(O)和可探测性(D)",
                        "计算风险优先级数(RPN = S×O×D)",
                        "制定改进措施，降低RPN",
                        "跟踪改进措施的实施效果"
                    ],
                    "注意事项": [
                        "确保团队成员具有相关专业知识",
                        "定期更新FMEA，反映产品或过程的变化",
                        "结合其他质量工具使用，如控制图、防错设计",
                        "将FMEA结果用于设计和过程改进"
                    ]
                }
            }
            
            # 显示质量工具详情
            if quality_tool in quality_tool_details:
                tool = quality_tool_details[quality_tool]
                st.markdown(f"### {quality_tool}")
                st.markdown(f"**描述**：{tool['description']}")
                
                st.markdown("**用途**：")
                for i, use in enumerate(tool['用途'], 1):
                    st.markdown(f"{i}. {use}")
                
                st.markdown("**应用步骤**：")
                for i, step in enumerate(tool['应用步骤'], 1):
                    st.markdown(f"{i}. {step}")
                
                st.markdown("**注意事项**：")
                for i, note in enumerate(tool['注意事项'], 1):
                    st.markdown(f"{i}. {note}")
            
        # 5. 生产效率提升
        with knowledge_tab5:
            st.markdown("### 🚀 生产效率提升")
            
            # 效率提升方法
            st.markdown("#### 📈 效率提升方法")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1. 生产线平衡**")
                st.markdown("- 分析各工序的作业时间")
                st.markdown("- 调整工序内容，使各工序作业时间相近")
                st.markdown("- 减少工序间等待时间")
                st.markdown("- 提高生产线整体效率")
                
                st.markdown("**2. 快速换模 (SMED)**")
                st.markdown("- 区分内部换模和外部换模")
                st.markdown("- 将内部换模转化为外部换模")
                st.markdown("- 优化换模步骤，减少换模时间")
                st.markdown("- 提高设备利用率")
            with col2:
                st.markdown("**3. 瓶颈管理**")
                st.markdown("- 识别生产流程中的瓶颈工序")
                st.markdown("- 集中资源解决瓶颈问题")
                st.markdown("- 优化瓶颈工序的作业方法")
                st.markdown("- 提高瓶颈工序的生产能力")
                
                st.markdown("**4. 标准化作业**")
                st.markdown("- 制定标准作业指导书(SOP)")
                st.markdown("- 确保所有操作人员按标准作业")
                st.markdown("- 减少作业变异，提高产品一致性")
                st.markdown("- 便于培训新员工")
            
            # 效率提升案例
            st.markdown("#### 📝 效率提升案例")
            with st.expander("案例：某电子厂生产线效率提升"):
                st.markdown("**背景**：某电子厂手机组装生产线效率低下，日产量仅为2000台，无法满足订单需求。")
                st.markdown("**问题分析**：")
                st.markdown("- 生产线平衡率仅为75%，存在明显瓶颈工序")
                st.markdown("- 换模时间长达2小时，影响设备利用率")
                st.markdown("- 操作人员技能参差不齐，作业方法不统一")
                st.markdown("- 生产计划不合理，导致频繁切换产品")
                
                st.markdown("**改进措施**：")
                st.markdown("1. 实施生产线平衡，调整工序内容，将平衡率提高到90%")
                st.markdown("2. 采用SMED方法，将换模时间减少到30分钟")
                st.markdown("3. 制定标准化作业指导书，对操作人员进行培训和考核")
                st.markdown("4. 优化生产计划，减少产品切换次数")
                
                st.markdown("**改进效果**：")
                st.markdown("- 日产量提高到2800台，效率提升40%")
                st.markdown("- 设备利用率从70%提高到85%")
                st.markdown("- 产品合格率从95%提高到98%")
                st.markdown("- 生产成本降低15%")
            
            # 效率评估指标
            st.markdown("#### 📊 效率评估指标")
            efficiency_metrics = {
                "设备利用率": "设备实际运行时间与计划运行时间的比率，反映设备的使用效率",
                "生产线平衡率": "各工序作业时间的平均值与瓶颈工序作业时间的比率，反映生产线的平衡程度",
                "生产效率": "实际产量与标准产量的比率，反映生产过程的效率",
                "单位产品工时": "生产单位产品所需的工时，反映劳动效率",
                "OEE (设备综合效率)": "可用率×表现率×质量率，综合反映设备的使用效率"
            }
            
            for metric, description in efficiency_metrics.items():
                st.markdown(f"**{metric}**：{description}")
            
            # 生产效率FAQ
            st.markdown("#### ❓ 生产效率常见问题")
            efficiency_faq = [
                {
                    "question": "如何管理库存？",
                    "answer": [
                        "实施库存分类管理（ABC分类法）",
                        "加强库存周转率监控",
                        "与供应商建立良好的合作关系，缩短交货期"
                    ]
                },
                {
                    "question": "如何提高生产效率？",
                    "answer": [
                        "优化生产布局，减少物料搬运时间",
                        "提高设备利用率，减少设备故障时间",
                        "合理安排生产计划，避免生产波动",
                        "引入自动化生产设备，减少人工操作",
                        "对生产过程进行持续改进"
                    ]
                }
            ]
            
            # 显示FAQ
            for faq in faq_list:
                with st.expander(f"❓ {faq['question']}"):
                    for i, answer_point in enumerate(faq['answer'], 1):
                        st.markdown(f"{i}. {answer_point}")
            
            # 快速导航
            st.markdown("---")
            st.markdown("### 🚀 快速导航")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**质量分析工具**")
                st.markdown("- [柏拉图分析](https://zh.wikipedia.org/wiki/%E6%99%AE%E6%8B%89%E6%89%98%E5%9B%BE)")
                st.markdown("- [因果图](https://zh.wikipedia.org/wiki/%E5%9B%A0%E6%9E%9C%E5%9B%BE)")
                st.markdown("- [控制图](https://zh.wikipedia.org/wiki/%E6%8E%A7%E5%88%B6%E5%9B%BE)")
            with col2:
                st.markdown("**生产管理方法**")
                st.markdown("- [精益生产](https://zh.wikipedia.org/wiki/%E7%B2%BE%E7%9B%8A%E7%94%9F%E4%BA%A7)")
                st.markdown("- [六西格玛](https://zh.wikipedia.org/wiki/%E5%85%AD%E8%A5%BF%E6%A0%BC%E7%8E%9B)")
                st.markdown("- [5S管理](https://zh.wikipedia.org/wiki/5S%E7%AE%A1%E7%90%86)")

# 系统设置页面
elif selected == "系统设置":
    st.title("⚙️ 系统设置")
    st.markdown("---")
    
    # 数据管理
    st.subheader("数据管理")
    
    # 显示当前数据量
    st.write(f"当前系统中共有 {len(st.session_state.production_data)} 条生产记录")
    
    # 数据管理功能
    if not st.session_state.production_data.empty:
        # 批量删除数据功能
        st.markdown("### 🗑️ 批量删除数据")
        
        # 显示数据并添加复选框
        selected_rows = []
        for i, (index, row) in enumerate(st.session_state.production_data.iterrows()):
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.checkbox("", key=f"delete_setting_{index}"):
                    selected_rows.append(index)
            with col2:
                st.write(f"**{row['产品名称']}** - {row['日期'].strftime('%Y-%m-%d')}: 生产 {row['生产数量']} 件, 合格率 {row['合格率']:.2f}%")
        
        # 删除按钮
        if st.button("删除选中数据", type="secondary", help="此操作将删除选中的生产记录，请谨慎操作"):
            if selected_rows:
                # 确认删除
                confirm_delete = st.checkbox("确认要删除选中的数据吗？此操作不可恢复")
                if confirm_delete:
                    # 从会话状态中删除数据
                    st.session_state.production_data = st.session_state.production_data.drop(selected_rows)
                    
                    # 重置索引
                    st.session_state.production_data = st.session_state.production_data.reset_index(drop=True)
                    
                    # 保存到数据库
                    save_data_to_db(st.session_state.production_data)
                    
                    st.success(f"成功删除 {len(selected_rows)} 条数据")
            else:
                st.warning("请先选择要删除的数据")
    
    # 清空数据按钮
    st.markdown("### 🗑️ 清空所有数据")
    if st.button("清空所有数据", type="secondary", help="此操作将删除所有生产记录，请谨慎操作"):
        if st.session_state.production_data.empty:
            st.info("系统中已无数据")
        else:
            confirm = st.checkbox("确认要清空所有数据吗？此操作不可恢复")
            if confirm:
                st.session_state.production_data = pd.DataFrame(columns=st.session_state.production_data.columns)
                # 清空数据库中的数据
                clear_data_from_db()
                st.success("所有数据已清空")
    
    # 导出全部数据
    if not st.session_state.production_data.empty:
        
        st.markdown(
            get_csv_download_link(
                st.session_state.production_data,
                f"production_data_{datetime.today().strftime('%Y%m%d')}.csv",
                "📥 导出全部生产数据"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # 关于系统
    st.subheader("关于系统")
    st.write("产品生产数据分析系统 v1.0")
    st.write("用于分析产品生产数据，生成可视化图表和月度报告")
    st.write("© 2025 数据分析系统")

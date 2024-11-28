import json
import os
import re
from datetime import datetime

import streamlit as st

# ============================
# 你负责的文件是：
your_splited_filename = "0-2000.json"
# ============================
raw_data_dir = os.path.join(os.path.dirname(__file__), "raw", "test1")
image_dir = os.path.join(raw_data_dir, "images")
splited_dir = os.path.join(os.path.dirname(__file__), "splited")
output_dir = os.path.join(os.path.dirname(__file__), "output")
# ============================


# 加载 JSON 数据
def load_data(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return []


def get_task_name(item):
    if "-" in item["id"]:
        return "picture"
    else:
        return "dialog"


# 加载结果文件数据
def load_results(results_file_path):
    if os.path.exists(results_file_path):
        try:
            with open(results_file_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"加载结果文件失败: {e}")
    return []


# 保存标注结果到文件
def save_results(data, results_file_path):
    try:
        with open(results_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"保存标注结果失败: {e}")


# 恢复进度
def get_starting_index(data, results):
    return len(results)


# 主程序
def main():
    st.set_page_config(page_title="图片数据标注工具", layout="wide")

    # 配置文件路径
    json_file_path = os.path.join(splited_dir, your_splited_filename)  # 原始数据文件路径
    results_file_path = os.path.join(output_dir, "marked_" + your_splited_filename)  # 结果文件路径

    # 加载原始数据
    data = load_data(json_file_path)
    if not data:
        st.warning("没有有效数据！")
        return

    # 加载结果文件
    results = load_results(results_file_path)

    # 恢复进度
    starting_index = get_starting_index(data, results)
    if "current_index" not in st.session_state:
        st.session_state.current_index = starting_index

    # 当前数据索引
    current_index = st.session_state.current_index
    total_count = len(data)  # 数据总条数

    # 显示进度信息
    st.markdown(f"### 共 {total_count} 条，现第 {current_index + 1} 条")
    if current_index >= total_count:
        st.success("标注任务完成！所有数据已保存。")
        return

    # 当前数据项
    item = data[current_index]
    item_id = item.get("id", "未知ID")
    images = item.get("image", [])
    instruction = item.get("instruction", "无说明")
    task_name = get_task_name(item)

    # 布局：图片和选项左右排列，图片下方显示 instruction
    cols = st.columns([1, 1, 1])  # 三列布局

    with cols[0]:  # 左侧显示图片和 instruction
        if images:
            for image in images:
                with open(os.path.join(image_dir, image), "rb") as img_file:
                    st.image(img_file.read(), caption=f"数据 ID: {item_id}", width=300)
        else:
            st.error(f"数据 ID {item_id} 缺少图片！")
            st.session_state.current_index += 1
            st.rerun()

    with cols[1]:  # 中间显示 instruction
        st.markdown("### 说明")
        if task_name == "dialog":
            # 正则提取 <用户与客服的对话 START> 和 <用户与客服的对话 END> 之间的内容
            match = re.search(r"<用户与客服的对话 START>(.*?)<用户与客服的对话 END>", instruction, re.S)

            # 如果匹配到内容，提取用户与客服对话
            if match:
                conversation = match.group(1).strip()
                # conversation = conversation.replace("\n", "\n\n")
                conversation_lines = conversation.split("\n")
                # 隔行显示不同颜色对话内容
                for line in conversation_lines:
                    if line.startswith("用户"):
                        st.markdown(f"**{line}**", unsafe_allow_html=True)
                    elif line.startswith("客服"):
                        st.markdown(f"*{line}*", unsafe_allow_html=True)
                    else:
                        st.text(line)
            else:
                conversation = "未找到对话内容"
            st.text(conversation)
        elif task_name == "picture":
            st.text(instruction)
        else:
            st.error(f"未知任务名称: {task_name}")
            return

    with cols[2]:  # 右侧显示选项
        st.markdown("### 请选择标注：")
        intend_choices = [
            "反馈密封性不好",
            "是否好用",
            "是否会生锈",
            "排水方式",
            "包装区别",
            "发货数量",
            "反馈用后症状",
            "商品材质",
            "功效功能",
            "是否易褪色",
            "适用季节",
            "能否调光",
            "版本款型区别",
            "单品推荐",
            "用法用量",
            "控制方式",
            "上市时间",
            "商品规格",
            "信号情况",
            "养护方法",
            "套装推荐",
            "何时上货",
            "气泡",
        ]
        intend_choices.append("跳过")
        pic_choices = [
            "实物拍摄(含售后)",
            "商品分类选项",
            "商品头图",
            "商品详情页截图",
            "下单过程中出现异常（显示购买失败浮窗）",
            "订单详情页面",
            "支付页面",
            "消费者与客服聊天页面",
            "评论区截图页面",
            "物流页面-物流列表页面",
            "物流页面-物流跟踪页面",
            "物流页面-物流异常页面",
            "退款页面",
            "退货页面",
            "换货页面",
            "购物车页面",
            "店铺页面",
            "活动页面",
            "优惠券领取页面",
            "账单/账户页面",
            "个人信息页面",
            "投诉举报页面",
            "平台介入页面",
            "外部APP截图",
            "其他类别图片",
        ]
        pic_choices.append("跳过")

        # 获取当前数据的 output，并设置默认选中项
        current_output = item.get("output", None)

        if task_name == "dialog":
            default_index = (
                intend_choices.index(current_output) if current_output in intend_choices else len(intend_choices) - 1
            )
            choice = st.radio(
                "对话意图分类标注选项", intend_choices, index=default_index, key=f"choice_{current_index}"
            )
        elif task_name == "picture":
            default_index = pic_choices.index(current_output) if current_output in pic_choices else len(pic_choices) - 1
            choice = st.radio("图片分类标注选项", pic_choices, index=default_index, key=f"choice_{current_index}")
        else:
            st.error(f"未知任务名称: {task_name}")
            return

        if st.button("提交标注"):
            # 保存当前标注结果
            if choice and choice != "跳过":
                results.append({"number": current_index + 1, "id": item_id, "output": choice})
            elif choice == "跳过":
                results.append({"number": current_index + 1, "id": item_id, "output": ""})
            save_results(results, results_file_path)
            # 更新索引并刷新页面
            st.session_state.current_index += 1
            st.rerun()


if __name__ == "__main__":
    main()

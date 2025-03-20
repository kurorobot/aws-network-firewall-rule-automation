import streamlit as st
import boto3
import json
import re
import os
from suricata_rule_manager import extract_sids, add_rule, delete_rule, update_rule, RULES_FILE

st.set_page_config(page_title="Suricata ルール管理", layout="wide")

# セッション状態の初期化
if 'rules_loaded' not in st.session_state:
    st.session_state.rules_loaded = False
if 'rules_content' not in st.session_state:
    st.session_state.rules_content = ""
if 'sids' not in st.session_state:
    st.session_state.sids = []

# AWSプロファイルとリージョンの設定
aws_profile = st.sidebar.text_input("AWS プロファイル名", "my-sso-session")
aws_region = st.sidebar.text_input("AWS リージョン", "ap-northeast-3")
rule_group_arn = st.sidebar.text_input(
    "ルールグループ ARN", 
    "arn:aws:network-firewall:ap-northeast-3:123456789012:stateful-rulegroup/network-firewall-rulegroup-stateful-suricata-prod"
)

# タブの作成
tab1, tab2, tab3 = st.tabs(["ルール表示", "ルール管理", "Terraform出力"])

def load_rules_from_aws():
    """AWSからルールを取得"""
    try:
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        client = session.client("network-firewall")
        
        response = client.describe_rule_group(RuleGroupArn=rule_group_arn)
        rule_data = response["RuleGroup"]["RulesSource"].get("RulesString", "")
        
        # ルールをファイルに保存
        with open(RULES_FILE, "w", encoding="utf-8") as f:
            f.write(rule_data)
            
        st.session_state.rules_content = rule_data
        st.session_state.sids = extract_sids(RULES_FILE)
        st.session_state.rules_loaded = True
        return True
    except Exception as e:
        st.error(f"ルールの取得に失敗しました: {str(e)}")
        return False

def load_rules_from_file():
    """ローカルファイルからルールを読み込む"""
    try:
        # ファイルが存在しない場合は作成
        if not os.path.exists(RULES_FILE):
            with open(RULES_FILE, "w", encoding="utf-8") as f:
                pass
            
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            rule_data = f.read()
            
        st.session_state.rules_content = rule_data
        st.session_state.sids = extract_sids(RULES_FILE)
        st.session_state.rules_loaded = True
        return True
    except Exception as e:
        st.error(f"ルールの読み込みに失敗しました: {str(e)}")
        return False

# サイドバーにロードボタン
if st.sidebar.button("AWSからルールを取得"):
    load_rules_from_aws()

if st.sidebar.button("ローカルファイルからルールを読み込む"):
    load_rules_from_file()

# タブ1: ルール表示
with tab1:
    st.header("Suricata ルール")
    
    if st.session_state.rules_loaded:
        st.text_area("現在のルール", st.session_state.rules_content, height=400)
        st.write(f"合計 {len(st.session_state.sids)} 個のルールが見つかりました")
        st.write("SID リスト:")
        st.write(st.session_state.sids)
    else:
        st.info("サイドバーの「ローカルファイルからルールを読み込む」ボタンをクリックしてルールを読み込んでください")

# タブ2: ルール管理
with tab2:
    st.header("ルール管理")
    
    if not st.session_state.rules_loaded:
        st.info("サイドバーの「ローカルファイルからルールを読み込む」ボタンをクリックしてルールを読み込んでください")
    else:
        operation = st.radio("操作を選択", ["追加", "削除", "更新"])
        
        if operation == "追加":
            new_rule = st.text_area("追加するルールを入力してください")
            if st.button("ルールを追加"):
                if new_rule:
                    add_rule(new_rule, RULES_FILE)
                    st.success("ルールを追加しました")
                    # 再読み込み
                    with open(RULES_FILE, "r", encoding="utf-8") as f:
                        st.session_state.rules_content = f.read()
                    st.session_state.sids = extract_sids(RULES_FILE)
                else:
                    st.error("ルールを入力してください")
        
        elif operation == "削除":
            if not st.session_state.sids:
                st.warning("削除可能なルールがありません")
            else:
                sid_to_delete = st.selectbox("削除するSIDを選択", st.session_state.sids)
                if st.button("ルールを削除"):
                    delete_rule(sid_to_delete, RULES_FILE)
                    st.success(f"SID {sid_to_delete} のルールを削除しました")
                    # 再読み込み
                    with open(RULES_FILE, "r", encoding="utf-8") as f:
                        st.session_state.rules_content = f.read()
                    st.session_state.sids = extract_sids(RULES_FILE)
        
        elif operation == "更新":
            if not st.session_state.sids:
                st.warning("更新可能なルールがありません")
            else:
                sid_to_update = st.selectbox("更新するSIDを選択", st.session_state.sids)
                
                # 選択したSIDの現在のルールを表示
                current_rule = ""
                with open(RULES_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        if f"sid:{sid_to_update};" in line:
                            current_rule = line.strip()
                            break
                
                st.text_area("現在のルール", current_rule, disabled=True)
                new_rule = st.text_area("新しいルールを入力", current_rule)
                
                if st.button("ルールを更新"):
                    update_rule(sid_to_update, new_rule, RULES_FILE)
                    st.success(f"SID {sid_to_update} のルールを更新しました")
                    # 再読み込み
                    with open(RULES_FILE, "r", encoding="utf-8") as f:
                        st.session_state.rules_content = f.read()

# タブ3: Terraform出力
with tab3:
    st.header("Terraform設定")
    
    if not st.session_state.rules_loaded:
        st.info("サイドバーの「ローカルファイルからルールを読み込む」ボタンをクリックしてルールを読み込んでください")
    else:
        # Terraformリソース名
        resource_name = st.text_input("リソース名", "network_firewall_suricata_rules")
        
        # Terraformコード生成
        terraform_code = f'''
resource "aws_networkfirewall_rule_group" "{resource_name}" {{
  capacity = 100
  name     = "network-firewall-rulegroup-stateful-suricata-prod"
  type     = "STATEFUL"
  
  rule_group {{
    rules_source {{
      rules_string = <<EOT
{st.session_state.rules_content}
EOT
    }}
  }}
  
  tags = {{
    Name = "network-firewall-rulegroup-stateful-suricata-prod"
  }}
}}
'''
        
        st.code(terraform_code, language="hcl")
        
        # ダウンロードボタン
        if st.button("Terraformファイルをダウンロード"):
            tf_filename = f"{resource_name}.tf"
            with open(tf_filename, "w", encoding="utf-8") as f:
                f.write(terraform_code)
            st.success(f"{tf_filename} を保存しました") 
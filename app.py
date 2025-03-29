import streamlit as st
import boto3
import json
import re
import os
import subprocess
import tempfile
from suricata_rule_manager import extract_sids, add_rule, delete_rule, update_rule

# ページ設定
st.set_page_config(
    page_title="AWS Network Firewall 管理",
    page_icon="🔥",
    layout="wide"
)

# リージョンとプロファイルの設定
REGIONS = {
    "東京": {
        "code": "ap-northeast-1",
        "profile": "my-sso-session",
        "rule_groups": {
            "prod": "tokyo-network-firewall-rulegroup-stateful-suricata-prod",
            "nonprod": "tokyo-network-firewall-rulegroup-stateful-suricata-nonprod"
        },
        "rules_file": {
            "prod": "environments/tokyo/suricata-prod.rules",
            "nonprod": "environments/tokyo/suricata-nonprod.rules"
        },
        "terraform_dir": "environments/tokyo"
    },
    "シンガポール": {
        "code": "ap-southeast-1",
        "profile": "singapore-profile",
        "rule_groups": {
            "prod": "singapore-network-firewall-rulegroup-stateful-suricata-prod",
            "nonprod": "singapore-network-firewall-rulegroup-stateful-suricata-nonprod"
        },
        "rules_file": {
            "prod": "environments/singapore/suricata-prod.rules",
            "nonprod": "environments/singapore/suricata-nonprod.rules"
        },
        "terraform_dir": "environments/singapore"
    },
    "バージニア": {
        "code": "us-east-1",
        "profile": "virginia-profile",
        "rule_groups": {
            "prod": "virginia-network-firewall-rulegroup-stateful-suricata-prod",
            "nonprod": "virginia-network-firewall-rulegroup-stateful-suricata-nonprod"
        },
        "rules_file": {
            "prod": "environments/virginia/suricata-prod.rules",
            "nonprod": "environments/virginia/suricata-nonprod.rules"
        },
        "terraform_dir": "environments/virginia"
    }
}

# タイトル
st.title("AWS Network Firewall 管理")

# タブの作成
tabs = st.tabs(["ルール取得", "ルール管理", "Terraform 適用"])

# ルール取得タブ
with tabs[0]:
    st.header("AWS Network Firewall からルールを取得")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_region = st.selectbox("リージョンを選択", list(REGIONS.keys()))
    
    with col2:
        env_type = st.radio("環境タイプ", ["prod", "nonprod"], horizontal=True)
    
    if st.button("ルールを取得"):
        with st.spinner(f"{selected_region}リージョンからルールを取得中..."):
            try:
                # AWS クライアント作成
                region_info = REGIONS[selected_region]
                session = boto3.Session(
                    profile_name=region_info["profile"], 
                    region_name=region_info["code"]
                )
                client = session.client("network-firewall")
                
                # ルールグループ名を取得
                rule_group_name = region_info["rule_groups"][env_type]
                
                # ルールグループARNを取得
                response = client.list_rule_groups()
                rule_group_arn = None
                
                for group in response.get("RuleGroups", []):
                    if group["Name"] == rule_group_name:
                        rule_group_arn = group["Arn"]
                        break
                
                if not rule_group_arn:
                    st.error(f"ルールグループ '{rule_group_name}' が見つかりませんでした。")
                else:
                    # ルールを取得
                    response = client.describe_rule_group(RuleGroupArn=rule_group_arn)
                    rule_data = response["RuleGroup"]["RulesSource"].get("RulesString", "")
                    
                    # ファイルに保存
                    rules_file = region_info["rules_file"][env_type]
                    os.makedirs(os.path.dirname(rules_file), exist_ok=True)
                    
                    with open(rules_file, "w", encoding="utf-8") as f:
                        f.write(rule_data)
                    
                    st.success(f"ルールを {rules_file} に保存しました。")
                    
                    # ルールを表示
                    st.subheader("取得したルール")
                    st.code(rule_data)
            
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

# ルール管理タブ
with tabs[1]:
    st.header("Suricata ルール管理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_region = st.selectbox("リージョンを選択", list(REGIONS.keys()), key="region_select_tab2")
    
    with col2:
        env_type = st.radio("環境タイプ", ["prod", "nonprod"], horizontal=True, key="env_type_tab2")
    
    # ルールファイルのパスを取得
    region_info = REGIONS[selected_region]
    rules_file = region_info["rules_file"][env_type]
    
    # ファイルが存在するか確認
    if not os.path.exists(rules_file):
        st.warning(f"ルールファイル {rules_file} が存在しません。「ルール取得」タブでルールを取得してください。")
    else:
        # ルールファイルを読み込む
        with open(rules_file, "r", encoding="utf-8") as f:
            rules_content = f.read()
        
        # 操作タイプを選択
        operation = st.radio("操作を選択", ["ルール追加", "ルール削除", "ルール更新", "ルール表示"], horizontal=True)
        
        if operation == "ルール追加":
            new_rule = st.text_area("新しいルールを入力", height=100)
            if st.button("ルールを追加"):
                if new_rule.strip():
                    add_rule(new_rule, rules_file)
                    st.success("ルールを追加しました。")
                    st.rerun()
                else:
                    st.error("ルールを入力してください。")
        
        elif operation == "ルール削除":
            # SIDの一覧を取得
            sids = extract_sids(rules_file)
            
            if not sids:
                st.warning("ルールファイルにSIDが見つかりません。")
            else:
                selected_sid = st.selectbox("削除するルールのSIDを選択", sids)
                
                # 選択されたSIDのルールを表示
                with open(rules_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if f"sid:{selected_sid};" in line:
                            st.code(line)
                            break
                
                if st.button("ルールを削除"):
                    delete_rule(selected_sid, rules_file)
                    st.success(f"SID {selected_sid} のルールを削除しました。")
                    st.rerun()
        
        elif operation == "ルール更新":
            # SIDの一覧を取得
            sids = extract_sids(rules_file)
            
            if not sids:
                st.warning("ルールファイルにSIDが見つかりません。")
            else:
                selected_sid = st.selectbox("更新するルールのSIDを選択", sids)
                
                # 選択されたSIDのルールを取得
                current_rule = ""
                with open(rules_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if f"sid:{selected_sid};" in line:
                            current_rule = line.strip()
                            break
                
                st.subheader("現在のルール")
                st.code(current_rule)
                
                st.subheader("更新後のルール")
                updated_rule = st.text_area("ルールを編集", current_rule, height=100)
                
                if st.button("ルールを更新"):
                    if updated_rule.strip():
                        update_rule(selected_sid, updated_rule, rules_file)
                        st.success(f"SID {selected_sid} のルールを更新しました。")
                        st.rerun()
                    else:
                        st.error("ルールを入力してください。")
        
        elif operation == "ルール表示":
            st.subheader("現在のルール")
            st.code(rules_content)

# Terraform 適用タブ
with tabs[2]:
    st.header("Terraform でルールを適用")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_region = st.selectbox("リージョンを選択", list(REGIONS.keys()), key="region_select_tab3")
    
    with col2:
        env_type = st.radio("環境タイプ", ["prod", "nonprod"], horizontal=True, key="env_type_tab3")
    
    # リージョン情報を取得
    region_info = REGIONS[selected_region]
    terraform_dir = region_info["terraform_dir"]
    rule_group_name = region_info["rule_groups"][env_type]
    
    # Terraform コマンドを実行する関数
    def run_terraform_command(command, working_dir):
        try:
            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    # Terraform 初期化
    if st.button("Terraform 初期化"):
        with st.spinner("Terraform を初期化中..."):
            success, output = run_terraform_command(["terraform", "init"], terraform_dir)
            if success:
                st.success("Terraform の初期化が完了しました。")
            else:
                st.error(f"Terraform の初期化に失敗しました: {output}")
            st.code(output)
    
    # Terraform 差分確認
    if st.button("差分を確認"):
        with st.spinner("差分を確認中..."):
            target_option = f"-target=aws_networkfirewall_rule_group.{env_type}"
            success, output = run_terraform_command(
                ["terraform", "plan", target_option], 
                terraform_dir
            )
            if success:
                st.success("差分の確認が完了しました。")
            else:
                st.error(f"差分の確認に失敗しました: {output}")
            st.code(output)
    
    # Terraform 適用
    if st.button("変更を適用"):
        confirm = st.checkbox("本当に適用しますか？")
        if confirm:
            with st.spinner("変更を適用中..."):
                target_option = f"-target=aws_networkfirewall_rule_group.{env_type}"
                success, output = run_terraform_command(
                    ["terraform", "apply", "-auto-approve", target_option], 
                    terraform_dir
                )
                if success:
                    st.success("変更の適用が完了しました。")
                else:
                    st.error(f"変更の適用に失敗しました: {output}")
                st.code(output)
        else:
            st.warning("適用を確認するにはチェックボックスをオンにしてください。")

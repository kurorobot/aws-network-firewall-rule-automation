import re
import os

RULES_FILE = "./suricata-prod.rules"  # Suricata ルールファイルのパス

def extract_sids(file_path):
    """Suricataルールファイルから SID (ルールID) を抽出"""
    sid_pattern = re.compile(r"sid:(\d+);")
    sids = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = sid_pattern.search(line)
            if match:
                sids.append(int(match.group(1)))

    return sids

def add_rule(rule_text, file_path):
    """新しいルールを追加"""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(rule_text + "\n")
    
    print(f"ルールを追加しました: {rule_text}")

def delete_rule(sid, file_path):
    """SID に基づいてルールを削除"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
            if f"sid:{sid};" not in line:
                f.write(line)
            else:
                print(f"ルールを削除しました: {line.strip()}")

def update_rule(sid, new_rule, file_path):
    """SID に基づいてルールを更新"""
    found = False
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
            if f"sid:{sid};" in line:
                f.write(new_rule + "\n")
                found = True
                print(f"ルールを更新しました: {new_rule}")
            else:
                f.write(line)

    if not found:
        print(f"SID {sid} のルールが見つかりませんでした。")

# メインの実行部分は削除（Streamlitアプリで代替するため）

import streamlit as st

# 仮のデータベース（セッションステートを利用）
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# ユーザー情報の入力
user_name = st.text_input("ユーザー名を入力してください")
match_id = st.text_input("対戦IDを入力してください")

if st.button("対戦に参加"):
    if match_id not in st.session_state.matches:
        st.session_state.matches[match_id] = {
            'players': [user_name],
            'current_turn': 0,
            'questions': [],
            'scores': {user_name: 0}
        }
    else:
        st.session_state.matches[match_id]['players'].append(user_name)
        st.session_state.matches[match_id]['scores'][user_name] = 0

    st.success(f"{user_name} が対戦 {match_id} に参加しました。")
# 対戦が開始されたかチェック
if match_id in st.session_state.matches:
    match = st.session_state.matches[match_id]
    
    if len(match['players']) == 2:  # 2人揃ったら対戦開始
        current_player = match['players'][match['current_turn'] % 2]
        
        st.write(f"現在のターン: {current_player}")
        
        if current_player == user_name:
            # ユーザーが問題を作成
            question = st.text_input("問題を作成してください (〇か×かで答えられる形式)")
            correct_answer = st.selectbox("正しい答えを選んでください", ["〇", "×"])
            
            if st.button("問題を出題"):
                match['questions'].append({
                    'question': question,
                    'answer': correct_answer,
                    'player': current_player
                })
                match['current_turn'] += 1
                st.success(f"問題が出題されました。次のターンをお待ちください。")
        else:
            # 相手のターンを待つ
            if len(match['questions']) > match['current_turn']:
                question = match['questions'][match['current_turn']]
                st.write(f"{question['player']} からの問題: {question['question']}")
                
                user_answer = st.selectbox("答えを選んでください", ["〇", "×"])
                
                if st.button("回答を送信"):
                    if user_answer == question['answer']:
                        match['scores'][user_name] += 1
                        st.success("正解！")
                    else:
                        st.error("不正解…")
                    
                    match['current_turn'] += 1
                    st.success("次のターンをお待ちください。")
if match_id in st.session_state.matches:
    match = st.session_state.matches[match_id]
    
    if match['current_turn'] >= len(match['players']) * 5:  # 例えば5ターンごとに対戦を終了
        st.write("対戦が終了しました！")

        # スコアの表示
        for player, score in match['scores'].items():
            st.write(f"{player}: {score} 点")
        
        winner = max(match['scores'], key=match['scores'].get)
        st.write(f"勝者は {winner} です！")

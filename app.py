from flask import Flask, render_template, request, jsonify
from nba_card_simulator import CardSimulator
import json
import os

app = Flask(__name__)
simulator = CardSimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure', methods=['POST'])
def configure():
    data = request.json
    settings = {}
    
    if 'jackpot_probability' in data:
        settings['jackpot_probability'] = 1 / float(data['jackpot_probability'])
    if 'signature_pack_price' in data:
        settings['signature_pack_price'] = float(data['signature_pack_price'])
    if 'signature_pack_cost' in data:
        settings['signature_pack_cost'] = float(data['signature_pack_cost'])
    if 'material_pack_price' in data:
        settings['material_pack_price'] = float(data['material_pack_price'])
    if 'material_pack_cost' in data:
        settings['material_pack_cost'] = float(data['material_pack_cost'])
    if 'shipping_fee' in data:
        settings['shipping_fee'] = float(data['shipping_fee'])
    if 'jackpot_cost' in data:
        settings['jackpot_cost'] = float(data['jackpot_cost'])
    
    # 應用設定
    for key, value in settings.items():
        setattr(simulator, key, value)
    
    return jsonify({'status': 'success'})

@app.route('/open_pack', methods=['POST'])
def open_pack():
    data = request.json
    pack_type = "簽名卡包" if data.get('pack_type') == '1' else "物料卡包"
    
    # 生成卡片
    cards = simulator.generate_pack(pack_type)
    
    # 計算收入和成本
    revenue, cost, has_jackpot = simulator.calculate_pack_profit(cards, pack_type)
    
    # 更新統計數據
    simulator.total_revenue += revenue
    simulator.total_cost += cost
    if has_jackpot:
        simulator.total_jackpot_hits += 1
        simulator.advance_jackpot()
    
    # 準備回應數據
    response = {
        'cards': [{'team': team, 'type': card_type} for team, card_type in cards],
        'revenue': revenue,
        'cost': cost,
        'profit': revenue - cost,
        'has_jackpot': has_jackpot,
        'jackpot_team': simulator.get_current_jackpot_team() if has_jackpot else None,
        'next_jackpot_team': simulator.jackpot_pool[simulator.current_jackpot_index + 1] if has_jackpot and simulator.current_jackpot_index < len(simulator.jackpot_pool) - 1 else None,
        'total_revenue': simulator.total_revenue,
        'total_cost': simulator.total_cost,
        'total_profit': simulator.total_revenue - simulator.total_cost,
        'total_jackpot_hits': simulator.total_jackpot_hits
    }
    
    return jsonify(response)

@app.route('/get_stats')
def get_stats():
    return jsonify({
        'jackpot_team': simulator.get_current_jackpot_team(),
        'next_jackpot_team': simulator.jackpot_pool[simulator.current_jackpot_index + 1] if simulator.current_jackpot_index < len(simulator.jackpot_pool) - 1 else None,
        'jackpot_probability': simulator.jackpot_probability,
        'cards_per_pack': simulator.cards_per_pack,
        'total_revenue': simulator.total_revenue,
        'total_cost': simulator.total_cost,
        'total_profit': simulator.total_revenue - simulator.total_cost,
        'total_jackpot_hits': simulator.total_jackpot_hits
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('RENDER'):
        # 在 Render 上運行
        app.run(host='0.0.0.0', port=port)
    else:
        # 本地開發環境
        print("\n=== NBA 球星卡抽卡模擬器 ===")
        print("本地訪問網址：http://localhost:5000")
        print("同網路其他設備訪問：http://[您電腦的IP地址]:5000")
        print("按 Ctrl+C 可以停止程式")
        print("===========================\n")
        app.run(host='0.0.0.0', port=port, debug=True) 
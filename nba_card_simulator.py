import random
import time
import cursor
from typing import List, Dict, Tuple
import math

# NBA 隊伍列表（30支球隊）
NBA_TEAMS = [
    "Lakers", "Celtics", "Warriors", "Bulls", "Heat",
    "Knicks", "Nets", "Bucks", "Suns", "Mavericks",
    "Clippers", "Nuggets", "76ers", "Raptors", "Grizzlies",
    "Pelicans", "Timberwolves", "Thunder", "Jazz", "Kings",
    "Spurs", "Rockets", "Hornets", "Magic", "Pistons",
    "Pacers", "Cavaliers", "Hawks", "Wizards", "Trail Blazers"
]

class CardSimulator:
    def __init__(self):
        """
        初始化抽卡模擬器
        """
        self.cards_per_pack = 6
        self.packs_per_simulation = 10
        self.total_cards = self.cards_per_pack * self.packs_per_simulation
        
        # 預設成本與售價設定
        self.signature_pack_price = 80   # 簽名卡包售價
        self.signature_pack_cost = 50    # 簽名卡包成本
        self.material_pack_price = 60    # 物料卡包售價
        self.material_pack_cost = 30     # 物料卡包成本
        self.shipping_fee = 25           # 運費
        self.jackpot_cost = 300          # 中獎額外成本
        
        # 中獎機率設定
        self.jackpot_probability = 0.1   # 預設每10包中1包
        
        # 統計數據
        self.total_revenue = 0
        self.total_cost = 0
        self.total_jackpot_hits = 0
        self.pack_results = []
        
        # 初始化外部獎池
        self.jackpot_pool = self.initialize_jackpot_pool()
        self.current_jackpot_index = 0

    def initialize_jackpot_pool(self) -> List[str]:
        """
        初始化外部獎池，根據中獎機率生成獎池卡
        :return: 獎池卡列表
        """
        # 計算需要多少張獎池卡
        total_packs = 100  # 假設總共開100包
        expected_hits = int(total_packs * self.jackpot_probability)
        jackpot_teams = random.choices(NBA_TEAMS, k=expected_hits)
        return jackpot_teams

    def get_current_jackpot_team(self) -> str:
        """
        獲取當前獎池隊伍
        :return: 當前獎池隊伍
        """
        return self.jackpot_pool[self.current_jackpot_index]

    def advance_jackpot(self):
        """
        推進獎池到下一個隊伍
        """
        if self.current_jackpot_index < len(self.jackpot_pool) - 1:
            self.current_jackpot_index += 1

    def generate_pack(self, pack_type: str) -> List[Tuple[str, str]]:
        """
        生成一包卡片
        :param pack_type: 卡包類型（"簽名卡包" 或 "物料卡包"）
        :return: 卡片列表，每個元素為 (隊伍名稱, 卡片類型)
        """
        pack = []
        # 生成5張普通卡
        for _ in range(5):
            team = random.choice(NBA_TEAMS)
            pack.append((team, "普通卡"))
        
        # 生成1張特殊卡
        team = random.choice(NBA_TEAMS)
        pack.append((team, pack_type))
        
        return pack

    def calculate_pack_profit(self, cards: List[Tuple[str, str]], pack_type: str) -> Tuple[float, float, bool]:
        """
        計算一包卡片的收入和成本
        :param cards: 卡片列表
        :param pack_type: 卡包類型
        :return: (收入, 成本, 是否中獎)
        """
        revenue = 0
        cost = 0
        has_jackpot = False

        # 根據卡包類型設定價格
        if pack_type == "簽名卡包":
            revenue = self.signature_pack_price
            cost = self.signature_pack_cost
        else:  # 物料卡包
            revenue = self.material_pack_price
            cost = self.material_pack_cost

        # 檢查是否中獎
        for team, card_type in cards:
            if team == self.get_current_jackpot_team():
                has_jackpot = True
                break

        # 加入運費
        revenue += self.shipping_fee
        
        # 如果中獎，加入額外成本
        if has_jackpot:
            cost += self.jackpot_cost

        return revenue, cost, has_jackpot

    def display_jackpot_info(self):
        """
        顯示獎池資訊
        """
        print("\n" + "="*50)
        print("🎯 外部獎池資訊")
        print(f"📊 當前獎池隊伍：{self.get_current_jackpot_team()}")
        if self.current_jackpot_index < len(self.jackpot_pool) - 1:
            print(f"📊 下一張中獎隊伍：{self.jackpot_pool[self.current_jackpot_index + 1]}")
        print(f"📦 每包卡片數：{self.cards_per_pack}")
        print(f"🎲 中獎機率：{self.jackpot_probability*100:.1f}% (每{int(1/self.jackpot_probability)}包中1包)")
        print("="*50 + "\n")

    def display_statistics(self):
        """
        顯示統計資訊
        """
        print("\n" + "="*50)
        print("📈 統計資訊")
        print(f"💰 總收入：${self.total_revenue:,.0f}")
        print(f"💸 總成本：${self.total_cost:,.0f}")
        print(f"💵 淨利潤：${(self.total_revenue - self.total_cost):,.0f}")
        print(f"🎯 中獎次數：{self.total_jackpot_hits}")
        print("="*50 + "\n")

    def simulate_pack_opening(self):
        """
        模擬開包過程，包含動畫效果
        """
        cursor.hide()  # 隱藏游標
        
        # 顯示獎池資訊
        self.display_jackpot_info()
        
        while True:
            # 選擇卡包類型
            print("\n請選擇要開啟的卡包類型：")
            print("1. 簽名卡包 (售價: ${}, 成本: ${})".format(
                self.signature_pack_price, self.signature_pack_cost))
            print("2. 物料卡包 (售價: ${}, 成本: ${})".format(
                self.material_pack_price, self.material_pack_cost))
            
            while True:
                try:
                    choice = input("\n請選擇 (1/2): ")
                    if choice in ["1", "2"]:
                        break
                    print("無效的選擇，請重試。")
                except ValueError:
                    print("請輸入有效的數字。")
            
            pack_type = "簽名卡包" if choice == "1" else "物料卡包"
            
            print(f"\n📦 開啟{pack_type}...\n")
            time.sleep(0.5)
            
            # 生成一包卡片
            cards = self.generate_pack(pack_type)
            
            # 顯示卡片
            for i, (card, card_type) in enumerate(cards, 1):
                print(f"第 {i} 張卡: ", end="", flush=True)
                time.sleep(0.5)  # 等待效果
                print(f"{card} ({card_type})")
                time.sleep(0.3)  # 卡片之間的間隔

            # 計算收入和成本
            revenue, cost, has_jackpot = self.calculate_pack_profit(cards, pack_type)
            
            # 更新統計數據
            self.total_revenue += revenue
            self.total_cost += cost
            if has_jackpot:
                self.total_jackpot_hits += 1
                self.advance_jackpot()  # 中獎時推進獎池

            # 顯示本包結果
            print("\n" + "="*30)
            if has_jackpot:
                print(f"🎉 恭喜！你抽到了 {self.get_current_jackpot_team()} 的卡片！")
                print(f"🔄 獎池推進到下一張卡")
                if self.current_jackpot_index < len(self.jackpot_pool) - 1:
                    print(f"🎯 下一張中獎隊伍：{self.jackpot_pool[self.current_jackpot_index + 1]}")
            else:
                print("😢 很遺憾，這次沒有中獎...")
            print(f"💰 本包收入：${revenue:,.0f}")
            print(f"💸 本包成本：${cost:,.0f}")
            print(f"💵 本包利潤：${(revenue - cost):,.0f}")
            print("="*30 + "\n")
            
            # 顯示總體統計
            self.display_statistics()
            
            # 詢問是否繼續
            while True:
                choice = input("是否繼續開包？(y/n): ").lower()
                if choice in ["y", "n"]:
                    break
                print("請輸入 y 或 n")
            
            if choice == "n":
                break

        cursor.show()  # 顯示游標

def configure_settings() -> Dict:
    """
    配置模擬器設定
    :return: 設定字典
    """
    settings = {}
    
    print("\n是否要修改預設設定？(y/n)")
    if input().lower() != "y":
        return settings
    
    print("\n請輸入新的設定值（直接按 Enter 保持預設值）：")
    
    # 中獎機率設定
    try:
        prob = input("每10包中獎機率 (預設: 1，表示每10包中1包): ")
        if prob:
            settings["jackpot_probability"] = 1 / float(prob)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    # 簽名卡包設定
    try:
        price = input("簽名卡包售價 (預設: 80): ")
        if price:
            settings["signature_pack_price"] = float(price)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    try:
        cost = input("簽名卡包成本 (預設: 50): ")
        if cost:
            settings["signature_pack_cost"] = float(cost)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    # 物料卡包設定
    try:
        price = input("物料卡包售價 (預設: 60): ")
        if price:
            settings["material_pack_price"] = float(price)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    try:
        cost = input("物料卡包成本 (預設: 30): ")
        if cost:
            settings["material_pack_cost"] = float(cost)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    # 運費設定
    try:
        fee = input("運費 (預設: 25): ")
        if fee:
            settings["shipping_fee"] = float(fee)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    # 中獎額外成本設定
    try:
        cost = input("中獎額外成本 (預設: 300): ")
        if cost:
            settings["jackpot_cost"] = float(cost)
    except ValueError:
        print("無效的輸入，使用預設值")
    
    return settings

def main():
    print("\n" + "="*50)
    print("🎮 NBA 球星卡抽卡模擬器")
    print("="*50)
    
    # 配置設定
    settings = configure_settings()
    
    # 創建模擬器實例
    simulator = CardSimulator()
    
    # 應用自定義設定
    for key, value in settings.items():
        setattr(simulator, key, value)
    
    # 開始模擬
    simulator.simulate_pack_opening()
    
    # 等待用戶確認
    input("\n按 Enter 鍵退出...")

if __name__ == "__main__":
    main() 
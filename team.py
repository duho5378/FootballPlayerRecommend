import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import re

def calculate_cosine_similarity(team1, team2):
        # team1_vector = team1.get_team_vector()
        # team2_vector = team2.get_team_vector()

        # Tính cosine similarity giữa hai vector đội hình
        similarity = np.dot(team1, team2) / (np.linalg.norm(team1) * np.linalg.norm(team2))
        return similarity

class FootballTeam:
    def __init__(self, formation):
        self.formation = formation
        self.team_positions = self.generate_positions(formation)

    def generate_positions(self, formation):
        positions = {
            "gk": None
        }
        if formation == '3142':
            positions.update({
                'cb1': None, 'cb2': None, 'cb3': None, 'cdm': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'st1': None, 'st2': None
            })
        elif formation == '3412':
            positions.update({'cb1': None, 'cb2': None, 'cb3': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None,'cam': None, 'st1': None, 'st2': None})
        elif formation == '3421':
            positions.update({'cb1': None, 'cb2': None, 'cb3': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'rf': None, 'lf': None, 'st': None})
        elif formation == '343':
            positions.update({'cb1': None, 'cb2': None, 'cb3': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'rw': None, 'st': None, 'lw': None})
        elif formation == '3511':
            positions.update({'cb1': None, 'cb2': None, 'cb3': None, 'rm': None, 'cdm1': None, 'cm': None, 'cdm2': None, 'lm': None, 'cf': None, 'st': None})
        elif formation == '352':
            positions.update({'cb1': None, 'cb2': None, 'cb3': None, 'cdm1': None, 'cdm2': None, 'rm': None, 'cam': None, 'lm': None, 'st1': None, 'st2': None})
        elif formation == '41212':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cdm': None, 'rm': None, 'lm': None, 'cam': None, 'st1': None, 'st2': None})
        elif formation == '4141':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cdm': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'st': None})
        elif formation == '4222':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cdm1': None, 'cdm2': None, 'cam1': None, 'cam2': None, 'st1': None, 'st2': None})
        elif formation == '4231':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cdm1': None, 'cdm2': None, 'rm': None, 'cam': None, 'lm': None, 'st': None})
        elif formation == '4312':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cm1': None, 'cm2': None, 'cm3': None, 'cam': None, 'st1': None, 'st2': None})
        elif formation == '4321':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cm1': None, 'cm2': None, 'cm3': None, 'rf': None, 'lf': None, 'st': None})
        elif formation == '433':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'cm1': None, 'cm2': None, 'cm3': None, 'rw': None, 'st': None, 'lw': None})
        elif formation == '4411':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'cf': None, 'st': None})
        elif formation == '442':
            positions.update({'rb': None, 'cb1': None, 'cb2': None, 'lb': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'st1': None, 'st2': None})
        elif formation == '532':
            positions.update({'rwb': None, 'cb1': None, 'cb2': None, 'cb3': None, 'lwb': None, 'cm1': None, 'cm2': None, 'cm3': None, 'st1': None, 'st2': None})
        elif formation == '541':
            positions.update({'rwb': None, 'cb1': None, 'cb2': None, 'cb3': None, 'lwb': None, 'rm': None, 'cm1': None, 'cm2': None, 'lm': None, 'st': None})
        return positions

    def add_player(self, position, player_id):
        if position in self.team_positions:
            self.team_positions[position] = player_id
            return True
        else:
            return False

    def update_player(self, position, player_id):
        if position in self.team_positions:
            self.team_positions[position] = player_id
            return True
        else:
            return False

    def remove_player(self, position):
        if position in self.team_positions:
            self.team_positions[position] = None
            return True
        else:
            return False
        
        
    def recommend_lineup(self):
        
        number_none_position = 0
        none_position = []
        has_position = []
        max_cosine = 0
        recommend_form = dict()
        
        for i in self.team_positions:
            if self.team_positions[i] is not None:
                number_none_position += 1
                if i != 'gk':
                    has_position.append(i)
            else:
                none_position.append(i)
                
        if number_none_position == 0:
            print("Hãy thêm cầu thủ vào đội hình")
            return
        
        if self.team_positions['gk'] is None:
            return
        
        current_form = []
        for i in has_position:
            # pos_file = re.sub(r'\d', '', i)
            player = pd.read_csv(f'C:/Users/duyhd/OneDrive/Desktop/seminar/data/player_stat_fl_pos/all_player.csv')
            # print(self.team_positions[f'{i}'])
            # lỗi do chưa chuyển file tổng thành file csv. Cần chuyển đổi file tổng để có thể lấy được tất cả cầu thủ.
            row = player[player['sofifa_id'] == int(self.team_positions[f'{i}'])].iloc[0][2:42].to_list()
            # print(row)
            current_form.extend(row)
        
        
        with open(f'C:/Users/duyhd/OneDrive/Desktop/seminar/data/lineup/lineup_{self.formation}.json', 'r') as file:
            data = json.load(file)
        for i in range(0, len(data)):
            sample_form = []
            # print(data[i])
            for pos in has_position:
                pos_file = re.sub(r'\d', '', pos)
                player = pd.read_csv(f'C:/Users/duyhd/OneDrive/Desktop/seminar/data/recommend_csv/{pos_file}_player.csv')
                # print(data[i][pos])
                row = player[player['sofifa_id'] == int(data[i][pos])].iloc[0][2:42].to_list()
                sample_form.extend(row)
            cosine = calculate_cosine_similarity(current_form, sample_form)
            if cosine > max_cosine:
                max_cosine = cosine
                recommend_form = data[i]
                
        for pos in none_position:
            pos_file = re.sub(r'\d', '', pos)
            similarity = pd.read_csv(f'C:/Users/duyhd/OneDrive/Desktop/seminar/data/cosine_player/{pos_file}_similarity.csv')
            max_index = similarity[recommend_form[pos]].idxmax()
            # print(max_index)
            self.team_positions[pos] = int(similarity.iloc[max_index][0])

        
        return True
    
    
            

# Sử dụng lớp FootballTeam
team_433 = FootballTeam("433")
team_532 = FootballTeam("532")

# Thêm cầu thủ cho đội 4-3-3
# team_433.add_player("GK", "Nguyễn Văn A")
# team_433.add_player("CB1", "Trần Văn B")
# team_433.add_player("CM1", "Phạm Văn C")

# Thêm cầu thủ cho đội 5-3-2
team_532.add_player("gk", "158023")
team_532.add_player("cb1", "20801")
team_532.add_player("cm1", "192985")

team_532.recommend_lineup()

# Hiển thị đội hình
# print("Đội hình 4-3-3:")
# print(team_433.team_positions)

# print("\nĐội hình 5-3-2:")
print(team_532.team_positions)


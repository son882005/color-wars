"""
Ý tưởng:
Bỏ qua nhánh không cần thiết
Tăng tốc cực mạnh
def alphabeta(state, depth, alpha, beta, maximizing):
    return

#Move Ordering
moves.sort(key=heuristic_score, reverse=True)
Ưu tiên:
threat cao
danger thấp
material cao

#expand top-K
moves = moves[:K]
giúp:
giữ performance
không lag animation

def evaluate(state):
    material_norm
    + mobility_norm
    + threat_norm
    - danger_norm
    + stability_norm
#Test từng bước
#Noise
if score_diff < 0.08:
    random chọn top 2 (85/15)

#mỗi lượt AI mất bao lâu?
start = time.time()
move = get_ai_move(...)
end = time.time()
print(end - start)
"""
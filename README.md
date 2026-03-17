# Color Wars

Game chiến thuật theo lượt viết bằng Pygame.
Game khởi động ở chế độ mặc định `pvbot` (đấu với AI)

## Tính năng hiện tại

- Bàn cờ 5x5.
- Người chơi điều khiển bằng chuột, AI điều khiển Red.
- Lượt khởi đầu của mỗi bên:
  - Là lượt duy nhất được đặt vào ô trống.
  - Ô khởi đầu nhận 3 chấm.
- Sau khi đã có ô khởi đầu:
  - Chỉ được đặt vào ô đã có điểm của chính mình.
  - Không được đặt vào ô trống nữa.
- Có cơ chế nổ dây chuyền và đồng hóa ô lân cận.
- HUD hiển thị:
  - Điểm Blue/Red ở phía trên bàn cờ
  - Chế độ + lượt hiện tại/người thắng ở bên trái bàn cờ
  - Hướng dẫn phím tắt ở bên phải bàn cờ

## Luật nổ và đồng hóa

- Khi một ô đạt đủ 4 chấm:
  - Ô đó nổ, Dot được phân tán ra 4 hướng (trên, dưới, trái, phải).
  - Ô bị trúng sẽ bị đồng hóa về màu của bên gây nổ và cộng thêm 1 dot.
  - Nếu ô lân cận đạt mốc 4 chấm, tiếp tục nổ dây chuyền.

## Điều kiện thắng thua

- Mục tiêu: chiếm 100% bàn cờ bằng màu của mình và xóa sạch hoàn toàn màu đối thủ.

## AI hiện tại

- Thuật toán AI: `ai\ai.get_ai_move(board, dots)`.
- Mỗi lượt AI:
  - Lấy nước hợp lệ từ cùng bộ rule với controller.
  - Mô phỏng từng nước.
  - Chấm điểm trạng thái theo số ô chiếm đóng (`Red - Blue`) và chọn nước điểm cao nhất.

## Kiến trúc rule dùng chung

- Rule game được đặt tại `src/engine/rules.py`.
- Xử lý nổ dây chuyền được đặt tại `src/engine/explosion.py`.
- `controller` và `AI` cùng gọi chung engine.

## Cấu trúc mã nguồn

- `src/main.py`: điểm vào ứng dụng (init/quit pygame).
- `src/game/state.py`: `GameState` (board, dots, current_player, winner, turn_count).
- `src/game/loop.py`: game loop (xử lý event, mode pvp/pvbot, vẽ scene mỗi frame).
- `src/controller.py`: logic xử lý nước đi trên `GameState` (apply move, tính điểm, xác định winner).
- `src/engine/rules.py`: định nghĩa rule (capacity, valid moves, constants).
- `src/engine/explosion.py`: giải nổ dây chuyền theo BFS.
- `src/ai/ai.py`: logic chọn nước cho Red (mô phỏng và đánh giá board).
- `src/view.py`: phần UI/render (vẽ board, dot, HUD, map vị trí chuột -> ô).

## Chạy dự án

1. Cài Python 3.10+.
2. Cài dependency:

```bash
pip install -r requirements.txt
```

3. Chạy game:

```bash
python -m src.main
```

## Phím tắt trong game

- `M`: Chuyển nhanh giữa `pvp` và `pvbot` (đồng thời reset ván mới).
- `R`: Khởi động lại ván hiện tại (giữ nguyên mode).

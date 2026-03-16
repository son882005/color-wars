# Color Wars

Game chien thuat theo luot viet bang Pygame, ho tro 2 che do:

- `pvbot`: nguoi choi Blue vs AI Red (mac dinh)
- `pvp`: 2 nguoi choi cung may (Blue va Red)

## Tinh nang hien tai

- Ban co 5x5, can giua man hinh.
- Nguoi choi dieu khien Blue bang chuot, AI dieu khien Red.
- Luot khoi dau cua moi ben:
  - Chi duoc dat vao o trong.
  - O khoi dau nhan 3 cham.
- Sau khi da co o khoi dau:
  - Chi duoc dat vao o da co diem cua chinh minh.
  - Khong duoc dat vao o trong nua.
- Co che no day chuyen va dong hoa o lan can.
- HUD hien thi:
  - So o Blue dang chiem
  - So o Red dang chiem
  - Luot hien tai hoac nguoi thang

## Luat no va dong hoa

- Khi mot o dat du 4 cham:
  - O do no, bi xoa toan bo dot va tro ve trong.
  - Dot duoc phan tan ra 4 huong (tren, duoi, trai, phai).
  - O bi trung se bi dong hoa ve mau cua ben gay no va cong them 1 dot.
  - Neu o lan can dat moc 4 cham, tiep tuc no day chuyen.

## Dieu kien thang thua

- Muc tieu toi thuong: chiem 100% ban co bang mau cua minh va xoa so hoan toan mau doi thu.
- Trong code, nguoi thang la ben so huu toan bo `GRID_SIZE * GRID_SIZE` o.

## AI hien tai

- AI choi ben Red trong ham `ai.ai.get_ai_move(board, dots)`.
- Moi luot AI:
  - Lay nuoc hop le tu cung bo rule voi controller (khoi dau o trong, sau do chi danh o cua minh).
  - Mo phong tung nuoc (copy board/dots + xu ly no day chuyen BFS).
  - Cham diem trang thai theo so o chiem dong (`Red - Blue`) va chon nuoc diem cao nhat.

## Kien truc rule dung chung

- Rule game duoc dat tai `src/engine/rules.py`.
- Xu ly no day chuyen duoc dat tai `src/engine/explosion.py`.
- `controller` va `AI` cung goi chung engine de tranh lech logic.

## Cau truc ma nguon

- `src/main.py`: diem vao ung dung (init/quit pygame).
- `src/game/state.py`: `GameState` (board, dots, current_player, winner, turn_count).
- `src/game/loop.py`: game loop (xu ly event, mode pvp/pvbot, ve scene moi frame).
- `src/controller.py`: logic xu ly nuoc di tren `GameState` (apply move, tinh diem, xac dinh winner).
- `src/engine/rules.py`: dinh nghia rule (capacity, valid moves, constants).
- `src/engine/explosion.py`: giai no day chuyen theo BFS.
- `src/ai/ai.py`: logic chon nuoc cho Red (mo phong va danh gia board).
- `src/view.py`: phan UI/render (ve board, dot, HUD, map vi tri chuot -> o).

## Chay du an

1. Cai Python 3.10+.
1. Cai dependency:

```bash
pip install -r requirements.txt
```

1. Chay game:

```bash
python -m src.main --mode pvbot
```

Hoac che do 2 nguoi choi:

```bash
python -m src.main --mode pvp
```

## Ghi chu ky thuat

- Man hinh duoc `fill` moi frame de tranh bong hinh (render ghosting).
- Logic va UI duoc tach ro de mo rong scene, them menu, restart, AI.

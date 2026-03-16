# Color Wars

Game chien thuat theo luot viet bang Pygame (nguoi choi Blue vs AI Red).

## Tinh nang hien tai

- Ban co 5x5, can giua man hinh.
- Nguoi choi dieu khien Blue bang chuot, AI dieu khien Red.
- Moi ben dat dot theo luat:
  - Neu chua so huu o nao: chi duoc dat vao o trong.
  - Neu da so huu o: chi duoc dat vao o do chinh minh dang chiem.
- Co che no day chuyen va dong hoa o lan can.
- HUD hien thi:
  - So o Blue dang chiem
  - So o Red dang chiem
  - Luot hien tai hoac nguoi thang

## Luat no va dong hoa

- Hien tai moi o deu co suc chua = 4 (co dinh).
- Khi dot trong o dat nguong suc chua:
  - O do no, bi xoa toan bo dot va tro ve trong.
  - Dot duoc phan tan ra 4 huong (tren, duoi, trai, phai).
  - O bi trung se bi dong hoa ve mau cua ben gay no va cong them 1 dot.
  - Neu o lan can dat nguong, tiep tuc no day chuyen.

## Dieu kien thang thua

- Sau giai doan mo dau, mot ben thang khi ben con lai bi an sach.
- Logic controller hien tai:
  - Chi bat dau kiem tra thang/thua sau toi thieu 2 luot (`MIN_TURNS_FOR_WIN_CHECK = 2`).
  - Neu Red da tung co o tren ban va hien tai Red = 0 o thi Blue thang.
  - Neu Blue da tung co o tren ban va hien tai Blue = 0 o thi Red thang.

## AI hien tai

- AI choi ben Red trong ham `ai.get_ai_move(board, dots)`.
- Luot dau cua AI: chon ngau nhien 1 o trong.
- Cac luot sau:
  - Liet ke cac nuoc hop le theo luat (chi tren o Red dang so huu).
  - Mo phong tung nuoc (copy board/dots + xu ly no day chuyen BFS).
  - Cham diem trang thai theo so o chiem dong (`Red - Blue`) va chon nuoc diem cao nhat.

## Cau truc ma nguon

- `src/main.py`: diem vao ung dung (init/quit pygame).
- `src/controller.py`: game state va logic luot choi, xu ly input Blue, luot AI Red, no day chuyen, tinh diem, xac dinh winner.
- `src/ai.py`: logic chon nuoc cho Red (mo phong va danh gia board).
- `src/view.py`: phan UI/render (ve board, dot, HUD, map vi tri chuot -> o).

## Chay du an

1. Cai Python 3.10+.
1. Cai dependency:

```bash
pip install pygame
```

1. Chay game:

```bash
python src/main.py
```

## Ghi chu ky thuat

- Man hinh duoc `fill` moi frame de tranh bong hinh (render ghosting).
- Logic va UI duoc tach ro de de mo rong scene, them menu, restart, AI.

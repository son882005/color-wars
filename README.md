# Color Wars

Game chien thuat theo luot 2 nguoi choi (Blue vs Red) viet bang Pygame.

## Tinh nang hien tai

- Ban co 5x5, can giua man hinh.
- Moi luot, nguoi choi dat dot vao:
  - O trong, hoac
  - O do chinh minh dang chiem.
- Co che no day chuyen va dong hoa o lan can.
- HUD hien thi:
  - So o Blue dang chiem
  - So o Red dang chiem
  - Luot hien tai hoac nguoi thang

## Luat no va dong hoa

- Moi o co suc chua tuy vi tri:
  - Goc: 2
  - Canh: 3
  - Giua: 4
- Khi dot trong o dat nguong suc chua:
  - O do no, bi xoa toan bo dot va tro ve trong.
  - Dot duoc phan tan ra 4 huong (tren, duoi, trai, phai).
  - O bi trung se bi dong hoa ve mau cua ben gay no va cong them 1 dot.
  - Neu o lan can dat nguong, tiep tuc no day chuyen.

## Dieu kien thang thua

- Sau giai doan mo dau, mot ben thang khi ben con lai bi an sach.
- Cu the theo yeu cau du an:
  - Neu Red da tung co o tren san ma hien tai Red = 0 o, Blue thang.
  - Nguoc lai tuong tu cho Blue.

## Cau truc ma nguon

- `src/main.py`: diem vao ung dung (init/quit pygame).
- `src/controller.py`: game state va logic (input, no day chuyen, tinh diem, xac dinh winner).
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

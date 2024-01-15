import random
import curses
import time  # Import the time module

def show_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 2, "1. Start New Game")
    stdscr.addstr(1, 2, "2. Quit")
    stdscr.refresh()
    key = stdscr.getch()
    return key

def main(stdscr):
    while True:
        curses.curs_set(0)
        sh, sw = stdscr.getmaxyx()
        w = curses.newwin(sh, sw, 0, 0)
        w.keypad(1)
        w.timeout(100)

        snake_x = sw // 4
        snake_y = sh // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]

        food = [sh // 2, sw // 2]
        w.addch(food[0], food[1], curses.ACS_PI)

        key = curses.KEY_RIGHT
        score = 0

        while True:
            next_key = w.getch()

            # Check if the new direction is opposite to the current direction
            if next_key in [curses.KEY_RIGHT, curses.KEY_LEFT] and key in [curses.KEY_RIGHT, curses.KEY_LEFT] or \
               next_key in [curses.KEY_UP, curses.KEY_DOWN] and key in [curses.KEY_UP, curses.KEY_DOWN]:
                pass
            else:
                key = key if next_key == -1 else next_key

            if (
                    snake[0][0] in [0, sh] or
                    snake[0][1] in [0, sw] or
                    snake[0] in snake[1:]
            ):
                w.addstr(sh // 2, sw // 2, f'Game Over! Your score: {score}')
                w.addstr(sh // 2 + 1, sw // 2, '1. Play Again')
                w.addstr(sh // 2 + 2, sw // 2, '2. Quit to Terminal')
                w.refresh()

                choice = w.getch()
                if choice == ord('1'):
                    break
                elif choice == ord('2'):
                    w.addstr(sh // 2 + 1, sw // 2, 'Exiting to Terminal...')
                    w.refresh()
                    time.sleep(10)  # Adiciona um atraso de 10 segundos antes de sair
                    return

            new_head = [snake[0][0], snake[0][1]]

            if key == curses.KEY_DOWN:
                new_head[0] += 1
            if key == curses.KEY_UP:
                new_head[0] -= 1
            if key == curses.KEY_LEFT:
                new_head[1] -= 1
            if key == curses.KEY_RIGHT:
                new_head[1] += 1

            snake.insert(0, new_head)

            if snake[0] == food:
                score += 1
                food = None
                while food is None:
                    nf = [
                        random.randint(1, sh - 1),
                        random.randint(1, sw - 1)
                    ]
                    food = nf if nf not in snake else None
                w.addch(food[0], food[1], curses.ACS_PI)
            else:
                tail = snake.pop()
                w.addch(tail[0], tail[1], ' ')

            if 0 < snake[0][0] < sh and 0 < snake[0][1] < sw:
                w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

            w.addstr(0, 2, f'Score: {score}')

if __name__ == '__main__':
    curses.wrapper(main)

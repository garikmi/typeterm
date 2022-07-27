import random
import sys
import string
import curses
import time
from words_dictionary import generate_words


def main(term):
    # term.keypad(True)
    term.nodelay(True)

    words = generate_words()
    entered_words = ''

    is_game_going = False
    start_time = time.time()

    speed = 0

    curses.init_pair(1, 15, 16)  # background color
    curses.init_pair(2, 9, 16)  # error color
    curses.init_pair(3, 12, 16)  # typing color

    term.bkgd(' ', curses.color_pair(1))

    def refresh_ui():
        # term.clear()
        term.erase()

        if not is_game_going:
            term.addstr('press \'enter\' to start a game')
            if speed > 0:
                term.addstr(5, 0, f'speed: {speed}')
        else:
            term.addstr(5, 0, '%0.1f' % (time.time() - start_time))
            term.addstr(6, 0, f'errors: {count_errors()}')
            term.move(0, 0)

            term.addstr(words)

            term.move(0, 0)
            for index in range(len(entered_words)):
                if entered_words[index] != words[index]:
                    term.addstr(words[index], curses.color_pair(2) | curses.A_BOLD)
                else:
                    term.addstr(words[index], curses.color_pair(3) | curses.A_BOLD)

        term.refresh()

    def reset_game():
        nonlocal words
        nonlocal is_game_going
        nonlocal entered_words

        is_game_going = False
        entered_words = ''
        words = generate_words()

    def calculate_speed():
        return int(((len(entered_words) / 5) / 1) - (count_errors() / 1))  # net wpm

    def count_errors():
        error_count = 0
        for index in range(len(entered_words)):
            if entered_words[index] != words[index]:
                error_count += 1
        return error_count

    while True:
        if is_game_going and time.time() - start_time >= 60:
            speed = calculate_speed()
            reset_game()

        try:
            # disable command k to prevent screen clearing
            event = term.getch()  # get the number of the pressed key
            if event == curses.ERR:  # -1 no input
                pass
            elif event == ord('X'):  # terminate app
                break
            elif event == 127:  # backspace
                entered_words = entered_words[:-1]
            elif event == 10:  # enter
                is_game_going = not is_game_going
                start_time = time.time()
            else:
                if is_game_going and len(entered_words) < len(words):
                    key = curses.keyname(event).decode('utf-8')
                    if key in string.ascii_letters + ' ':
                        if key == ' ':
                            if len(entered_words) > 0 and entered_words[-1] != ' ':
                                entered_words += key
                        else:
                            entered_words += key

            refresh_ui()
            time.sleep(0.01)

        except KeyboardInterrupt:
            sys.exit()


curses.wrapper(main)

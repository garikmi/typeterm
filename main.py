import random
import sys
import string
import curses
import time


def main(term):
    # term.keypad(True)
    term.nodelay(True)

    words = 'hemacytometer introducement solder unparochially unconcordant debby tetrapneumonian cerebronic weeder sublateral martinoe archphylarch funkiest currijong sephirah realizer acnodal stonehearted unson crinums nonlinearly obsidians feverlike jaycees revelatory drupal polyopia disestablish londonism discriminative fenster cheerlessness maracan leucodermic brotulid perrukery focalizes quitrent basalt dorm rort beckoningly tyrosinuria crankest pickup undramatical unempaneled pilgarlicky shrift raptureless unalluring neutralizers plagioclimax candlesticks chrysography pleadingness nephrocystosis crisis undeductible huckstress buffware untimid quiff tiddlywink gyrostatic metabiological ureterostenoma demodulate cooed streamliner'
    entered_words = ''

    is_game_going = False
    start_time = time.time()

    speed = 0

    # error_count = 0

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def refresh_ui():
        term.clear()

        term.addstr(10, 0, '%0.1f' % (time.time() - start_time))
        term.addstr(11, 0, f'speed: {speed}')
        term.addstr(12, 0, f'errors: {count_errors()}')
        # term.addstr(12, 0, f'errors: {error_count}')
        term.move(0, 0)

        term.addstr(words)

        term.move(0, 0)
        for index in range(len(entered_words)):
            if entered_words[index] != words[index]:
                term.addstr(words[index], curses.color_pair(1))
            else:
                term.addstr(words[index], curses.color_pair(2))

        term.refresh()

    def reset_game():
        nonlocal words
        nonlocal is_game_going
        nonlocal entered_words

        is_game_going = False
        entered_words = ''
        # add new words and shuffle
        # display results

    def calculate_speed():
        # return (len(entered_words) / 5) / 1  # gross wpm
        # return ((len(entered_words) / 5) / 0.5) - (error_count / 0.5)  # net wpm
        return ((len(entered_words) / 5) / 0.5) - (count_errors() / 0.5)  # net wpm

    def count_errors():
        error_count = 0
        for index in range(len(entered_words)):
            if entered_words[index] != words[index]:
                error_count += 1
        return error_count

    while True:
        if is_game_going and time.time() - start_time >= 30:
            speed = int(calculate_speed())
            reset_game()

        try:
            event = term.getch()  # get the number of the pressed key
            if event == curses.ERR:  # -1 no input
                pass
            elif event == ord('x'):  # terminate app
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

                        # pos = len(entered_words)-1
                        # if pos < 0:
                        #     pos = 0
                        # if entered_words[-1] != ' ' and words[pos] != entered_words[-1]:
                        #     error_count += 1

            refresh_ui()
            time.sleep(0.01)

        except KeyboardInterrupt:
            sys.exit()


curses.wrapper(main)

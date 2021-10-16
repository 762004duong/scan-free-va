import pyttsx3
import speech_recognition as sr


def read_file(filename):
    """
    Read content in filename
    :param filename:
    :return: contents
    """
    with open(filename, mode='r', encoding='utf8') as fp:
        contents = fp.read()
        return contents.splitlines()


def find_answer(text, list_cons, list_prices):
    """
    Find price for consumption
        - Find index of this consumption in list_cons
        - Return correspond price in list_prices
    :param text:
    :param list_cons:
    :param list_prices:
    :return:
    """
    for idx, cons in enumerate(list_cons):
        if cons.lower() in text.lower():
            return list_prices[idx]
    return -1


def say(text):
    global engine
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    engine = pyttsx3.init()
    recognizer = sr.Recognizer()
    list_cons = read_file('data/question.txt')
    list_prices = read_file('data/answer.txt')
    list_stops = read_file('data/stopped.txt')

    with sr.Microphone() as src:
        recognizer.adjust_for_ambient_noise(src)
        run = True
        error = 0
        while run and error <= 3:
            say(" What information that you want to know?")
            print("Listening....")
            audio = recognizer.listen(src, timeout=8, phrase_time_limit=2)
            print(error)
            try:
                text = recognizer.recognize_google(audio)
                error = 0
                print(text)

                for word in list_stops:
                    if word in text.lower():
                        say("Good bye. Have a good day!")
                        run = False
                if not run:
                    break
                ans = find_answer(text, list_cons, list_prices)
                print(ans)
                if ans == -1:
                    say("I don't know!")
                else:
                    say(ans)
                say("Do you want to continue?")
                say("Please say yes or no")
                print(" Yes or No")
                audio = recognizer.listen(src)
                text = recognizer.recognize_google(audio)
                print(text)
                if "yes" not in text.lower():
                    say("Bye")
                    break
            except sr.UnknownValueError:
                print("Dont know")
                say("Can you repeat?")
                error += 1
            except sr.RequestError:
                print("RequestError")
                say("Network is out of service")
                break
            except sr.WaitTimeoutError:
                print("WaitTimeoutError")
            except sr.HTTPError:
                print("HTTPError")
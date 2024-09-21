from cs50 import get_string


def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count


def count_words(text):
    count = 0
    for char in text:
        if char.isspace():
            count += 1
    return count + 1


def count_sentences(text):
    count = 0
    for char in text:
        if char in '.!?':
            count += 1
    return count


def calculate_grade_level(letters, words, sentences):
    L = letters / words * 100
    S = sentences / words * 100
    return round(0.0588 * L - 0.296 * S - 15.8)


text = get_string("Enter text: ")

letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

grade = calculate_grade_level(letters, words, sentences)

if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print("Grade", int(grade))

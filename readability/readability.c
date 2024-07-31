#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Main functions
int countLetters(string text);
int countWords(string text);
int countSentences(string text);
float calculateGradeLevel(int letters, int words, int sentences);

int main(void)
{

    // Prompt the user for an input text
    string text = get_string("Enter text: ");

    // Counting
    int letters = countLetters(text);
    int words = countWords(text);
    int sentences = countSentences(text);
    printf("Number of sentences: %i\n",sentences);

    // Grade level
    float grade = calculateGradeLevel(letters, words, sentences);

    // Print the result
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        int gradeInt = (int) grade;
        printf("Grade %i\n", gradeInt);
    }
}

// Return number of letters
int countLetters(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

// Return number of words
int countWords(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isspace(text[i]))
        {
            count++;
        }
    }
    return count + 1;
}

// Return number of sentences
int countSentences(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}

// Calculate grade level (rounded)
float calculateGradeLevel(int letters, int words, int sentences)
{
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;
    return round(0.0588 * L - 0.296 * S - 15.8);
}

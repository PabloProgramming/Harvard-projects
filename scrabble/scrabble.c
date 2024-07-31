#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Define points for each letter

const int onePointLetters[10] = {'a', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't', 'u'};
const char twoPointLetters[2] = {'d', 'g'};
const char threePointLetters[4] = {'b', 'c', 'm', 'p'};
const char fourPointLetters[5] = {'f', 'h', 'v', 'w', 'y'};
const char fivePointLetter = 'k';
const char eightPointLetters[2] = {'j', 'x'};
const char tenPointLetters[2] = {'q', 'z'};

// Function prototype
int computeScore(string word);

int main(void)
{

// Prompt the 2 players to type a word

    string wordPlayer1 = get_string("Player 1 type your word: ");
    string wordPlayer2 = get_string("Player 2 type your word: ");

// Compute scores for both words

    int player1Score = computeScore(wordPlayer1);
    int player2Score = computeScore(wordPlayer2);

// Define the winner

    if (player1Score > player2Score)
    {
        printf("Player 1 wins!\n");
    }
    else if (player2Score > player1Score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

// Function to compute the score

int computeScore(string word)
{
    int valueOfWord = 0;
    int length = strlen(word);

    for (int i = 0; i < length; i++)
    {

// Convert letter to lowercase to handle case insensitivity
        char letter = tolower(word[i]);

// Check which array the letter belongs to and add points accordingly

        for (int j = 0; j < 10; j++)
        {
            if (letter == onePointLetters[j])
            {
                valueOfWord += 1;
                break;
            }
        }

        for (int j = 0; j < 2; j++)
        {
            if (letter == twoPointLetters[j])
            {
                valueOfWord += 2;
                break;
            }
        }

        for (int j = 0; j < 4; j++)
        {
            if (letter == threePointLetters[j])
            {
                valueOfWord += 3;
                break;
            }
        }

        for (int j = 0; j < 5; j++)
        {
            if (letter == fourPointLetters[j])
            {
                valueOfWord += 4;
                break;
            }
        }

        if (letter == fivePointLetter)
        {
            valueOfWord += 5;
        }

        for (int j = 0; j < 2; j++)
        {
            if (letter == eightPointLetters[j])
            {
                valueOfWord += 8;
                break;
            }
        }

        for (int j = 0; j < 2; j++)
        {
            if (letter == tenPointLetters[j])
            {
                valueOfWord += 10;
                break;
            }
        }
    }

    return valueOfWord;
}

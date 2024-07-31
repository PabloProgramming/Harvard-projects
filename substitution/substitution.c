#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Main functions
bool isValidKey(string key);
void plainTextToCipher(string key, string plaintext);

int main(int argc, string argv[])
{
//Check if program receives one line argument as KEY
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

// Prompt the user for a valid key
    string key = argv[1];
    if (!isValidKey(key))
    {
        printf("Key must contain 26 unique alphabetic characters. \n");
        return 1;
    }

// Prompt user for plaintext input
    string plaintext = get_string("plaintext: ");

// Turn plaintext into cipherText
    printf("ciphertext: ");
    plainTextToCipher(key, plaintext);
    printf("\n");

    return 0;
}

// Define what is a valid KEY
bool isValidKey(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }

    bool letters[26] = {false};

    for (int i = 0; i < 26; i++)
    {

        if (!isalpha(key[i]))
        {

            return false;
        }
        int index = tolower(key[i]) - 'a';
        if (letters[index])
        {

            return false;
        }
        letters[index] = true;
    }
    return true;
}
// Encrypt text to cipher
void plainTextToCipher(string key, string plaintext)
{

// Arrays for storing lower and uppercase letters
    char lowerMap[26];
    char upperMap[26];

    for (int i = 0; i < 26; i++)
    {
        lowerMap[i] = tolower(key[i]);
        upperMap[i] = toupper(key[i]);
    }

    for (int i = 0; i < strlen(plaintext); i++)
    {
        char ch = plaintext[i];
        if (islower(ch))
        {

            int index = ch - 'a';
            printf("%c", lowerMap[index]);
        }
        else if (isupper(ch))
        {
            int index = ch - 'A';
            printf("%c", upperMap[index]);
        }
        else
        {
// Non alphabetic character unchanged
            printf("%c", ch);
        }
    }
}

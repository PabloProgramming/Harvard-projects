// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

#define HASH_TABLE_SIZE 10000

// Defines struct for a node
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} Node;

Node *hashTable[HASH_TABLE_SIZE];

// Hashes the word using a simple hash function
unsigned int hashIndex(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hash = (hash * 31) + tolower(word[i]);
    }
    return hash % HASH_TABLE_SIZE;
}

// Initializes counter for words in dictionary
int wordCount = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Read dictionary word by word and populate hash table with nodes containing words found in
    // dictionary
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for a new node
        Node *newNode = malloc(sizeof(Node));
        if (newNode == NULL)
        {
            unload();
            fclose(file);
            return false;
        }

        // Copy word into node
        strcpy(newNode->word, word);

        // Calculate index for insertion into hash table
        unsigned int index = hashIndex(newNode->word);

        // Insert new node into hash table at calculated index
        newNode->next = hashTable[index];
        hashTable[index] = newNode;

        // Increment word count
        wordCount++;
    }

    fclose(file);
    return true;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Create a lowercase copy of the word
    char wordCopy[LENGTH + 1];
    int length = strlen(word);
    for (int i = 0; i < length; i++)
    {
        wordCopy[i] = tolower(word[i]);
    }
    wordCopy[length] = '\0';

    // Calculate index for hashed word
    unsigned int index = hashIndex(wordCopy);

    // Traverse the linked list at that index in the hash table
    Node *cursor = hashTable[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, wordCopy) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        Node *cursor = hashTable[i];
        while (cursor != NULL)
        {
            Node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}

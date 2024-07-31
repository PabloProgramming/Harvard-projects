#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    // Get valid pyramid height from user
    do
    {
        height = get_int("Height: Type a number between 1 and 8: ");
    }
    while (height < 1 || height > 8);

    // Print the pyramid shape (height - row)
    for (int row = 1; row <= height; row++)
    {
        for (int space = 1; space <= height - row; space++)
        {
            printf(" ");
        }
        // Print left hashes of the pyramid
        for (int hash = 1; hash <= row; hash++)
        {
            printf("#");
        }
        // Print middle space
        printf("  ");

        // Print right hashes of the pyramid
        for (int hash = 1; hash <= row; hash++)
        {
            printf("#");
        }

        printf("\n");
    }
    return 0;
}

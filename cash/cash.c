#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int changeOwed;
    int numOfCoins = 0;
    // Prompt the user to write a number > 0
    do
    {
        changeOwed = get_int("Type a changeOwed in cents: ");
    }
    while (changeOwed < 1);

    // Use the least number of coins
    for (int i = 1; changeOwed > 0; i++)
    {
        if (changeOwed >= 25)
        {
            changeOwed -= 25;
            numOfCoins++;
        }
        else if (changeOwed >= 10)
        {
            changeOwed -= 10;
            numOfCoins++;
        }
        else if (changeOwed >= 5)
        {
            changeOwed -= 5;
            numOfCoins++;
        }
        else
        {
            changeOwed -= 1;
            numOfCoins++;
        }
    }

    // Print number of coins
    printf("Number of coins: %i\n", numOfCoins);
    return 0;
}

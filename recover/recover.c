#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Single comand-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer
    uint8_t buffer[BLOCK_SIZE];

    // Variable to keep track of JPEG files
    FILE *img = NULL;
    int imgCount = 0;
    char fileName[8];

    // Read while there is still data left
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new fileName for new JPEG
            sprintf(fileName, "%03i.jpg", imgCount);
            imgCount++;

            // Open a new file to write JPG data
            img = fopen(fileName, "w");
            if (img == NULL)
            {
                printf("COuld not create output file.\n");
                fclose(card);
                return 1;
            }
        }

        // If JPG is open, write the block
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    // Close remaining files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);

    return 0;
}

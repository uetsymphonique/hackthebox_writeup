#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file;
    unsigned char buffer[4];
    unsigned int value = 0;

    
    // Open the file in binary mode
    file = fopen("flag.enc", "rb");

    if (file == NULL) {
        printf("Error opening the file.\n");
        return 1;
    }

    // Read the first four bytes
    size_t bytesRead = fread(buffer, sizeof(unsigned char), 4, file);

    if (bytesRead != 4) {
        printf("Error reading the file.\n");
        fclose(file);
        return 1;
    }

    // Convert the four bytes to an integer
    value = (buffer[3] << 24) | (buffer[2] << 16) | (buffer[1] << 8) | buffer[0];

    // Print the integer value
    printf("Random seed: %u\n", value);
    srand(value);

    // Print the rest of the file
    printf("Flag:\n");
    int byte;
    while ((byte = fgetc(file)) != EOF) {
        // printf("%02X ", byte);
        int r1 = rand();
        int r2 = rand() & 7;
        byte = byte << (8 - r2) | byte >> r2;
        byte = byte ^ r1;
        printf("%c", (char)byte);
    }
    printf("\n");

    // Close the file
    fclose(file);

    return 0;
}
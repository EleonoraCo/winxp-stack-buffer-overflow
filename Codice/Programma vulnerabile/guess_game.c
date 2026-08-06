#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void get_name() {
    char buffer[64];
    printf("Come ti chiami? ");
    fgets(buffer, 1024, stdin);   
    printf("Ciao %s", buffer);
}

int main() {
    int secret, guess;

    srand((unsigned)time(NULL));
    secret = (rand() % 100) + 1;

    get_name();

    printf("Ho pensato un numero da 1 a 100. Indovina: ");
    scanf("%d", &guess);

    if (guess == secret)
        printf("Complimenti! Hai indovinato!\n");
    else
        printf("Sbagliato, il numero era %d. Ritenta!\n", secret);

    return 0;
}
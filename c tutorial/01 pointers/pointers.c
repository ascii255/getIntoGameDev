#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
	int i = 8;
	int* iPtr = &i;

	char* myStr = (char*)malloc(3 * sizeof(char));
	myStr[0] = 'H';
	myStr[1] = 'i';
	myStr[2] = '\0';

	int** myArray = (int**)malloc(2 * sizeof(int*));
	myArray[0] = (int*)malloc(4 * sizeof(int));
	myArray[1] = (int*)malloc(4 * sizeof(int));
	myArray[0][0] = 0;
	myArray[0][0] = 1;
	myArray[0][0] = 2;

	printf("Hello my dudes!\n");
	printf("Integer i has value %d\n", i);
	printf("Integer i has location %p\n", iPtr);
	printf("Integer i has value %d\n", *iPtr);

	printf("String myStr has location %p\n", &myStr);
	printf("String myStr has value %s\n", myStr);
	free(myStr);
	printf("String myStr has location %p\n", &myStr);
	//printf("String myStr has value %s\n", myStr);
	for (int i = 0; i < 2; i++) {
		free(myArray[i]);
	}
	free(myArray);
	return 0;
}
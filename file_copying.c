#include <stdio.h> 
#include <stdlib.h> 
  
int main() 
{ 
    FILE *file_ptr1, *file_ptr2; 
    char filename[100], c; 
  
    printf("Enter the filename to open for reading: "); 
    scanf("%s", filename); 
  
    file_ptr1 = fopen(filename, "r"); 

    printf("\nEnter the filename to open for writing: "); 
    scanf("%s", filename); 

    file_ptr2 = fopen(filename, "w"); 

    c = fgetc(file_ptr1); 

    while (c != EOF) 
    { 
        fputc(c, file_ptr2); 
        c = fgetc(file_ptr1);
    } 
  
    fclose(file_ptr1); 
    fclose(file_ptr2); 
    return 0; 
}
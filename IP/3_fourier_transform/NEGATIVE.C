#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <complex.h>
#define PI 3.141592654

/*-------STRUCTURES---------*/
typedef struct {int rows; int cols; unsigned char* data;} sImage;

/*-------PROTOTYPES---------*/
long getImageInfo(FILE*, long, int);
void copyImageInfo(FILE* inputFile, FILE* outputFile);
void copyColorTable(FILE* inputFile, FILE* outputFile, int nColors);

int main(int argc, char* argv[])
{
  FILE			*bmpInput, *bmpOutput;
  sImage		originalImage;
  unsigned char		someChar;
  unsigned char*	pChar;
  unsigned char*  newChar;
  int			nColors;  /* BMP number of colors */
  long			fileSize; /* BMP file size */
  int			vectorSize; /* BMP vector size */
  int			r, c, ir, ic, ft;       /* r = rows, c = cols, ir = input_rows, ic = input_cols, ft = fourier transform value */
  double value,sum = 0, stat_val,real, imag;
  int holder[256][256] = {0};
  int transform[256][256] = {0};

  /* initialize pointer */
  someChar = '0';
  pChar = &someChar;
  newChar = &someChar;

  if(argc < 2)
  {
    printf("Usage: %s bmpInput.bmp\n", argv[0]);
    exit(0);
  }
  printf("Reading filename %s\n", argv[1]);

  /*--------READ INPUT FILE------------*/
  bmpInput = fopen(argv[1], "rb");
  fseek(bmpInput, 0L, SEEK_END);




  /*--------DECLARE OUTPUT FILE--------*/
  bmpOutput = fopen("output_test.bmp", "wb");

  /*--------GET BMP DATA---------------*/
  originalImage.cols = (int)getImageInfo(bmpInput, 18, 4);
  originalImage.rows = (int)getImageInfo(bmpInput, 22, 4);
  fileSize = getImageInfo(bmpInput, 2, 4);
  nColors = getImageInfo(bmpInput, 46, 4);
  vectorSize = fileSize - (14 + 40 + 4*nColors);

  /*-------PRINT DATA TO SCREEN-------------*/
  printf("Width: %d\n", originalImage.cols);
  printf("Height: %d\n", originalImage.rows);
  printf("File size: %ld\n", fileSize);
  printf("# Colors: %d\n", nColors);
  printf("Vector size: %d\n", vectorSize);

  copyImageInfo(bmpInput, bmpOutput);
  copyColorTable(bmpInput, bmpOutput, nColors);

  /*----START AT BEGINNING OF RASTER DATA-----*/
  fseek(bmpInput, (54 + 4*nColors), SEEK_SET);
  //fseek(bmpOutput, (54 + 4*nColors), SEEK_SET);

  /*----------READ RASTER DATA----------*/
  for(r=0; r<=originalImage.rows - 1; r++)
  {
    for(c=0; c<=originalImage.cols - 1; c++)
    {
      /*-----read data, reflect and write to output file----*/

      fread(newChar, sizeof(char), 1, bmpInput);
      holder[r][c]= int( *pChar );

      //  *pChar = 255 - *pChar;
      //fwrite(newChar, sizeof(char), 1, bmpOutput);
    }
  }

  for(r=0; r<=originalImage.rows - 1; r++)
  {
    for(c=0; c<=originalImage.cols - 1; c++)
    {
      /*-----read data, reflect and write to output file----*/
        sum = 0;
        for(ir=0; ir<=originalImage.rows - 1; ir++)
        {
          
          for(ic=0; ic<=originalImage.cols - 1; ic++)
          {
            fread(pChar, sizeof(char), 1, bmpInput);
            stat_val = (r*ir + c*ic) / 20;      // size of image is 20x20
            stat_val = -2 * PI * stat_val;
            stat_val = (stat_val * PI) / 180;
            //stat_val = cos(stat_val) + sin(stat_val);
            stat_val = holder[ir][ic] * stat_val;
            real += cos(stat_val);
            imag = imag - sin(stat_val);
            
            //stat_val = holder[ir][ic] * stat_val;
            //sum = sum + stat_val;
          }
        }
        real = real / 20;
        imag = imag / 20;
        //printf("*** %d *** %d\n", r, (int)sum);
        //transform[r][c] = sum;
        //*newChar = sum;
        //printf("****%lf**** REAL\n", real);
        printf("****%lf**** IMAG\n", pow(imag,2));
        sum = sqrt(pow(real,2) + pow(imag,2));
        transform[r+5][c+5] = sum;
    }
  }

  for(r=0; r<=originalImage.rows - 1; r++)
  {
    for(c=0; c<=originalImage.cols - 1; c++)
    {

      printf("%d,", transform[r][c]);
      *pChar = transform[r][c];
      fwrite(newChar, sizeof(char), 1, bmpOutput);

    }
  }

  fclose(bmpInput);
  fclose(bmpOutput);
return(0);
}




/*----------GET IMAGE INFO SUBPROGRAM--------------*/
long getImageInfo(FILE* inputFile, long offset, int numberOfChars)
{
  unsigned char			*ptrC;
  long				value = 0L;
  unsigned char			dummy;
  int				i;

  dummy = '0';
  ptrC = &dummy;

  fseek(inputFile, offset, SEEK_SET);

  for(i=1; i<=numberOfChars; i++)
  {
    fread(ptrC, sizeof(char), 1, inputFile);
    /* calculate value based on adding bytes */
    value = (long)(value + (*ptrC)*(pow(256, (i-1))));
  }
  return(value);

} /* end of getImageInfo */

/*-------------COPIES HEADER AND INFO HEADER----------------*/
void copyImageInfo(FILE* inputFile, FILE* outputFile)
{
  unsigned char		*ptrC;
  unsigned char		dummy;
  int				i;

  dummy = '0';
  ptrC = &dummy;

  fseek(inputFile, 0L, SEEK_SET);
  fseek(outputFile, 0L, SEEK_SET);

  for(i=0; i<=50; i++)
  {
    fread(ptrC, sizeof(char), 1, inputFile);
    fwrite(ptrC, sizeof(char), 1, outputFile);
  }

}

/*----------------COPIES COLOR TABLE-----------------------------*/
void copyColorTable(FILE* inputFile, FILE* outputFile, int nColors)
{
  unsigned char		*ptrC;
  unsigned char		dummy;
  int				i;

  dummy = '0';
  ptrC = &dummy;

  fseek(inputFile, 54L, SEEK_SET);
  fseek(outputFile, 54L, SEEK_SET);

  for(i=0; i<=(4*nColors); i++)  /* there are (4*nColors) bytesin color table */
  {
    fread(ptrC, sizeof(char), 1, inputFile);
    fwrite(ptrC, sizeof(char), 1, outputFile);
  }

}







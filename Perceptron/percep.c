#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define epoca 3000000
#define K 0.03f

//0.00000
//Funcion de Entrenamiento Perceptron
float EntNt(float, float, float  );
//Funcion para las salidas 
float InitNt(float, float);
//Sigmoide
float sigmoide(float);
//pesos aleatorios
void pesos_initNt();

float Pesos[2];	
float bias=0.5f;
float Error;

// Pesos de la capa oculta
float PesosOcultos[2][2];
float BiasOcultos[2];

// Pesos de la capa de salida
float PesosSalida[2];
float BiasSalida=0.5f;


//                 1          1          1
//                 0          1         0           
//                 1          0         0
//                0          0          0
float EntNt( float x0, float x1, float target )
{
  
//printf("x0=%f, x1=%f, t %f \n" ,x0, x1,  target );
  
  float net = 0;
  float out = 0;
  float delta[2];  //Es la variacion de los pesos sinapticos
  //float Error;

  float ocultas[2];
  float netSalida;
  float errorSalida;
  float errorOculta[2];

  ocultas[0] = sigmoide(
      PesosOcultos[0][0]*x0 +
      PesosOcultos[0][1]*x1 -
      BiasOcultos[0]
  );

  ocultas[1] = sigmoide(
      PesosOcultos[1][0]*x0 +
      PesosOcultos[1][1]*x1 -
      BiasOcultos[1]
  );

  netSalida = PesosSalida[0]*ocultas[0] +
              PesosSalida[1]*ocultas[1] -
              BiasSalida;

  net = sigmoide(netSalida);

  Error = target - net;

  errorSalida = Error * net * (1.0f - net);

  errorOculta[0] =
      errorSalida *
      PesosSalida[0] *
      ocultas[0] *
      (1.0f - ocultas[0]);

  errorOculta[1] =
      errorSalida *
      PesosSalida[1] *
      ocultas[1] *
      (1.0f - ocultas[1]);

  PesosSalida[0] += K * errorSalida * ocultas[0];
  PesosSalida[1] += K * errorSalida * ocultas[1];

  BiasSalida -= K * errorSalida;

  PesosOcultos[0][0] += K * errorOculta[0] * x0;
  PesosOcultos[0][1] += K * errorOculta[0] * x1;

  PesosOcultos[1][0] += K * errorOculta[1] * x0;
  PesosOcultos[1][1] += K * errorOculta[1] * x1;

  BiasOcultos[0] -= K * errorOculta[0];
  BiasOcultos[1] -= K * errorOculta[1];

  out=net;
  return out;
}


 
float InitNt( float x0, float x1 )
{
  float net = 0;
  float out = 0;
//Pesos de cada epoca
//Peso 1 = 30.753101
//Peso 2 = 30.780966
//BiasBias = 61.583714
//Resultados 
//  net = 1.23*x0 + 2.4*x1+23;
//Peso 1 = 989.755493
//Peso 2 = -1407.284180
//Bias = 989.755981 

net = 70.934807*x0 + 93.935219*x1 - 187.886169 ;

  //net = 316.518982*x0 + 316.522095*x1-633.045837;
  net=sigmoide( net );
   
  out=net;
  return out;
}

 
 
void pesos_initNt(void)
{
int i;
  for(  i = 0; i < 2; i++ )
  {
    Pesos[i] = (float)rand()/RAND_MAX;
  }

  for(i = 0; i < 2; i++)
  {
    PesosOcultos[i][0] = (float)rand()/RAND_MAX;
    PesosOcultos[i][1] = (float)rand()/RAND_MAX;
    BiasOcultos[i] = (float)rand()/RAND_MAX;
  }

  for(i = 0; i < 2; i++)
  {
    PesosSalida[i] = (float)rand()/RAND_MAX;
  }
}
 
float sigmoide( float s ){
  return (1.0f/(1.0f + expf(-s)));
}

int main(){
  int i=0;
  float apr;
  pesos_initNt();
  
 while(i<epoca){
    
    printf("------------------------\n");
    printf("Salida Entrenamiento Epoco %d \n", i);
    apr=EntNt(1,1,0);
    printf("1,1=%f\n",apr);
    apr=EntNt(1,0,1);
    printf("1,0=%f\n",apr);
    apr=EntNt(0,1,1);
    printf("0,1=%f\n",apr);
    apr=EntNt(0,0,0);
    printf("0,0=%f\n",apr);
    printf("\n"); 
    printf("Pesos de cada epoca\n");
    printf("Peso 0 = %f\n", Pesos[0]);
    printf("Peso 1 = %f\n", Pesos[1]);
  
    printf("Bias = %f \n",bias);
    printf("Error %f\n ",Error  );
    printf("------------------------\n"); 
    i++;   
/*

    printf("Resultados\n");
    apr=InitNt(1,1);
    printf("1,1=%f\n",apr);
    apr=InitNt(1,0);
    printf("1,0=%f\n",apr);
    apr=InitNt(0,1);
    printf("0,1=%f\n",apr);
    apr=InitNt(0,0);
    printf("0,0=%f\n",apr);
*/

}

  return 0;
}
